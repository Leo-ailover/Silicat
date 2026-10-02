// Silicat chat client — vanilla JS, fetch + SSE parsing.

const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const statusEl = document.getElementById("status");

const messages = [];
const stopBtn = document.getElementById("stop");
let busy = false;
let ctrl = null;
let apiKey = "";
try { apiKey = sessionStorage.getItem("silicat_api_key") ?? ""; } catch { /* ignore */ }

// ── Conversation persistence ─────────────────────────────────────────────────

const STORAGE_KEY = "silicat_conversations";
const MAX_SAVED = 20;

let currentConvId = newId();

function newId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

function savedConversations() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]"); }
  catch { return []; }
}

function saveCurrentConversation() {
  if (messages.length === 0) return;
  const convs = savedConversations().filter(c => c.id !== currentConvId);
  const title = messages[0]?.content?.slice(0, 60) ?? "Conversation";
  convs.unshift({ id: currentConvId, title, ts: Date.now(), messages: [...messages] });
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(convs.slice(0, MAX_SAVED))); }
  catch { /* quota / blocked storage: keep chatting */ }
  renderRecentList();
}

function loadConversation(id) {
  if (busy) return;
  const conv = savedConversations().find(c => c.id === id);
  if (!conv) return;
  messages.length = 0;
  messages.push(...conv.messages);
  currentConvId = id;
  chat.innerHTML = "";
  for (const m of messages) addMessage(m.role, m.content);
  renderRecentList();
}

function startNewChat() {
  if (busy) return;
  if (messages.length > 0) saveCurrentConversation();
  messages.length = 0;
  currentConvId = newId();
  chat.innerHTML = "";
  renderRecentList();
  input.focus();
}

function formatTs(ts) {
  const diff = Date.now() - ts;
  const days = Math.floor(diff / 86400000);
  if (days === 0) return "Today";
  if (days === 1) return "Yesterday";
  return new Date(ts).toLocaleDateString();
}

function renderRecentList() {
  const list = document.getElementById("recent-list");
  if (!list) return;
  const convs = savedConversations();
  if (convs.length === 0) {
    list.innerHTML = `<p class="no-convs">No saved conversations yet.</p>`;
    return;
  }
  list.innerHTML = convs.map(c => `
    <button class="conv-item${c.id === currentConvId ? " active" : ""}" data-id="${escapeHtml(c.id)}">
      <span class="conv-title">${escapeHtml(c.title)}</span>
      <span class="conv-ts">${formatTs(c.ts)}</span>
    </button>
  `).join("");
  list.querySelectorAll(".conv-item").forEach(btn => {
    btn.addEventListener("click", () => loadConversation(btn.dataset.id));
  });
}

