import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import {
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

// 🔐 Firebase config (replace with yours)
const firebaseConfig = {
  apiKey: "AIzaSyDkJ0ZxgYQZkJH8xFZkJH8xFZkJH8xFZkJH8",
  authDomain: "test.firebaseapp.com",
  projectId: "test",
  appId: "1:107141014701:web:2b2e3e7f3e2e2e2e2e2e2e"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// 🌐 DOM Elements
const loginBtn = document.getElementById("login-btn");
const userInfoEl = document.getElementById("user-info");
const chatForm = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const chatLog = document.getElementById("chat-log");
const chatListEl = document.getElementById("chat-list");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const searchResultEl = document.getElementById("search-result");

let currentUser = null;

// 🔐 Login
loginBtn.addEventListener("click", async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    currentUser = result.user;
  } catch (err) {
    alert("Login failed: " + err.message);
  }
});

// 🔄 Auth state
onAuthStateChanged(auth, (user) => {
  currentUser = user || null;
  if (user) {
    loginBtn.style.display = "none";
    userInfoEl.textContent = `Welcome, ${user.displayName}`;
    chatForm.style.display = "flex";
    loadChats();
  } else {
    loginBtn.style.display = "block";
    userInfoEl.textContent = "";
    chatForm.style.display = "none";
    chatListEl.innerHTML = "";
    chatLog.innerHTML = "";
  }
});

// 📚 Load recent chats
async function loadChats() {
  if (!currentUser) return;
  const res = await fetch(`/api/chats?user_id=${encodeURIComponent(currentUser.uid)}`);
  const data = await res.json();
  chatListEl.innerHTML = "";
  data.items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item.prompt.slice(0, 60);
    li.title = item.created_at;
    li.addEventListener("click", () => {
      renderChat(item.prompt, item.response);
    });
    chatListEl.appendChild(li);
  });
}

// 💬 Chat submit
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!currentUser) return alert("Please sign in first.");
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  renderTyping();
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      prompt,
      user_id: currentUser.uid,
      email: currentUser.email || ""
    })
  });
  const data = await res.json();
  renderChat(prompt, data.response);
  promptInput.value = "";
  loadChats();
});

// 🔍 Search submit
searchForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = searchInput.value.trim();
  if (!q) return;
  searchResultEl.textContent = "Searching...";
  const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  if (data.summary && data.url) {
    searchResultEl.innerHTML = `<strong>${data.title}</strong><br>${data.summary}<br><a href="${data.url}" target="_blank">Source</a>`;
  } else {
    searchResultEl.textContent = data.summary || "No result.";
  }
});

// 🧠 Render chat
function renderChat(prompt, response) {
  chatLog.innerHTML = `
    <div class="bubble user">🧑 You: ${prompt}</div>
    <div class="bubble nova">✨ Nova: ${response}</div>
  `;
}

// ⏳ Typing animation
function renderTyping() {
  chatLog.innerHTML = `
    <div class="bubble user">🧑 You: ${promptInput.value}</div>
    <div class="bubble nova">✨ Nova is thinking...</div>
  `;
}
