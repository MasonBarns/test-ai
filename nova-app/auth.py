# auth.py
from fastapi import Request

# In-memory user store (for demo purposes only)
active_users = {}

def register_user(email: str):
    if email not in active_users:
        active_users[email] = {"history": []}
    return active_users[email]

def get_user_history(email: str):
    return active_users.get(email, {}).get("history", [])

def save_to_history(email: str, prompt: str, response: str):
    if email in active_users:
        active_users[email]["history"].append({
            "prompt": prompt,
            "response": response
        })
