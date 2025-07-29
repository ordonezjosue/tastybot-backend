from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

BASE_URL = "https://api.tastytrade.com"

# ✅ Step 1: Define the correct request schema
class LoginRequest(BaseModel):
    login: str
    password: str

# ✅ Step 2: Use that schema in your POST endpoint
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
