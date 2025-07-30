from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests

app = FastAPI()

BASE_URL = "https://api.tastytrade.com"

# ✅ Login request model
class LoginRequest(BaseModel):
    login: str
    password: str

# ✅ POST /login - Authenticates and returns session token
@app.post("/login")
def login(credentials: LoginRequest):
    url = f"{BASE_URL}/sessions"
    headers = {
        "User-Agent": "tastybot-client/1.0",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=credentials.dict(), headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    token = response.json()["data"]["session-token"]
    return {"session_token": token}

# ✅ GET /accounts - Fetches account info using session token
@app.get("/accounts")
def get_accounts(authorization: str = Header(..., description="Paste your session token here (without 'Bearer ')")):
    url = f"{BASE_URL}/accounts"
    headers = {
        "Authorization": f"Bearer {authorization}",
        "User-Agent": "tastybot-client/1.0",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# ✅ GET / - Friendly homepage
@app.get("/")
def root():
    return {
        "message": "TastyBot backend is live. Use /login to authenticate.",
        "docs": "/docs",
        "redoc": "/redoc"
    }
