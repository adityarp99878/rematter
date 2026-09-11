from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.material import Material
from app.models.requirement import Requirement
from app.models.match import Match
from app.models.transaction import Transaction

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    mat_count = db.query(Material).filter(Material.status == 'available').count()
    req_count = db.query(Requirement).filter(Requirement.status == 'active').count()
    match_count = db.query(Match).count()
    reused = db.query(Transaction).filter(Transaction.status == 'completed').count()

    # Aggregate carbon and value
    co2_row = db.query(func.sum(Material.carbon_estimate)).filter(Material.status == 'available').scalar()
    co2_total = round((co2_row or 0) / 1000, 1)  # tonnes

    val_row = db.query(func.sum(Material.estimated_value)).filter(Material.status == 'available').scalar()
    val_total = round(val_row or 0, 0)

    # Recent materials
    recent_mats = db.query(Material).order_by(Material.created_at.desc()).limit(6).all()
    recent_materials = [{
        "id": m.id, "material_type": m.material_type, "quantity": m.quantity,
        "unit": m.unit, "location": m.location, "condition": m.condition,
        "reuse_score": m.reuse_score, "estimated_value": m.estimated_value,
        "status": m.status, "description": m.description
    } for m in recent_mats]

    # Recent matches
    recent_ms = db.query(Match).order_by(Match.created_at.desc()).limit(5).all()
    recent_matches = [{
        "id": m.id, "material_id": m.material_id, "requirement_id": m.requirement_id,
        "match_score": m.match_score, "status": m.status,
        "recommended_price": m.recommended_price
    } for m in recent_ms]

    # AI recommendations
    ai_recs = []
    # Count pending matches per material type
    pending_matches = db.query(Match).filter(Match.status == 'recommended').all()
    if pending_matches:
        ai_recs.append({"type": "match", "message": f"{len(pending_matches)} material(s) have recommended matches waiting for review", "priority": "high"})

    # Check for under-budget requirements
    active_reqs = db.query(Requirement).filter(Requirement.status == 'active').all()
    for req in active_reqs[:2]:
        matching = db.query(Material).filter(
            Material.material_type == req.material_type,
            Material.status == 'available'
        ).count()
        if matching > 0:
            ai_recs.append({
                "type": "opportunity",
                "message": f"{matching} {req.material_type}(s) available for '{req.purpose}'",
                "priority": "medium"
            })

    return {
        "materials_listed": mat_count,
        "active_requirements": req_count,
        "successful_matches": match_count,
        "materials_reused": reused,
        "co2_avoided": co2_total,
        "value_recovered": val_total,
        "recent_materials": recent_materials,
        "recent_matches": recent_matches,
        "ai_recommendations": ai_recs,
    }
