from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="materials.id")
    match_id: Optional[int] = Field(default=None, foreign_key="matches.id")
    buyer_id: int = Field(foreign_key="users.id")
    seller_id: int = Field(foreign_key="users.id")
    agreed_price: float
    transport_cost: Optional[float] = None
    total_cost: float
    carbon_impact: Optional[float] = None
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
