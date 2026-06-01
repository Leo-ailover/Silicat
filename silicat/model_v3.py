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
  - Weight tying between token embedding and the output head

Still small and readable; still one file.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


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


def _build_rope(head_dim: int, max_seq: int, theta: float, device=None):
    """Return (cos, sin) tables of shape (max_seq, head_dim)."""
    inv_freq = 1.0 / (theta ** (torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim))
    t = torch.arange(max_seq, dtype=torch.float32)
    freqs = torch.outer(t, inv_freq)          # (max_seq, head_dim/2)
    emb = torch.cat([freqs, freqs], dim=-1)   # (max_seq, head_dim)
    return emb.cos(), emb.sin()


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    half = x.shape[-1] // 2
    x1, x2 = x[..., :half], x[..., half:]
    return torch.cat([-x2, x1], dim=-1)


def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    # x: (B, n_head, T, head_dim); cos/sin: (T, head_dim)
    cos = cos.unsqueeze(0).unsqueeze(0)
    sin = sin.unsqueeze(0).unsqueeze(0)
    return (x * cos) + (_rotate_half(x) * sin)


class Attention(nn.Module):
    def __init__(self, cfg: GPTConfigV3, use_rope: bool):
        super().__init__()
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

    def forward(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
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

        if self.use_rope:
            q = _apply_rope(q, cos[:T], sin[:T])
            k = _apply_rope(k, cos[:T], sin[:T])

        y = F.scaled_dot_product_attention(
            q, k, v,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=True,
            enable_gqa=True,
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
        self.attn = Attention(cfg, use_rope=use_rope)
        self.mlp_norm = RMSNorm(cfg.n_embd, eps=cfg.norm_eps)
        self.mlp = SwiGLU(cfg)

    def forward(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.attn_norm(x), cos, sin)
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
        self.head = nn.Linear(cfg.n_embd, cfg.vocab_size, bias=False)
        self.head.weight = self.tok_emb.weight  # weight tying

        cos, sin = _build_rope(cfg.head_dim, cfg.block_size, cfg.rope_theta)
        self.register_buffer("rope_cos", cos, persistent=False)
        self.register_buffer("rope_sin", sin, persistent=False)

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

    def num_params(self) -> int:
        # subtract tied head (shares tok_emb) to report unique params
        n = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return n

    def forward(
        self,
        idx: torch.Tensor,
        targets: torch.Tensor | None = None,
        loss_mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        B, T = idx.shape
        assert T <= self.cfg.block_size, f"sequence length {T} > block size {self.cfg.block_size}"
        x = self.drop(self.tok_emb(idx))
        cos = self.rope_cos.to(x.device)
        sin = self.rope_sin.to(x.device)
        for block in self.blocks:
            x = block(x, cos, sin)
        x = self.norm_f(x)
        logits = self.head(x)

        loss = None
        if targets is not None:
            per_tok = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.view(-1),
                ignore_index=-100,
                reduction="none",
            )
            if loss_mask is not None:
                mask = loss_mask.view(-1).to(per_tok.dtype)
                denom = mask.sum().clamp(min=1.0)
                loss = (per_tok * mask).sum() / denom
            else:
                loss = per_tok.mean()
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
        return torch.optim.AdamW(groups, lr=lr, betas=betas)
