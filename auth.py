# auth.py
from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from models import User

users_db = {}

router = APIRouter()

@router.post("/signup")
def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = bcrypt.hash(user.password)
    return {"message": "User created"}

@router.post("/login")
def login(user: User):
    if user.email not in users_db or not bcrypt.verify(user.password, users_db[user.email]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
