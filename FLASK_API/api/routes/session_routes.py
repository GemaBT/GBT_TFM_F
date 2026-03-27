from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import UserSession
from api.schemas import UserSessionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(UserSession).all()

@router.post("/sessions")
def create_session(session: UserSessionCreate, db: Session = Depends(get_db)):
    new_session = UserSession(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    s = db.query(UserSession).filter(UserSession.id == session_id).first()
    if not s:
        raise HTTPException(404, "Session no encontrada")
    db.delete(s)
    db.commit()
    return {"message": "Session eliminada"}