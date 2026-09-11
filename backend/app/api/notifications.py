from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.get("/")
def get_notifications(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user_id).all()

@router.put("/{id}/read")
def mark_notification_read(id: int, db: Session = Depends(get_db)):
    n = db.query(Notification).filter(Notification.id == id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    n.is_read = True
    db.commit()
    return {"status": "success"}
