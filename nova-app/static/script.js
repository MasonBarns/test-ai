const form = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const chatWindow = document.getElementById("chat-window");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  addBubble(prompt, "user");
  promptInput.value = "";

  addBubble("Nova is thinking...", "nova", true);

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  const data = await res.json();
  removeTyping();
  addBubble(data.response, "nova");
});

function addBubble(text, sender, isTyping = false) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  bubble.textContent = text;
  bubble.dataset.typing = isTyping;
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeTyping() {
  const bubbles = document.querySelectorAll('[data-typing="true"]');
  bubbles.forEach(b => b.remove());
}
