from fastapi import FastAPI, Request, HTTPException, Depends #nuevo
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import uuid

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

def create_access_token(data: dict):
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=30)  # 🔹 OWASP recomienda 15-30 min

    to_encode.update({
        "exp": int(expire.timestamp()),   # expiración
        "iat": int(now.timestamp()),      # issued at
        "jti": str(uuid.uuid4()),         # identificador único del token
        "token_type": "access"            # tipo de token
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# refresh token
def create_refresh_token(data: dict):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=7)

    to_encode = data.copy()
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": str(uuid.uuid4()),
        "token_type": "refresh"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

"""def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": int(expire.timestamp())})  # <-- importante
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
"""



def verify_token(token: str): #https
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload