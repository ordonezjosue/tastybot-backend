from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests

app = FastAPI()

BASE_URL = "https://api.tastytrade.com"

# ✅ Login request model
class LoginRequest(BaseModel):
    login: str
    password: str

# ✅ POST /login
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
    
    return {"session_token": response.json()["data"]["session-token"]}

# ✅ GET /accounts — requires session token header
@app.get("/accounts")
def get_accounts(session_token: str = Header(...)):
    url = f"{BASE_URL}/accounts"
    headers = {
        "Authorization": f"Bearer {session_token}",
        "User-Agent": "tastybot-client/1.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()

# ✅ Optional: Friendly homepage
@app.get("/")
def root():
    return {
        "message": "TastyBot backend is live. Use /login to authenticate.",
        "docs": "/docs",
        "redoc": "/redoc"
    }
