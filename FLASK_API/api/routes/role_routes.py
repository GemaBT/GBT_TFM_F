from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Role, RolePermission, Permission
from api.schemas import RoleCreate, RoleUpdate

router = APIRouter()

# -------------------------------
# Dependencia para obtener DB
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===============================
# RUTAS DE ROLES
# ===============================

# Listar todos los roles
@router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles

# Crear un nuevo rol
@router.post("/roles")
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(name=role.name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# Obtener un rol por ID
@router.get("/roles/{role_id}")
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role no encontrado")
    return role

# Actualizar un rol
@router.put("/roles/{role_id}")
def update_role(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role no encontrado")
    
    role.name = role_data.name
    role.description = role_data.description
    db.commit()
    db.refresh(role)
    return role

# Eliminar un rol
@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role no encontrado")
    db.delete(role)
    db.commit()
    return {"message": "Role eliminado"}