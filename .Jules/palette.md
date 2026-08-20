## 2025-05-18 - Accessibility in Vanilla JS Chat Interfaces
**Learning:** Chat textareas and interactive buttons (e.g. "+ New chat", send, input prompts, sampling controls) in vanilla JS chat applications often lack explicit ARIA labels and focus-visible indicators, degrading the experience for screen reader and keyboard users.
**Action:** Always provide explicit `aria-label` attributes on primary inputs, submit/action buttons, and form labels, as well as distinct `:focus-visible` outline styles for keyboard focus state visibility.
