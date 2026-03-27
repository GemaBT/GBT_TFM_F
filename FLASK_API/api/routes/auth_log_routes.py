from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import AuthLog
from api.schemas import AuthLogCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(AuthLog).all()

@router.post("/logs")
def create_log(log: AuthLogCreate, db: Session = Depends(get_db)):
    new_log = AuthLog(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(AuthLog).filter(AuthLog.id == log_id).first()
    if not log:
        raise HTTPException(404, "Log no encontrado")
    db.delete(log)
    db.commit()
    return {"message": "Log eliminado"}