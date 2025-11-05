const form = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const chatWindow = document.getElementById("chat-window");
const historyList = document.getElementById("history-list");
const userEmail = "clayworley9@gmail.com"; // Replace with dynamic user email

document.getElementById("user-email").textContent = userEmail;

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const prompt = promptInput.value;
  promptInput.value = "";

  addBubble(prompt, "user");

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: userEmail, prompt }),
  });

  const data = await res.json();
  addBubble(data.response, "nova");
  updateHistory(data.history);
});

function addBubble(text, sender) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  bubble.textContent = text;
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function updateHistory(history) {
  historyList.innerHTML = "";
  history.forEach((entry) => {
    const item = document.createElement("li");
    item.textContent = entry.prompt;
    historyList.appendChild(item);
  });
}
