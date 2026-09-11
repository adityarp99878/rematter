from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.agents.impact_agent import ImpactAgent

router = APIRouter(prefix="/api/impact", tags=["impact"])
agent = ImpactAgent()


class ImpactRequest(BaseModel):
    material_type: str
    quantity: float
    unit: str = "units"
    transport_distance_km: float = 0
    material_value: float = 0
    new_material_cost: float = 0


@router.post("/calculate")
def calculate_impact(req: ImpactRequest):
    result = agent.calculate_impact(
        req.material_type, req.quantity, req.unit,
        req.transport_distance_km, req.material_value, req.new_material_cost
    )
    return {
        "material_type": result.material_type,
        "quantity": result.quantity,
        "unit": result.unit,
        "waste_diverted_kg": result.waste_diverted_kg,
        "waste_diverted_tonnes": result.waste_diverted_tonnes,
        "co2_avoided_kg": result.co2_avoided_kg,
        "co2_avoided_tonnes": result.co2_avoided_tonnes,
        "transport_emissions_kg": result.transport_emissions_kg,
        "net_co2_saved_kg": result.net_co2_saved_kg,
        "economic_savings": result.economic_savings,
        "circularity_score": result.circularity_score,
        "trees_equivalent": result.trees_equivalent,
        "reasoning": result.reasoning,
        "disclaimer": result.disclaimer,
    }
