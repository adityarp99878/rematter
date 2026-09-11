from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    material_id: int
    match_id: Optional[int] = None
    buyer_id: int
    seller_id: int
    agreed_price: float
    transport_cost: Optional[float] = None
    total_cost: float
    carbon_impact: Optional[float] = None

class TransactionResponse(TransactionCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
