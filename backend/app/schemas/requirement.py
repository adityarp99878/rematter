from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequirementCreate(BaseModel):
    buyer_id: int
    material_type: str
    quantity_needed: float
    unit: str = "units"
    max_budget: Optional[float] = None
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: float = 50.0
    deadline: Optional[str] = None
    purpose: Optional[str] = None

class RequirementResponse(BaseModel):
    id: int
    buyer_id: int
    material_type: str
    quantity_needed: float
    unit: str
    max_budget: Optional[float]
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    radius_km: float
    deadline: Optional[str]
    purpose: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
