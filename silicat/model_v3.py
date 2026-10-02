"""Silicat v3 — a modernized decoder-only transformer (2026 architecture).

Upgrades over the v2 GPT-2-style model, based on what small models converged on
in 2025-2026 (Qwen3 / SmolLM3 / Llama-3 design choices):

  - RMSNorm instead of LayerNorm (faster, no mean-subtraction, no bias)
  - RoPE (rotary position embeddings) instead of learned absolute positions,
    with NoPE (no positional encoding) on every 4th layer for better length
    generalisation (SmolLM3's 3:1 RoPE:NoPE trick)
  - GQA (grouped-query attention): fewer KV heads than query heads -> smaller
    KV cache and faster attention with ~no quality loss
  - QK-Norm: RMSNorm on per-head queries and keys before attention, which
    prevents attention-logit blow-up and stabilises training
  - SwiGLU feed-forward instead of GELU MLP (better quality per parameter)
  - Weight tying between token embedding and the output head (the head reuses
    `tok_emb.weight` directly, so the state_dict holds a single copy)
  - Exact KV cache (`KVCache`) for fast incremental decoding

Still small and readable; still one file.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from .model import make_adamw


@dataclass
class GPTConfigV3:
    vocab_size: int = 32768
    block_size: int = 512
    n_layer: int = 12
    n_head: int = 12          # query heads
    n_kv_head: int = 4        # key/value heads (GQA); n_head % n_kv_head == 0
    n_embd: int = 768
    dropout: float = 0.0
    rope_theta: float = 10000.0
    nope_every: int = 4       # every Nth layer uses NO positional encoding
    norm_eps: float = 1e-5

    @property
    def head_dim(self) -> int:
        return self.n_embd // self.n_head


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-5):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        x = x.float()
        x = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return (x * self.weight).to(dtype)


def _rope_tables(start: int, length: int, head_dim: int, theta: float, device) -> tuple[torch.Tensor, torch.Tensor]:
    """fp32 (cos, sin) tables of shape (length, head_dim) for positions start..start+length-1.

    Computed on the fly (not buffers) so they never follow the model dtype."""
    inv_freq = 1.0 / (theta ** (torch.arange(0, head_dim, 2, dtype=torch.float32, device=device) / head_dim))
    t = torch.arange(start, start + length, dtype=torch.float32, device=device)
    freqs = torch.outer(t, inv_freq)          # (length, head_dim/2)
    emb = torch.cat([freqs, freqs], dim=-1)   # (length, head_dim)
    return emb.cos(), emb.sin()


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    half = x.shape[-1] // 2
    x1, x2 = x[..., :half], x[..., half:]
    return torch.cat([-x2, x1], dim=-1)


def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    # x: (B, n_head, T, head_dim); cos/sin: (T, head_dim), fp32. Rotate in fp32, keep x's dtype.
    xf = x.float()
    return ((xf * cos) + (_rotate_half(xf) * sin)).to(x.dtype)


class KVCache:
    """Per-request key/value cache for incremental decoding (batch size fixed at first use).

    Not an nn.Module/buffer: it never touches state_dict. Holds post-QK-norm,
    post-RoPE keys at n_kv_head width (GQA-sized). `length` is advanced once per
    model forward by GPTV3.forward, so every layer sees the same past."""

    def __init__(self, n_layer: int, block_size: int):
        self.n_layer = n_layer
        self.block_size = block_size
        self.k: list[torch.Tensor | None] = [None] * n_layer
        self.v: list[torch.Tensor | None] = [None] * n_layer
        self.length = 0

    def reset(self) -> None:
        self.length = 0

    def update(self, layer: int, k: torch.Tensor, v: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        B, H, T, D = k.shape
        if self.k[layer] is None:
            self.k[layer] = k.new_empty(B, H, self.block_size, D)
            self.v[layer] = v.new_empty(B, H, self.block_size, D)
        s, e = self.length, self.length + T
        self.k[layer][:, :, s:e] = k
        self.v[layer][:, :, s:e] = v
        return self.k[layer][:, :, :e], self.v[layer][:, :, :e]


class Attention(nn.Module):
    def __init__(self, cfg: GPTConfigV3, use_rope: bool, layer_idx: int = 0):
        super().__init__()
        self.layer_idx = layer_idx
        assert cfg.n_embd % cfg.n_head == 0
        assert cfg.n_head % cfg.n_kv_head == 0
        self.n_head = cfg.n_head
        self.n_kv_head = cfg.n_kv_head
        self.head_dim = cfg.head_dim
        self.use_rope = use_rope
        self.dropout = cfg.dropout

        self.q_proj = nn.Linear(cfg.n_embd, cfg.n_head * self.head_dim, bias=False)
        self.k_proj = nn.Linear(cfg.n_embd, cfg.n_kv_head * self.head_dim, bias=False)
        self.v_proj = nn.Linear(cfg.n_embd, cfg.n_kv_head * self.head_dim, bias=False)
        self.o_proj = nn.Linear(cfg.n_head * self.head_dim, cfg.n_embd, bias=False)

        # QK-Norm: RMSNorm over the per-head dimension
        self.q_norm = RMSNorm(self.head_dim, eps=cfg.norm_eps)
        self.k_norm = RMSNorm(self.head_dim, eps=cfg.norm_eps)

    def forward(
        self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor, cache: KVCache | None = None
    ) -> torch.Tensor:
        B, T, C = x.shape
        q = self.q_proj(x).view(B, T, self.n_head, self.head_dim)
        k = self.k_proj(x).view(B, T, self.n_kv_head, self.head_dim)
        v = self.v_proj(x).view(B, T, self.n_kv_head, self.head_dim)

        # QK-Norm (applied per head, before RoPE)
        q = self.q_norm(q)
        k = self.k_norm(k)

        q = q.transpose(1, 2)   # (B, n_head, T, hd)
        k = k.transpose(1, 2)   # (B, n_kv_head, T, hd)
        v = v.transpose(1, 2)

        if self.use_rope:       # cos/sin already cover positions [past, past+T)
            q = _apply_rope(q, cos, sin)
            k = _apply_rope(k, cos, sin)

        if cache is None:
            y = F.scaled_dot_product_attention(
                q, k, v,
                dropout_p=self.dropout if self.training else 0.0,
                is_causal=True,
                enable_gqa=True,
            )
        else:
            past = cache.length
            k, v = cache.update(self.layer_idx, k, v)
            mask = None
            causal = False
            if past == 0:
                causal = True
            elif T > 1:  # chunked prefill onto a non-empty cache
                mask = torch.ones(T, past + T, dtype=torch.bool, device=q.device).tril(diagonal=past)
            y = F.scaled_dot_product_attention(
                q, k, v, attn_mask=mask, dropout_p=0.0, is_causal=causal, enable_gqa=True
            )
        y = y.transpose(1, 2).contiguous().view(B, T, self.n_head * self.head_dim)
        return self.o_proj(y)


class SwiGLU(nn.Module):
    def __init__(self, cfg: GPTConfigV3):
        super().__init__()
        # SwiGLU hidden dim ~ 8/3 * n_embd, rounded to a multiple of 64
        hidden = int(8 / 3 * cfg.n_embd)
        hidden = 64 * ((hidden + 63) // 64)
        self.gate = nn.Linear(cfg.n_embd, hidden, bias=False)
        self.up = nn.Linear(cfg.n_embd, hidden, bias=False)
        self.down = nn.Linear(hidden, cfg.n_embd, bias=False)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.drop(self.down(F.silu(self.gate(x)) * self.up(x)))


class Block(nn.Module):
    def __init__(self, cfg: GPTConfigV3, layer_idx: int):
        super().__init__()
        # NoPE on every Nth layer (1-indexed: layers 4, 8, 12, ... skip RoPE)
        use_rope = ((layer_idx + 1) % cfg.nope_every) != 0
        self.attn_norm = RMSNorm(cfg.n_embd, eps=cfg.norm_eps)
        self.attn = Attention(cfg, use_rope=use_rope, layer_idx=layer_idx)
        self.mlp_norm = RMSNorm(cfg.n_embd, eps=cfg.norm_eps)
        self.mlp = SwiGLU(cfg)

    def forward(
        self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor, cache: KVCache | None = None
    ) -> torch.Tensor:
        x = x + self.attn(self.attn_norm(x), cos, sin, cache)
        x = x + self.mlp(self.mlp_norm(x))
        return x


class GPTV3(nn.Module):
    def __init__(self, cfg: GPTConfigV3):
        super().__init__()
        self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.n_embd)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList([Block(cfg, i) for i in range(cfg.n_layer)])
        self.norm_f = RMSNorm(cfg.n_embd, eps=cfg.norm_eps)
        # output head = tok_emb.weight (tied; no separate parameter / state_dict key)

        self.apply(self._init_weights)
        # scaled init for residual projections (GPT-2 trick)
        for n, p in self.named_parameters():
            if n.endswith("o_proj.weight") or n.endswith("down.weight"):
                nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * cfg.n_layer))

    @staticmethod
    def _init_weights(m: nn.Module) -> None:
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)

    def num_params(self, non_embedding: bool = False) -> int:
        """Unique trainable params (the tied embedding/head counts once)."""
        n = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return n - self.tok_emb.weight.numel() if non_embedding else n

    def new_cache(self) -> KVCache:
        return KVCache(self.cfg.n_layer, self.cfg.block_size)

    def forward(
        self,
        idx: torch.Tensor,
        targets: torch.Tensor | None = None,
        loss_mask: torch.Tensor | None = None,
        cache: KVCache | None = None,
        last_only: bool = False,
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        """Return (logits, loss).

        - Training/eval: logits are (B, T, V). With targets AND loss_mask, the head
          is applied only to masked positions and logits are the selected rows
          (n_sel, V); loss is the masked mean (identical to the dense computation).
        - cache: decode incrementally; idx holds only the new tokens, positions
          start at cache.length. Cache is advanced by T. Eval use only.
        - last_only: logits for the final position only, (B, 1, V). No targets."""
        B, T = idx.shape
        start = cache.length if cache is not None else 0
        if start + T > self.cfg.block_size:
            raise ValueError(f"sequence length {start + T} > block size {self.cfg.block_size}")
        if last_only and targets is not None:
            raise ValueError("last_only cannot be combined with targets")
        x = self.drop(self.tok_emb(idx))
        cos, sin = _rope_tables(start, T, self.cfg.head_dim, self.cfg.rope_theta, x.device)
        for block in self.blocks:
            x = block(x, cos, sin, cache)
        if cache is not None:
            cache.length += T
        if last_only:
            x = x[:, -1:]
        x = self.norm_f(x)

        if targets is not None and loss_mask is not None:
            sel = loss_mask.reshape(-1).bool()
            h = x.reshape(-1, x.size(-1))[sel]
            tgt = targets.reshape(-1)[sel]
            logits = F.linear(h, self.tok_emb.weight)
            denom = sel.sum().clamp(min=1).to(torch.float32)
            loss = F.cross_entropy(logits.float(), tgt, ignore_index=-100, reduction="sum") / denom
            return logits, loss

        logits = F.linear(x, self.tok_emb.weight)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)), targets.reshape(-1), ignore_index=-100
            )
        return logits, loss

    def configure_optimizer(
        self,
        lr: float,
        weight_decay: float,
        betas: tuple[float, float] = (0.9, 0.95),
    ) -> torch.optim.Optimizer:
        decay, no_decay = [], []
        for n, p in self.named_parameters():
            if not p.requires_grad:
                continue
            if p.dim() >= 2:
                decay.append(p)
            else:
                no_decay.append(p)
        groups = [
            {"params": decay, "weight_decay": weight_decay},
            {"params": no_decay, "weight_decay": 0.0},
        ]
        return make_adamw(groups, lr, betas, next(self.parameters()).device)
