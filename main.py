from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

BASE_URL = "https://api.tastytrade.com"

# Root route for confirmation
@app.get("/")
def read_root():
    return {
        "message": "TastyBot backend is live. Use /login to authenticate.",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Schema for login credentials
class LoginRequest(BaseModel):
    login: str
    password: str

# POST /login endpoint
@app.post("/login")
def login(credentials: LoginRequest):
    url = f"{BASE_URL}/sessions"
    headers = {
        "User-Agent": "tastybot-client/1.0",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=credentials.dict(), headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    session_token = response.json()["data"].get("session-token")
    if not session_token:
        raise HTTPException(status_code=500, detail="Session token not found in response.")

    return {"session_token": session_token}
