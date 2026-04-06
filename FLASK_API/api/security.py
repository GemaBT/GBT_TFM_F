from fastapi import FastAPI, Request, HTTPException, Depends #nuevo
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": int(expire.timestamp())})  # <-- importante
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
"""
#función para obtener el token NUEVO
def get_token(request: Request) -> str:
    # 1. intenta desde la cookie
    token = request.cookies.get("access_token")
    if token:
        return token
    
    #2. Intenta dede header Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer"):
        token = auth_header.split(" ")[1]
        return token
"""