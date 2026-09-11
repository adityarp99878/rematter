from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Requirement(SQLModel, table=True):
    __tablename__ = "requirements"
    id: Optional[int] = Field(default=None, primary_key=True)
    buyer_id: int = Field(foreign_key="users.id")
    material_type: str
    quantity_needed: float
    unit: str = Field(default="units")
    max_budget: Optional[float] = None
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: float = Field(default=50.0)
    deadline: Optional[str] = None
    purpose: Optional[str] = None
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
