document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const prompt = document.getElementById("prompt").value;
  const email = document.getElementById("email").value;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ prompt, email })
  });

  const data = await res.json();
  document.getElementById("response").textContent = data.response;
});
