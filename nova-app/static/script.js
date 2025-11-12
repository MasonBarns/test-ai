import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

// Replace with your Firebase web config (from your console)
const firebaseConfig = {
  apiKey: "AIzaSyDkJ0ZxgYQZkJH8xFZkJH8xFZkJH8xFZkJH8", // from your screenshot
  authDomain: "test.firebaseapp.com",
  projectId: "test",
  appId: "1:107141014701:web:2b2e3e7f3e2e2e2e2e2e2e"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Elements
const loginBtn = document.getElementById("login-btn");
const userInfoEl = document.getElementById("user-info");
const chatForm = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const responseEl = document.getElementById("response");
const chatListEl = document.getElementById("chat-list");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const searchResultEl = document.getElementById("search-result");

let currentUser = null;

loginBtn.addEventListener("click", async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    currentUser = result.user;
  } catch (e) {
    alert("Login failed: " + e.message);
  }
});

onAuthStateChanged(auth, (user) => {
  currentUser = user || null;
  if (user) {
    loginBtn.style.display = "none";
    userInfoEl.textContent = `${user.displayName} (${user.email})`;
    chatForm.style.display = "flex";
    loadChats();
  } else {
    loginBtn.style.display = "block";
    userInfoEl.textContent = "";
    chatForm.style.display = "none";
    chatListEl.innerHTML = "";
    responseEl.textContent = "";
  }
});

// Load recent chats
async function loadChats() {
  if (!currentUser) return;
  const url = `/api/chats?user_id=${encodeURIComponent(currentUser.uid)}`;
  const res = await fetch(url);
  const data = await res.json();
  chatListEl.innerHTML = "";
  for (const item of data.items) {
    const li = document.createElement("li");
    li.textContent = item.prompt.slice(0, 60);
    li.title = item.created_at;
    li.addEventListener("click", () => {
      responseEl.textContent = `You: ${item.prompt}\n\nNova: ${item.response}`;
    });
    chatListEl.appendChild(li);
  }
}

// Chat submit
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!currentUser) return alert("Please sign in first.");
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  responseEl.textContent = "Thinking...";
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
  responseEl.textContent = data.response;
  promptInput.value = "";
  loadChats();
});

// Search submit
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
