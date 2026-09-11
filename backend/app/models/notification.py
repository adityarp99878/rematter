from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    title: str
    message: str
    notification_type: str = Field(default="info")
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
