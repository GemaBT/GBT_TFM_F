from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import User
from api.schemas import UserCreate, UserUpdate, PasswordUpdate,UserLogin
from api.security import hash_password, verify_password, create_access_token, create_refresh_token
from api.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
   
# Listar usuarios
"""
# sin comprobar el ID --> BOLA
@router.get("/usuarios/")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 AQUÍ
):
    return db.query(User).all()
"""
@router.get("/usuarios/")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 🔹 Admin → ve todos
    if current_user.role_id == 1:
        return db.query(User).all()

    # 🔹 Usuario normal → solo él mismo
    return [current_user]  # devolvemos una lista con su propio usuario

#Crear usuario.- 1 admin 2-user normal
@router.post("/registro/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        #password_hash=user.password,  # sin hash todavía
        password_hash=hash_password(user.password), 
        role_id=user.role_id,         
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Login token
#@router.post("/usuarios/login")
@router.post("/token/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    token_data = {
        "user_id": db_user.id,
        "username": db_user.username,
        "role_id": db_user.role_id, #primer cambio
    }
    
    # token = create_token(token_data)
    # return {"access_token": token, "token_type": "bearer"}

    return { # NUEVO
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer"
    }


# Obtener usuario por ID
"""
# sin comprobar el ID --> BOLA
@router.get("/usuarios/{user_id}/")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
"""
@router.get("/usuarios/{user_id}/")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Solo permite si eres admin o si es tu propio ID
    if current_user.role_id == 1 or current_user.id == user_id:
        return user

    raise HTTPException(status_code=403, detail="No autorizado")

#Actualizar contraseña
"""
# sin comprobar el ID --> BOLA
@router.put("/usuarios/{user_id}/password/")
def change_password(user_id: int, password_data: PasswordUpdate, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar contraseña actual
    if not verify_password(password_data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    # Nueva contraseña hasheada (Argon2)
    user.password_hash = hash_password(password_data.new_password)

    db.commit()

    return {"msg": "Contraseña actualizada correctamente"}
"""
@router.put("/usuarios/{user_id}/password/")
def change_password(user_id: int, password_data: PasswordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(password_data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    user.password_hash = hash_password(password_data.new_password)
    db.commit()
    
    return {"msg": "Contraseña actualizada correctamente"}

# Actualizar usuario. Tengo que cambiar los dos datos a la vez
"""
# sin comprobar el ID --> BOLA
@router.put("/usuarios/{user_id}/")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.username = user_data.username
    user.email = user_data.email
    db.commit()
    db.refresh(user)
    return user
"""
@router.put("/usuarios/{user_id}/")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.username = user_data.username
    user.email = user_data.email
    db.commit()
    db.refresh(user)
    return user

# Eliminar usuario
"""
# sin comprobar el ID --> BOLA
@router.delete("/usuarios/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado"}
"""
@router.delete("/usuarios/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado"}