async function refreshHealth() {
  try {
    const r = await fetch("/api/health");
    const h = await r.json();
    if (h.model_loaded) {
      statusEl.textContent =
        `ready · ${h.arch}${h.stage ? "/" + h.stage : ""} · ${h.n_params.toLocaleString()} params · ${h.device} · step ${h.step}`;
      statusEl.className = "status ok";
      const maxEl = document.getElementById("max_new_tokens");
      if (h.max_new_tokens) {
        maxEl.max = h.max_new_tokens;
        if (parseInt(maxEl.value, 10) > h.max_new_tokens) maxEl.value = h.max_new_tokens;
      }
    } else {
      statusEl.textContent = h.error
        ? `model not loaded — ${h.error}`
        : "no checkpoint — train Silicat first";
      statusEl.className = "status err";
    }
  } catch (e) {
    statusEl.textContent = "server unreachable";
    statusEl.className = "status err";
  }
}
refreshHealth();

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderMarkdown(text) {
  // Very small markdown: fenced code blocks (with language label; an unterminated
  // fence is auto-closed while streaming) and inline code. Nothing fancy.
  let t = text;
  if ((t.match(/```/g) || []).length % 2 === 1) t += "\n```";
  let html = escapeHtml(t);
  html = html.replace(/```([\w+-]*)[ \t]*\n?([\s\S]*?)```/g, (_, lang, code) =>
    `<pre${lang ? ` data-lang="${lang}"` : ""}><code>${code}</code></pre>`);
  html = html.replace(/`([^`\n]+)`/g, (_, code) => `<code>${code}</code>`);
  return html;
}

function addMessage(role, text = "") {
  const el = document.createElement("div");
  el.className = `msg ${role}`;
  el.innerHTML = `<div class="who">${role}</div><div class="body"></div>`;
  el.querySelector(".body").innerHTML = renderMarkdown(text);
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
  return el;
}

async function describeError(resp) {
  let detail = "";
  try {
    const j = JSON.parse(await resp.text());
    detail = Array.isArray(j.detail) ? j.detail.map(d => d.msg ?? JSON.stringify(d)).join("; ") : (j.detail ?? "");
  } catch { /* not JSON */ }
  return `HTTP ${resp.status}${detail ? ": " + detail : ""}`;
}

function numOrOmit(id, parse) {
  const v = parse(document.getElementById(id).value);
  return Number.isFinite(v) ? v : undefined;
}

// Returns {text, ok, note}. ok=false when nothing usable arrived.
async function streamReply(replyEl, signal, state) {
  const body = replyEl.querySelector(".body");
  replyEl.classList.add("cursor");

  const params = {
    messages,
    temperature: numOrOmit("temperature", parseFloat),
    top_k: numOrOmit("top_k", v => parseInt(v, 10)),
    top_p: numOrOmit("top_p", parseFloat),
    max_new_tokens: numOrOmit("max_new_tokens", v => parseInt(v, 10)),
  };
  const headers = { "content-type": "application/json", accept: "text/event-stream" };
  if (apiKey) headers.authorization = `Bearer ${apiKey}`;

  const resp = await fetch("/api/chat", { method: "POST", headers, body: JSON.stringify(params), signal });

  if (!resp.ok || !resp.body) {
    if (resp.status === 401) {
      const k = window.prompt("API key required:");
      if (k) { apiKey = k; try { sessionStorage.setItem("silicat_api_key", k); } catch { /* ignore */ } }
    }
    const msg = await describeError(resp);
    body.innerHTML = `<em>${escapeHtml(msg)}</em>`;
    state.error = true;
    return;
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let accumulated = "";
  let sawDone = false, sawError = false, finish = "";

  const handle = (evt) => {
    let event = "message";
    let data = "";
    for (const line of evt.split("\n")) {
      if (line.startsWith("event:")) event = line.slice(6).trim();
      else if (line.startsWith("data:")) data += line.slice(5).trim();
    }
    if (!data) return;
    let payload;
    try { payload = JSON.parse(data); } catch { return; }
    if (event === "token") {
      accumulated += payload.text ?? "";
      state.text = accumulated;
      body.innerHTML = renderMarkdown(accumulated);
      chat.scrollTop = chat.scrollHeight;
    } else if (event === "error") {
      sawError = true;
      state.error = true;
      body.innerHTML = `<em>${escapeHtml(payload.message ?? "error")}</em>`;
    } else if (event === "done") {
      sawDone = true;
      finish = payload.finish_reason ?? "";
      if (payload.truncated) finish += " truncated-prompt";
    }
  };

  // sse-starlette separates events with \r\n\r\n: normalise before splitting.
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer = (buffer + decoder.decode(value, { stream: true })).replace(/\r\n/g, "\n");
    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";
    events.forEach(handle);
  }
  buffer = (buffer + decoder.decode()).replace(/\r\n/g, "\n");
  if (buffer.trim()) handle(buffer);

  let note = "";
  if (finish.includes("length")) note = "reply cut off at the token limit";
  if (finish.includes("truncated-prompt")) note += (note ? "; " : "") + "older messages were dropped to fit the context";
  if (!sawDone && !sawError) note = "stream interrupted";
  if (note && accumulated) {
    body.innerHTML = renderMarkdown(accumulated) + `<div class="note">${escapeHtml(note)}</div>`;
  }
}

function setBusy(b) {
  busy = b;
  sendBtn.disabled = b;
  if (stopBtn) stopBtn.hidden = !b;
  chat.setAttribute("aria-busy", String(b));
  document.getElementById("new-chat-btn")?.toggleAttribute("disabled", b);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (busy || !text) return;
  setBusy(true);
  ctrl = new AbortController();
  const convId = currentConvId;
  input.value = "";

  const userEl = addMessage("user", text);
  messages.push({ role: "user", content: text });
  const reply = addMessage("silicat", "");
  const state = { text: "", error: false };
  let aborted = false;
  try {
    await streamReply(reply, ctrl.signal, state);
  } catch (err) {
    if (err?.name === "AbortError") aborted = true;
    else { state.error = true; reply.querySelector(".body").innerHTML = `<em>${escapeHtml(err?.message ?? err)}</em>`; }
  } finally {
    reply.classList.remove("cursor");
    ctrl = null;
  }
  // partial text (Stop click, interrupted stream) is kept; empty/failed replies are rolled back
  if (convId === currentConvId) {
    if (state.text && !state.error) {
      messages.push({ role: "silicat", content: state.text });
      saveCurrentConversation();
    } else {
      messages.pop();               // never send two user turns in a row
      if (aborted) { userEl.remove(); reply.remove(); }
      if (!input.value) input.value = text;
    }
  }
  setBusy(false);
  input.focus();
});

stopBtn?.addEventListener("click", () => ctrl?.abort());

document.getElementById("new-chat-btn")?.addEventListener("click", startNewChat);

renderRecentList();

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    if (!busy) form.requestSubmit();
  }
});
