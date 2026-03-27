from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Role, Permission

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ➕ Añadir permiso a un rol
@router.post("/roles/{role_id}/permisos/{permiso_id}")
def add_permission(role_id: int, permiso_id: int, db: Session = Depends(get_db)):
    role = db.get(Role, role_id)
    permiso = db.get(Permission, permiso_id)
    if not role or not permiso:
        raise HTTPException(status_code=404, detail="Rol o permiso no encontrado")
    
    if permiso not in role.permissions:
        role.permissions.append(permiso)
        db.commit()
        return {"message": "Permiso añadido"}
    return {"message": "El permiso ya estaba asignado"}

# ❌ Eliminar permiso de un rol
@router.delete("/roles/{role_id}/permisos/{permiso_id}")
def remove_permission(role_id: int, permiso_id: int, db: Session = Depends(get_db)):
    role = db.get(Role, role_id)
    permiso = db.get(Permission, permiso_id)
    if not role or not permiso:
        raise HTTPException(status_code=404, detail="Rol o permiso no encontrado")
    
    if permiso in role.permissions:
        role.permissions.remove(permiso)
        db.commit()
        return {"message": "Permiso eliminado"}
    return {"message": "El permiso no estaba asignado"}