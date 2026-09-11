from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.agents.logistics_agent import LogisticsAgent

router = APIRouter(prefix="/api/logistics", tags=["logistics"])
agent = LogisticsAgent()


class LogisticsRequest(BaseModel):
    source_location: str
    destination_location: str
    material_type: str
    quantity: float
    source_lat: Optional[float] = None
    source_lng: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lng: Optional[float] = None


@router.post("/estimate")
def estimate_logistics(req: LogisticsRequest):
    result = agent.estimate_logistics(
        req.source_location, req.destination_location, req.material_type, req.quantity,
        req.source_lat, req.source_lng, req.dest_lat, req.dest_lng
    )
    return {
        "source_location": result.source_location,
        "destination_location": result.destination_location,
        "direct_distance_km": result.direct_distance_km,
        "total_weight_kg": result.total_weight_kg,
        "recommended_route": result.recommended_route,
        "route_options": [
            {"route_name": r.route_name, "distance_km": r.distance_km,
             "estimated_cost": r.estimated_cost, "estimated_time_hours": r.estimated_time_hours,
             "co2_emissions_kg": r.co2_emissions_kg, "vehicle_type": r.vehicle_type,
             "recommended": r.recommended}
            for r in result.route_options
        ],
        "reasoning": result.reasoning,
    }
