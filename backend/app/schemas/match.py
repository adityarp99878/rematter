from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MatchFindRequest(BaseModel):
    requirement_id: int

class MatchResponse(BaseModel):
    id: int
    material_id: int
    requirement_id: int
    match_score: float
    quantity_score: float
    quality_score: float
    distance_score: float
    price_score: float
    carbon_score: float
    ai_reasoning: str
    recommended_price: Optional[float]
    transport_cost: Optional[float]
    transport_distance_km: Optional[float]
    co2_avoided_kg: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
