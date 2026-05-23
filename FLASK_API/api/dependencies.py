
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api.database import SessionLocal
from api.models import User
from api.security import SECRET_KEY, ALGORITHM
from api.security import verify_token #https

def get_db():
    db = SessionLocal() #Abre una conexión a la base de datos
                        # Es como decir: “quiero empezar a trabajar con la DB”
    try:
        yield db #Entrega esa conexión al endpoint
                        #FastAPI hace magia aquí: pausa la función usa db en el endpoint 
                        #y cuando termina → vuelve aquí
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

from fastapi import Request
from api.utils.logging import log_event

"""def get_current_user( #http
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            log_event(db, None, "invalid_token", "401", ip, user_agent)
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        log_event(db, None, "invalid_token", "401", ip, user_agent)
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        log_event(db, None, "user_not_found", "404", ip, user_agent)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

""" #https
def get_current_user(request: Request, db: Session = Depends(get_db)): 

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    payload = verify_token(token)

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no válido")

    return user
"""
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

"""

# -------
"""

from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from api.database import SessionLocal
from api.models import User
from api.security import SECRET_KEY, ALGORITHM


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    request: Request,  # 👈 añadimos Request
    db: Session = Depends(get_db)
):
    token = None

    # 🔹 1. Intentar obtener token desde cookie (frontend)
    token = request.cookies.get("access_token")

    # 🔹 2. Si no hay cookie, buscar en header (Postman)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    # 🔹 3. Si no hay token en ningún sitio
    if not token:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    # 🔹 4. Decodificar JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # 🔹 5. Buscar usuario en BD
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
"""