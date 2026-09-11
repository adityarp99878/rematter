from app.db.database import SessionLocal
from app.models.user import User
from app.models.material import Material, MaterialImage, MaterialAssessment, MaterialPassport
from app.models.requirement import Requirement
from app.models.match import Match
from app.models.notification import Notification
import json


def seed_database():
    db = SessionLocal()
    if db.query(User).first():
        db.close()
        return

    # --- Users ---
    users = [
        User(id=1, name="Arjun Menon", email="demo@materialrebirth.ai", company="Demo Construction Co.", location="Thrissur", verification_status="verified", trust_score=95.0),
        User(id=2, name="Priya Nair", email="greenbuild@example.com", company="GreenBuild School Project", location="Kochi", verification_status="verified", trust_score=90.0),
        User(id=3, name="Rajesh Kumar", email="kerala.builders@example.com", company="Kerala Builders Ltd.", location="Palakkad", verification_status="unverified", trust_score=60.0),
        User(id=4, name="Meera Krishnan", email="eco@example.com", company="Eco Renovators", location="Kozhikode", verification_status="verified", trust_score=85.0),
    ]
    for u in users:
        db.add(u)
    db.commit()

    # --- 12 Materials ---
    materials_data = [
        dict(id=1, seller_id=1, material_type="brick", quantity=2430, unit="units", location="Thrissur", latitude=10.5276, longitude=76.2144, condition="good", reuse_score=92.0, risk_level="low", ai_confidence=0.88, estimated_value=18500.0, carbon_estimate=1900.0, status="available", age="15 years", previous_use="Residential building", description="Reclaimed red clay bricks from traditional Kerala house demolition"),
        dict(id=2, seller_id=3, material_type="steel_beam", quantity=45, unit="units", location="Palakkad", latitude=10.7867, longitude=76.6548, condition="fair", reuse_score=78.0, risk_level="medium", ai_confidence=0.82, estimated_value=125000.0, carbon_estimate=12825.0, status="available", age="20 years", previous_use="Commercial warehouse", description="Steel I-beams from warehouse demolition"),
        dict(id=3, seller_id=4, material_type="wood/door", quantity=12, unit="units", location="Kozhikode", latitude=11.2588, longitude=75.7804, condition="good", reuse_score=85.0, risk_level="low", ai_confidence=0.91, estimated_value=36000.0, carbon_estimate=504.0, status="available", age="25 years", previous_use="Heritage building", description="Teak wood doors with traditional Kerala carvings"),
        dict(id=4, seller_id=2, material_type="window", quantity=24, unit="units", location="Kochi", latitude=9.9312, longitude=76.2673, condition="fair", reuse_score=71.0, risk_level="medium", ai_confidence=0.87, estimated_value=48000.0, carbon_estimate=840.0, status="available", age="12 years", previous_use="Office building", description="Aluminium-framed glass windows"),
        dict(id=5, seller_id=1, material_type="tile", quantity=500, unit="sqft", location="Thrissur", latitude=10.5276, longitude=76.2144, condition="excellent", reuse_score=88.0, risk_level="low", ai_confidence=0.93, estimated_value=15000.0, carbon_estimate=1400.0, status="available", age="10 years", previous_use="Residential flooring", description="Ceramic floor tiles in excellent condition"),
        dict(id=6, seller_id=2, material_type="wood", quantity=200, unit="sqft", location="Kochi", latitude=9.9312, longitude=76.2673, condition="good", reuse_score=91.0, risk_level="low", ai_confidence=0.90, estimated_value=85000.0, carbon_estimate=1040.0, status="available", age="18 years", previous_use="Heritage restoration", description="Premium teak wood planks"),
        dict(id=7, seller_id=3, material_type="concrete", quantity=1500, unit="units", location="Palakkad", latitude=10.7867, longitude=76.6548, condition="fair", reuse_score=65.0, risk_level="medium", ai_confidence=0.85, estimated_value=22000.0, carbon_estimate=195.0, status="available", age="22 years", previous_use="Commercial building", description="Concrete blocks from demolition"),
        dict(id=8, seller_id=1, material_type="pipe", quantity=150, unit="meters", location="Thrissur", latitude=10.5276, longitude=76.2144, condition="good", reuse_score=82.0, risk_level="low", ai_confidence=0.89, estimated_value=45000.0, carbon_estimate=525.0, status="available", age="8 years", previous_use="Plumbing", description="Copper pipes in good condition"),
        dict(id=9, seller_id=4, material_type="roof_tile", quantity=800, unit="units", location="Kozhikode", latitude=11.2588, longitude=75.7804, condition="good", reuse_score=87.0, risk_level="low", ai_confidence=0.92, estimated_value=28000.0, carbon_estimate=960.0, status="available", age="20 years", previous_use="Traditional Kerala roof", description="Clay roof tiles - Mangalore pattern"),
        dict(id=10, seller_id=2, material_type="window", quantity=18, unit="units", location="Kochi", latitude=9.9312, longitude=76.2673, condition="fair", reuse_score=76.0, risk_level="medium", ai_confidence=0.86, estimated_value=54000.0, carbon_estimate=630.0, status="available", age="15 years", previous_use="Residential building", description="Salvaged wooden-frame windows"),
        dict(id=11, seller_id=1, material_type="granite", quantity=100, unit="sqft", location="Thrissur", latitude=10.5276, longitude=76.2144, condition="excellent", reuse_score=94.0, risk_level="low", ai_confidence=0.95, estimated_value=120000.0, carbon_estimate=820.0, status="available", age="12 years", previous_use="Kitchen countertops", description="Black granite slabs - premium quality"),
        dict(id=12, seller_id=3, material_type="bamboo", quantity=300, unit="units", location="Palakkad", latitude=10.7867, longitude=76.6548, condition="good", reuse_score=89.0, risk_level="low", ai_confidence=0.88, estimated_value=18000.0, carbon_estimate=135.0, status="available", age="3 years", previous_use="Scaffolding", description="Treated bamboo poles"),
    ]
    for md in materials_data:
        db.add(Material(**md))
    db.commit()

    # --- Assessments for first 3 ---
    assessments = [
        MaterialAssessment(material_id=1, detections=json.dumps([{"material": "brick", "confidence": 0.95, "count_estimate": 2430}]),
            visible_defects=json.dumps(["minor edge chipping on ~5% of units"]), condition="good", reuse_score=92.0, risk_level="low",
            confidence=0.88, recommendation="reuse", reasoning=json.dumps(["Material appears in good condition", "Minor edge chipping detected", "High demand for reclaimed bricks in Kerala", "Reuse score 92/100 - High reuse potential"])),
        MaterialAssessment(material_id=2, detections=json.dumps([{"material": "steel_beam", "confidence": 0.89, "count_estimate": 45}]),
            visible_defects=json.dumps(["moderate surface corrosion", "minor deformation at connection points"]), condition="fair", reuse_score=78.0, risk_level="medium",
            confidence=0.82, recommendation="verify_then_reuse", reasoning=json.dumps(["Moderate surface corrosion visible", "Structural material - professional verification recommended", "Reuse score 78/100 - Verification recommended"])),
        MaterialAssessment(material_id=3, detections=json.dumps([{"material": "wood/door", "confidence": 0.93, "count_estimate": 12}]),
            visible_defects=json.dumps(["minor edge damage", "slight finish deterioration"]), condition="good", reuse_score=85.0, risk_level="low",
            confidence=0.91, recommendation="reuse", reasoning=json.dumps(["Teak wood in good condition", "Traditional carvings add heritage value", "Minor cosmetic wear only", "Reuse score 85/100 - High reuse potential"])),
    ]
    for a in assessments:
        db.add(a)
    db.commit()

    # --- Passports ---
    passports = [
        MaterialPassport(material_id=1, passport_id="MR-1001", source_building="Traditional Kerala House", previous_use="Residential building", material_grade="A", ai_condition="good", ai_reuse_score=92.0, carbon_estimate=1900.0, verification_status="not_required", lifecycle_stage="listed"),
        MaterialPassport(material_id=2, passport_id="MR-1002", source_building="Commercial Warehouse", previous_use="Commercial warehouse", material_grade="B", ai_condition="fair", ai_reuse_score=78.0, carbon_estimate=12825.0, verification_status="recommended", lifecycle_stage="listed"),
        MaterialPassport(material_id=3, passport_id="MR-1003", source_building="Heritage Building", previous_use="Heritage building", material_grade="A", ai_condition="good", ai_reuse_score=85.0, carbon_estimate=504.0, verification_status="not_required", lifecycle_stage="listed"),
        MaterialPassport(material_id=5, passport_id="MR-1005", source_building="Residential Home", previous_use="Residential flooring", ai_condition="excellent", ai_reuse_score=88.0, carbon_estimate=1400.0, verification_status="not_required", lifecycle_stage="listed"),
        MaterialPassport(material_id=6, passport_id="MR-1006", source_building="Heritage Property", previous_use="Heritage restoration", ai_condition="good", ai_reuse_score=91.0, carbon_estimate=1040.0, verification_status="not_required", lifecycle_stage="listed"),
        MaterialPassport(material_id=11, passport_id="MR-1011", source_building="Premium Residence", previous_use="Kitchen countertops", ai_condition="excellent", ai_reuse_score=94.0, carbon_estimate=820.0, verification_status="not_required", lifecycle_stage="listed"),
    ]
    for p in passports:
        db.add(p)
    db.commit()

    # --- 5 Requirements ---
    reqs = [
        Requirement(id=1, buyer_id=2, material_type="brick", quantity_needed=2000, unit="units", max_budget=25000, location="Kochi", latitude=9.9312, longitude=76.2673, purpose="School construction project"),
        Requirement(id=2, buyer_id=3, material_type="steel_beam", quantity_needed=50, unit="units", max_budget=150000, location="Palakkad", latitude=10.7867, longitude=76.6548, purpose="Commercial building"),
        Requirement(id=3, buyer_id=4, material_type="wood/door", quantity_needed=20, unit="units", max_budget=50000, location="Kozhikode", latitude=11.2588, longitude=75.7804, purpose="Heritage restoration"),
        Requirement(id=4, buyer_id=2, material_type="tile", quantity_needed=300, unit="sqft", max_budget=20000, location="Kochi", latitude=9.9312, longitude=76.2673, purpose="School flooring"),
        Requirement(id=5, buyer_id=1, material_type="wood", quantity_needed=100, unit="sqft", max_budget=100000, location="Thrissur", latitude=10.5276, longitude=76.2144, purpose="Home renovation"),
    ]
    for r in reqs:
        db.add(r)
    db.commit()

    # --- Pre-built match ---
    match1 = Match(
        material_id=1, requirement_id=1, match_score=94.0, quantity_score=95.0,
        quality_score=92.0, distance_score=96.0, price_score=87.0, carbon_score=94.0,
        ai_reasoning="Excellent match: 2430 bricks available for 2000 needed (121% coverage). "
                     "High reuse score of 92/100. Only 66 km apart (Thrissur to Kochi). "
                     "Within budget at ₹18,500 vs ₹25,000 max. "
                     "Reusing these bricks avoids an estimated 1.9 tonnes CO₂e.",
        recommended_price=18500.0, transport_cost=2400.0, transport_distance_km=66.0,
        co2_avoided_kg=1900.0, status="recommended"
    )
    db.add(match1)
    db.commit()

    # --- Notifications ---
    notifs = [
        Notification(user_id=1, title="New Match Found", message="Your reclaimed bricks matched with 3 projects", notification_type="match", reference_id=1, reference_type="material"),
        Notification(user_id=1, title="Buyer Nearby", message="AI found a potential buyer just 12 km away", notification_type="match"),
        Notification(user_id=1, title="Passport Ready", message="Material passport generated for Steel I-Beams", notification_type="passport", reference_id=2, reference_type="material"),
        Notification(user_id=1, title="Requirement Alert", message="New requirement posted matching your ceramic tiles", notification_type="requirement", reference_id=4, reference_type="requirement"),
        Notification(user_id=1, title="Verification Update", message="Professional verification recommended for concrete blocks", notification_type="verification", reference_id=7, reference_type="material"),
    ]
    for n in notifs:
        db.add(n)
    db.commit()

    db.close()
    print("[OK] Demo database seeded: 4 users, 12 materials, 6 passports, 5 requirements, 1 match, 5 notifications")


if __name__ == "__main__":
    from app.db.database import init_db
    init_db()
    seed_database()
