from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    company: Optional[str] = None
    location: Optional[str] = None
    verification_status: str = Field(default="unverified")
    trust_score: float = Field(default=50.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
