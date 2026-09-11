from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Match(SQLModel, table=True):
    __tablename__ = "matches"
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="materials.id")
    requirement_id: int = Field(foreign_key="requirements.id")
    match_score: float
    quantity_score: float
    quality_score: float
    distance_score: float
    price_score: float
    carbon_score: float
    ai_reasoning: str
    recommended_price: Optional[float] = None
    transport_cost: Optional[float] = None
    transport_distance_km: Optional[float] = None
    co2_avoided_kg: Optional[float] = None
    status: str = Field(default="recommended")
    created_at: datetime = Field(default_factory=datetime.utcnow)
