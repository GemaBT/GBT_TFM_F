"""from sqlalchemy.orm import Session
from api.models import AuthLog

def log_event(
    db: Session,
    user_id: int | None,
    action: str,
    status: str,
    ip: str,
    user_agent: str
):
    log = AuthLog(
        user_id=user_id,
        action=action,
        status=status,
        ip_address=ip,
        user_agent=user_agent
    )

    db.add(log)
    db.commit()
    """
from api.models import AuthLog

def log_event(db, user_id, action, status, ip, user_agent):
    log = AuthLog(
        user_id=user_id,
        action=action,
        status=status,
        ip_address=ip,
        user_agent=user_agent
    )
    db.add(log)
    db.commit()