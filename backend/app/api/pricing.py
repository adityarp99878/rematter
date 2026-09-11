from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.agents.pricing_agent import PricingAgent

router = APIRouter(prefix="/api/pricing", tags=["pricing"])
agent = PricingAgent()


class PricingRequest(BaseModel):
    material_type: str
    condition: str = "good"
    quantity: float = 1
    age: str = ""
    location: str = ""
    unit: str = "units"


@router.post("/estimate")
def estimate_price(req: PricingRequest):
    result = agent.estimate_price(req.material_type, req.condition, req.quantity, req.age, req.location, req.unit)
    return {
        "new_material_price": result.new_material_price,
        "new_material_total": result.new_material_total,
        "recommended_price": result.recommended_price,
        "price_range_min": result.price_range_min,
        "price_range_max": result.price_range_max,
        "buyer_savings": result.buyer_savings,
        "buyer_savings_percent": result.buyer_savings_percent,
        "per_unit_price": result.per_unit_price,
        "reasoning": result.reasoning,
    }
