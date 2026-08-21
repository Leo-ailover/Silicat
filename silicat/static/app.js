// Silicat chat client — vanilla JS, fetch + SSE parsing.

const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const statusEl = document.getElementById("status");

const messages = [];

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
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convs.slice(0, MAX_SAVED)));
  renderRecentList();
}

function loadConversation(id) {
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
        `ready · ${h.n_params.toLocaleString()} params · ${h.device} · step ${h.step}`;
      statusEl.className = "status ok";
    } else {
      statusEl.textContent = "no checkpoint — train Silicat first";
      statusEl.className = "status err";
    }
  } catch (e) {
    statusEl.textContent = "server unreachable";
    statusEl.className = "status err";
  }
}
refreshHealth();

function escapeHtml(s) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderMarkdown(text) {
  // Very small markdown: fenced code blocks and inline code. Nothing fancy.
  let html = escapeHtml(text);
  html = html.replace(/```([\s\S]*?)```/g, (_, code) => `<pre><code>${code}</code></pre>`);
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

async function streamReply(replyEl) {
  const body = replyEl.querySelector(".body");
  replyEl.classList.add("cursor");

  const params = {
    messages,
    temperature: parseFloat(document.getElementById("temperature").value),
    top_k: parseInt(document.getElementById("top_k").value, 10),
    top_p: parseFloat(document.getElementById("top_p").value),
    max_new_tokens: parseInt(document.getElementById("max_new_tokens").value, 10),
  };

  const resp = await fetch("/api/chat", {
    method: "POST",
    headers: { "content-type": "application/json", accept: "text/event-stream" },
    body: JSON.stringify(params),
  });

  if (!resp.ok || !resp.body) {
    body.innerHTML = `<em>error: ${resp.status}</em>`;
    replyEl.classList.remove("cursor");
    return "";
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let accumulated = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";
    for (const evt of events) {
      const lines = evt.split("\n");
      let event = "message";
      let data = "";
      for (const line of lines) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        else if (line.startsWith("data:")) data += line.slice(5).trim();
      }
      if (!data) continue;
      let payload;
      try { payload = JSON.parse(data); } catch { continue; }
      if (event === "token") {
        accumulated += payload.text ?? "";
        body.innerHTML = renderMarkdown(accumulated);
        chat.scrollTop = chat.scrollHeight;
      } else if (event === "error") {
        body.innerHTML = `<em>${escapeHtml(payload.message ?? "error")}</em>`;
      }
    }
  }
  replyEl.classList.remove("cursor");
  return accumulated;
}

function updateSendButtonState() {
  if (sendBtn) {
    sendBtn.disabled = !input.value.trim();
  }
}

input.addEventListener("input", updateSendButtonState);

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  sendBtn.disabled = true;

  addMessage("user", text);
  messages.push({ role: "user", content: text });

  const reply = addMessage("silicat", "");
  const replyText = await streamReply(reply);
  if (replyText) {
    messages.push({ role: "silicat", content: replyText });
    saveCurrentConversation();
  }

  updateSendButtonState();
  input.focus();
});

document.getElementById("new-chat-btn")?.addEventListener("click", startNewChat);

renderRecentList();
updateSendButtonState();

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    if (input.value.trim()) {
      form.requestSubmit();
    }
  }
});
