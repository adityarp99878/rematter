from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class VerificationRequest(SQLModel, table=True):
    __tablename__ = "verification_requests"
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="materials.id")
    status: str = Field(default="pending")
    reason: str
    notes: Optional[str] = None
    requested_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
