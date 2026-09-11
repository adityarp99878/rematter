from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List, Optional
from app.models.material import Material, MaterialAssessment, MaterialPassport, MaterialImage
from app.schemas.material import MaterialResponse, MaterialAnalyzeResponse, MaterialCreate
from app.agents.orchestrator import Orchestrator
from app.services.storage import StorageService
import json

router = APIRouter(prefix="/api/materials", tags=["materials"])
orchestrator = Orchestrator()
storage = StorageService()


@router.post("/analyze")
async def analyze_material(
    files: List[UploadFile] = File(...),
    material_type: Optional[str] = Form(None),
    quantity: float = Form(0),
    unit: str = Form("units"),
    location: str = Form("Thrissur"),
    age: Optional[str] = Form(None),
    dimensions: Optional[str] = Form(None),
    previous_use: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    # Save uploaded files
    image_paths = []
    for f in files:
        content = await f.read()
        path = storage.save_file(content, f.filename or "upload.jpg", material_id=0)
        image_paths.append(path)

    metadata = {
        "material_type": material_type, "quantity": quantity, "unit": unit,
        "location": location, "age": age, "dimensions": dimensions,
        "previous_use": previous_use, "description": description,
        "latitude": latitude, "longitude": longitude, "seller_id": 1,
    }

    try:
        result = orchestrator.analyze_material(image_paths, metadata, db)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/")
def create_material(mat: MaterialCreate, db: Session = Depends(get_db)):
    m = Material(**mat.model_dump(), seller_id=1, status="draft")
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "material_type": m.material_type, "status": m.status}


@router.get("/")
def get_materials(
    material_type: Optional[str] = None, status: Optional[str] = None,
    min_score: Optional[float] = None, location: Optional[str] = None,
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    query = db.query(Material)
    if material_type:
        query = query.filter(Material.material_type == material_type)
    if status:
        query = query.filter(Material.status == status)
    if min_score:
        query = query.filter(Material.reuse_score >= min_score)
    if location:
        query = query.filter(Material.location.ilike(f"%{location}%"))
    total = query.count()
    materials = query.order_by(Material.created_at.desc()).offset(skip).limit(limit).all()
    result = []
    for m in materials:
        md = {
            "id": m.id, "seller_id": m.seller_id, "material_type": m.material_type,
            "quantity": m.quantity, "unit": m.unit, "location": m.location,
            "latitude": m.latitude, "longitude": m.longitude,
            "condition": m.condition, "reuse_score": m.reuse_score,
            "risk_level": m.risk_level, "ai_confidence": m.ai_confidence,
            "estimated_value": m.estimated_value, "carbon_estimate": m.carbon_estimate,
            "status": m.status, "description": m.description, "age": m.age,
            "dimensions": m.dimensions, "previous_use": m.previous_use,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        # Get images
        images = db.query(MaterialImage).filter(MaterialImage.material_id == m.id).all()
        md["images"] = [{"id": i.id, "image_url": i.image_url} for i in images]
        result.append(md)
    return {"materials": result, "total": total}


@router.get("/{id}")
def get_material(id: int, db: Session = Depends(get_db)):
    m = db.query(Material).filter(Material.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Material not found")
    md = {
        "id": m.id, "seller_id": m.seller_id, "material_type": m.material_type,
        "quantity": m.quantity, "unit": m.unit, "location": m.location,
        "latitude": m.latitude, "longitude": m.longitude,
        "condition": m.condition, "reuse_score": m.reuse_score,
        "risk_level": m.risk_level, "ai_confidence": m.ai_confidence,
        "estimated_value": m.estimated_value, "carbon_estimate": m.carbon_estimate,
        "status": m.status, "description": m.description, "age": m.age,
        "dimensions": m.dimensions, "previous_use": m.previous_use,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }
    images = db.query(MaterialImage).filter(MaterialImage.material_id == m.id).all()
    md["images"] = [{"id": i.id, "image_url": i.image_url} for i in images]
    assessment = db.query(MaterialAssessment).filter(MaterialAssessment.material_id == m.id).first()
    if assessment:
        md["assessment"] = {
            "condition": assessment.condition, "reuse_score": assessment.reuse_score,
            "risk_level": assessment.risk_level, "confidence": assessment.confidence,
            "recommendation": assessment.recommendation,
            "visible_defects": json.loads(assessment.visible_defects) if assessment.visible_defects else [],
            "reasoning": json.loads(assessment.reasoning) if assessment.reasoning else [],
        }
    passport = db.query(MaterialPassport).filter(MaterialPassport.material_id == m.id).first()
    if passport:
        md["passport"] = {
            "passport_id": passport.passport_id, "source_building": passport.source_building,
            "previous_use": passport.previous_use, "material_grade": passport.material_grade,
            "ai_condition": passport.ai_condition, "ai_reuse_score": passport.ai_reuse_score,
            "carbon_estimate": passport.carbon_estimate,
            "verification_status": passport.verification_status,
            "lifecycle_stage": passport.lifecycle_stage,
        }
    # Seller info
    from app.models.user import User
    seller = db.query(User).filter(User.id == m.seller_id).first()
    if seller:
        md["seller"] = {"id": seller.id, "name": seller.name, "company": seller.company, "location": seller.location}
    return md


@router.get("/{id}/passport")
def get_passport(id: int, db: Session = Depends(get_db)):
    m = db.query(Material).filter(Material.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Material not found")
    p = db.query(MaterialPassport).filter(MaterialPassport.material_id == id).first()
    if not p:
        pid = f'MR-{1000 + m.id}'
        is_rej = m.status == 'rejected' or 'rejected' in str(m.condition)
        p = MaterialPassport(
            material_id=m.id, passport_id=pid,
            source_building=m.previous_use or 'Salvage Site',
            previous_use=m.previous_use or 'Demolition Recovery',
            ai_condition=m.condition or 'fair',
            ai_reuse_score=m.reuse_score or 0.0,
            carbon_estimate=m.carbon_estimate or 0.0,
            verification_status='rejected' if is_rej else ('verified' if (m.reuse_score or 0) >= 80 else 'recommended'),
            lifecycle_stage='rejected' if is_rej else 'passport_created'
        )
        db.add(p)
        db.commit()
        db.refresh(p)
    return {
        "passport_id": p.passport_id, "material_id": p.material_id,
        "source_building": p.source_building, "previous_use": p.previous_use,
        "material_grade": p.material_grade, "ai_condition": p.ai_condition,
        "ai_reuse_score": p.ai_reuse_score, "carbon_estimate": p.carbon_estimate,
        "verification_status": p.verification_status, "lifecycle_stage": p.lifecycle_stage,
        "material": {
            "id": m.id, "material_type": m.material_type, "quantity": m.quantity,
            "unit": m.unit, "location": m.location, "condition": m.condition,
            "reuse_score": m.reuse_score, "estimated_value": m.estimated_value,
            "description": m.description, "age": m.age,
        } if m else None
    }


@router.put("/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):
    m = db.query(Material).filter(Material.id == id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Material not found")
    m.status = status
    db.commit()
    return {"status": "success", "new_status": status}
