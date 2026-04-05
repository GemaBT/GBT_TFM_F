"""
#from database import SessionLocal
from api.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal() #Abre una conexión a la base de datos
                        # Es como decir: “quiero empezar a trabajar con la DB”
    try:
        yield db        #Entrega esa conexión al endpoint
                        #FastAPI hace magia aquí: pausa la función usa db en el endpoint 
                        #y cuando termina → vuelve aquí

    finally:
        db.close()      # 
"""
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api.database import SessionLocal
from api.models import User
from api.security import SECRET_KEY, ALGORITHM

# 🔹 DB (esto ya lo tenías)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 TOKEN (esto es nuevo)
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# 🔹 USUARIO ACTUAL (esto es lo importante)
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