from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.match import MatchFindRequest
from app.models.match import Match
from app.models.material import Material, MaterialPassport
from app.models.requirement import Requirement
from app.agents.orchestrator import Orchestrator
import json

router = APIRouter(prefix="/api/matches", tags=["matches"])
orchestrator = Orchestrator()


@router.post("/find")
def find_matches(req: MatchFindRequest, db: Session = Depends(get_db)):
    try:
        result = orchestrator.find_best_matches(req.requirement_id, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match finding failed: {str(e)}")


@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).order_by(Match.match_score.desc()).all()
    result = []
    for m in matches:
        md = {
            "id": m.id, "material_id": m.material_id, "requirement_id": m.requirement_id,
            "match_score": m.match_score, "quantity_score": m.quantity_score,
            "quality_score": m.quality_score, "distance_score": m.distance_score,
            "price_score": m.price_score, "carbon_score": m.carbon_score,
            "ai_reasoning": m.ai_reasoning, "recommended_price": m.recommended_price,
            "transport_cost": m.transport_cost, "transport_distance_km": m.transport_distance_km,
            "co2_avoided_kg": m.co2_avoided_kg, "status": m.status,
        }
        mat = db.query(Material).filter(Material.id == m.material_id).first()
        if mat:
            md["material"] = {"id": mat.id, "material_type": mat.material_type, "quantity": mat.quantity,
                              "unit": mat.unit, "location": mat.location, "condition": mat.condition,
                              "reuse_score": mat.reuse_score, "estimated_value": mat.estimated_value}
        req = db.query(Requirement).filter(Requirement.id == m.requirement_id).first()
        if req:
            md["requirement"] = {"id": req.id, "material_type": req.material_type,
                                 "quantity_needed": req.quantity_needed, "max_budget": req.max_budget,
                                 "location": req.location, "purpose": req.purpose}
        result.append(md)
    return {"matches": result, "total": len(result)}


@router.get("/{id}")
def get_match(id: int, db: Session = Depends(get_db)):
    m = db.query(Match).filter(Match.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Match not found")

    md = {
        "id": m.id, "material_id": m.material_id, "requirement_id": m.requirement_id,
        "match_score": m.match_score, "quantity_score": m.quantity_score,
        "quality_score": m.quality_score, "distance_score": m.distance_score,
        "price_score": m.price_score, "carbon_score": m.carbon_score,
        "ai_reasoning": m.ai_reasoning, "recommended_price": m.recommended_price,
        "transport_cost": m.transport_cost, "transport_distance_km": m.transport_distance_km,
        "co2_avoided_kg": m.co2_avoided_kg, "status": m.status,
    }

    # Material with full info
    mat = db.query(Material).filter(Material.id == m.material_id).first()
    if mat:
        md["material"] = {
            "id": mat.id, "material_type": mat.material_type, "quantity": mat.quantity,
            "unit": mat.unit, "location": mat.location, "condition": mat.condition,
            "reuse_score": mat.reuse_score, "estimated_value": mat.estimated_value,
            "carbon_estimate": mat.carbon_estimate, "description": mat.description,
            "age": mat.age, "seller_id": mat.seller_id,
        }
        # Get seller
        from app.models.user import User
        seller = db.query(User).filter(User.id == mat.seller_id).first()
        if seller:
            md["seller"] = {"id": seller.id, "name": seller.name, "company": seller.company}

    # Requirement with full info
    req = db.query(Requirement).filter(Requirement.id == m.requirement_id).first()
    if req:
        md["requirement"] = {
            "id": req.id, "material_type": req.material_type,
            "quantity_needed": req.quantity_needed, "unit": req.unit,
            "max_budget": req.max_budget, "location": req.location,
            "purpose": req.purpose, "buyer_id": req.buyer_id,
        }
        from app.models.user import User
        buyer = db.query(User).filter(User.id == req.buyer_id).first()
        if buyer:
            md["buyer"] = {"id": buyer.id, "name": buyer.name, "company": buyer.company}

    # Run pricing, logistics, impact for this match on the fly
    from app.agents.pricing_agent import PricingAgent
    from app.agents.logistics_agent import LogisticsAgent
    from app.agents.impact_agent import ImpactAgent
    from app.agents.second_life_agent import SecondLifeAgent

    if mat:
        pricing = PricingAgent().estimate_price(mat.material_type, mat.condition or 'good', mat.quantity, mat.age or '', mat.location, mat.unit)
        md["pricing"] = {
            "new_material_price": pricing.new_material_price, "new_material_total": pricing.new_material_total,
            "recommended_price": pricing.recommended_price, "price_range_min": pricing.price_range_min,
            "price_range_max": pricing.price_range_max, "buyer_savings": pricing.buyer_savings,
            "buyer_savings_percent": pricing.buyer_savings_percent, "per_unit_price": pricing.per_unit_price,
            "reasoning": pricing.reasoning,
        }

    if mat and req:
        logistics = LogisticsAgent().estimate_logistics(mat.location, req.location, mat.material_type,
                                                         min(mat.quantity, req.quantity_needed),
                                                         mat.latitude, mat.longitude, req.latitude, req.longitude)
        md["logistics"] = {
            "direct_distance_km": logistics.direct_distance_km, "total_weight_kg": logistics.total_weight_kg,
            "recommended_route": logistics.recommended_route,
            "route_options": [{"route_name": r.route_name, "distance_km": r.distance_km,
                               "estimated_cost": r.estimated_cost, "estimated_time_hours": r.estimated_time_hours,
                               "co2_emissions_kg": r.co2_emissions_kg, "vehicle_type": r.vehicle_type,
                               "recommended": r.recommended} for r in logistics.route_options],
            "reasoning": logistics.reasoning,
        }

        impact = ImpactAgent().calculate_impact(mat.material_type, min(mat.quantity, req.quantity_needed), mat.unit,
                                                 logistics.direct_distance_km, mat.estimated_value or 0, pricing.new_material_total)
        md["impact"] = {
            "waste_diverted_kg": impact.waste_diverted_kg, "waste_diverted_tonnes": impact.waste_diverted_tonnes,
            "co2_avoided_kg": impact.co2_avoided_kg, "co2_avoided_tonnes": impact.co2_avoided_tonnes,
            "transport_emissions_kg": impact.transport_emissions_kg, "net_co2_saved_kg": impact.net_co2_saved_kg,
            "economic_savings": impact.economic_savings, "circularity_score": impact.circularity_score,
            "trees_equivalent": impact.trees_equivalent, "reasoning": impact.reasoning,
            "disclaimer": impact.disclaimer,
        }

        sl = SecondLifeAgent().suggest_uses(mat.material_type, mat.condition or 'good')
        md["second_life"] = [{"use_case": s.use_case, "suitability_score": s.suitability_score,
                              "description": s.description, "category": s.category} for s in sl]

    return md
