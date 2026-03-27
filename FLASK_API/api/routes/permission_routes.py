from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Permission
from api.schemas import PermissionCreate, PermissionUpdate

router = APIRouter()

# -------------------------------
# Dependencia DB
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===============================
# RUTAS DE PERMISOS
# ===============================

# Listar permisos
@router.get("/")
def get_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()

# Crear permiso
@router.post("/")
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    new_permission = Permission(
        name=permission.name,
        description=permission.description
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

# Obtener permiso por ID
@router.get("/{permission_id}")
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    perm = db.query(Permission).filter(Permission.id == permission_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return perm

# Actualizar permiso
@router.put("/{permission_id}")
def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: Session = Depends(get_db)
):
    perm = db.query(Permission).filter(Permission.id == permission_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")

    if permission_data.name is not None:
        perm.name = permission_data.name

    if permission_data.description is not None:
        perm.description = permission_data.description

    db.commit()
    db.refresh(perm)
    return perm

# Eliminar permiso
@router.delete("/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    perm = db.query(Permission).filter(Permission.id == permission_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")

    db.delete(perm)
    db.commit()
    return {"message": "Permiso eliminado"}