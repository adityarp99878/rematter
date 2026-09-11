import json
from dataclasses import dataclass, asdict
from datetime import datetime
from .base_agent import BaseAgent
from .material_assessment_agent import MaterialAssessmentAgent
from .matching_agent import MatchingAgent
from .pricing_agent import PricingAgent
from .logistics_agent import LogisticsAgent
from .impact_agent import ImpactAgent
from .second_life_agent import SecondLifeAgent
from app.vision.yolo_service import get_vision_service
from app.models.material import Material, MaterialImage, MaterialAssessment, MaterialPassport
from app.models.match import Match
from app.models.requirement import Requirement
from app.models.notification import Notification


@dataclass
class AgentActivityStep:
    agent: str
    status: str
    message: str
    timestamp: str
    duration_ms: int = 0


class Orchestrator(BaseAgent):
    """Central orchestrator coordinating all AI agents."""

    def __init__(self):
        super().__init__()
        self.assessment_agent = MaterialAssessmentAgent()
        self.matching_agent = MatchingAgent()
        self.pricing_agent = PricingAgent()
        self.logistics_agent = LogisticsAgent()
        self.impact_agent = ImpactAgent()
        self.second_life_agent = SecondLifeAgent()
        self.vision_service = get_vision_service()

    def _step(self, agent, msg, ms=200):
        return AgentActivityStep(agent, 'success', msg, datetime.utcnow().isoformat(), ms)

    def analyze_material(self, image_paths: list, metadata: dict, db_session) -> dict:
        activity = []
        user_hint = metadata.get('material_type')

        activity.append(self._step('Upload Agent', f'Received {len(image_paths)} photo(s)', 150))

        vision = self.vision_service.detect(image_paths, material_type_hint=user_hint)
        activity.append(self._step('Vision Agent', f'Analyzed {vision.image_count} images with {vision.model_used}', 800))

        det = vision.detections[0] if vision.detections else None
        if det:
            mt = det.material
            activity.append(self._step('Vision Agent', f'Detected {det.material} ({det.confidence:.0%} confidence, ~{det.count_estimate} units)', 200))
            if not metadata.get('quantity') and det.count_estimate:
                metadata['quantity'] = det.count_estimate
        else:
            mt = user_hint or 'brick'

        det_data = [{'material': d.material, 'confidence': d.confidence, 'count_estimate': d.count_estimate} for d in vision.detections]
        
        is_non_construction = det and not getattr(det, 'is_construction', True)
        if is_non_construction:
            from app.agents.material_assessment_agent import AssessmentResult
            assessment = AssessmentResult(
                material=mt,
                quantity=1.0,
                condition='rejected_non_construction',
                visible_defects=[f"Non-construction item detected: {mt.capitalize()}", "Not eligible for salvaged building material reuse"],
                reuse_score=0.0,
                risk_level='high',
                confidence=det.confidence,
                recommendation='rejected',
                verification_required=False,
                reasoning=[
                    f"Computer vision model detected '{mt}' with {det.confidence:.0%} confidence.",
                    "Material Rebirth AI only accepts circular construction materials (brick, steel, wood, concrete, tile, glass)."
                ],
                safety_disclaimer="Intake audit failed: rejected non-construction item."
            )
            activity.append(self._step('Assessment Agent', f'Item rejected: detected non-construction object ({mt})', 400))
        else:
            assessment = self.assessment_agent.assess(det_data, mt, metadata, image_paths=image_paths)
            activity.append(self._step('Assessment Agent', f'Condition: {assessment.condition}, {len(assessment.visible_defects)} defect(s)', 600))
            activity.append(self._step('Assessment Agent', f'Reuse score: {assessment.reuse_score}/100 — {"High" if assessment.reuse_score >= 80 else "Moderate"} potential', 300))

        qty = float(metadata.get('quantity', assessment.quantity))
        status = 'rejected' if is_non_construction else 'available'
        material = Material(
            seller_id=metadata.get('seller_id', 1), material_type=mt,
            quantity=qty, unit=metadata.get('unit', 'units'),
            age=metadata.get('age'), dimensions=metadata.get('dimensions'),
            previous_use=metadata.get('previous_use'),
            location=metadata.get('location', 'Thrissur'),
            latitude=metadata.get('latitude'), longitude=metadata.get('longitude'),
            condition=assessment.condition, reuse_score=assessment.reuse_score,
            risk_level=assessment.risk_level, ai_confidence=assessment.confidence,
            estimated_value=0, carbon_estimate=0, status=status,
            description=metadata.get('description'))
        db_session.add(material)
        db_session.flush()

        for p in image_paths:
            db_session.add(MaterialImage(material_id=material.id, image_url=p))

        db_session.add(MaterialAssessment(
            material_id=material.id, detections=json.dumps(det_data),
            visible_defects=json.dumps(assessment.visible_defects),
            condition=assessment.condition, reuse_score=assessment.reuse_score,
            risk_level=assessment.risk_level, confidence=assessment.confidence,
            recommendation=assessment.recommendation, reasoning=json.dumps(assessment.reasoning)))

        pricing = self.pricing_agent.estimate_price(mt, assessment.condition, qty, metadata.get('age', ''), metadata.get('location', ''), metadata.get('unit', 'units'))
        material.estimated_value = pricing.recommended_price
        activity.append(self._step('Pricing Agent', f'Value: \u20b9{pricing.recommended_price:,.0f} (saves \u20b9{pricing.buyer_savings:,.0f})', 400))

        impact = self.impact_agent.calculate_impact(mt, qty, metadata.get('unit', 'units'))
        material.carbon_estimate = impact.co2_avoided_kg
        activity.append(self._step('Impact Agent', f'{impact.waste_diverted_tonnes:.1f}t waste diverted, {impact.co2_avoided_tonnes:.1f}t CO\u2082e avoided', 350))

        pid = f'MR-{1000 + material.id}'
        if not is_non_construction:
            passport = MaterialPassport(
                material_id=material.id, passport_id=pid,
                source_building=metadata.get('previous_use', 'Unknown'),
                previous_use=metadata.get('previous_use'),
                ai_condition=assessment.condition, ai_reuse_score=assessment.reuse_score,
                carbon_estimate=impact.co2_avoided_kg,
                verification_status='recommended' if assessment.verification_required else 'not_required',
                lifecycle_stage='passport_created')
            db_session.add(passport)
            material.status = 'available'
            activity.append(self._step('Passport Agent', f'Passport {pid} generated', 250))
        else:
            material.status = 'rejected'
            passport = None
            activity.append(self._step('Intake Agent', 'Item flagged and rejected: not eligible for circular passport', 200))

        sl = self.second_life_agent.suggest_uses(mt, assessment.condition)
        if sl:
            activity.append(self._step('Second Life Agent', f'{len(sl)} reuse applications identified', 200))
        activity.append(self._step('Orchestrator', 'Analysis complete.', 100))

        db_session.commit()
        db_session.refresh(material)

        return {
            'material_id': material.id,
            'material': {'id': material.id, 'material_type': mt, 'quantity': qty, 'unit': material.unit,
                         'location': material.location, 'condition': material.condition,
                         'reuse_score': material.reuse_score, 'risk_level': material.risk_level,
                         'ai_confidence': material.ai_confidence, 'estimated_value': material.estimated_value,
                         'carbon_estimate': material.carbon_estimate, 'status': material.status},
            'assessment': {'condition': assessment.condition, 'visible_defects': assessment.visible_defects,
                           'reuse_score': assessment.reuse_score, 'risk_level': assessment.risk_level,
                           'confidence': assessment.confidence, 'recommendation': assessment.recommendation,
                           'verification_required': assessment.verification_required,
                           'reasoning': assessment.reasoning, 'safety_disclaimer': assessment.safety_disclaimer},
            'passport': {'passport_id': pid, 'verification_status': passport.verification_status, 'lifecycle_stage': passport.lifecycle_stage} if passport else {'passport_id': pid, 'verification_status': 'rejected', 'lifecycle_stage': 'rejected'},
            'pricing': {'recommended_price': pricing.recommended_price, 'price_range_min': pricing.price_range_min,
                        'price_range_max': pricing.price_range_max, 'buyer_savings': pricing.buyer_savings,
                        'new_material_total': pricing.new_material_total, 'per_unit_price': pricing.per_unit_price, 'reasoning': pricing.reasoning},
            'impact': {'waste_diverted_kg': impact.waste_diverted_kg, 'waste_diverted_tonnes': impact.waste_diverted_tonnes,
                       'co2_avoided_kg': impact.co2_avoided_kg, 'co2_avoided_tonnes': impact.co2_avoided_tonnes,
                       'circularity_score': impact.circularity_score, 'trees_equivalent': impact.trees_equivalent,
                       'reasoning': impact.reasoning, 'disclaimer': impact.disclaimer},
            'second_life': [{'use_case': s.use_case, 'suitability_score': s.suitability_score, 'description': s.description, 'category': s.category} for s in sl],
            'agent_activity': [asdict(a) for a in activity],
        }

    def find_best_matches(self, requirement_id: int, db_session) -> dict:
        activity = []
        req = db_session.query(Requirement).filter(Requirement.id == requirement_id).first()
        if not req:
            return {'error': 'Requirement not found', 'matches': [], 'agent_activity': []}

        activity.append(self._step('Orchestrator', f'Processing: {req.quantity_needed} {req.unit} of {req.material_type}', 100))

        candidates = db_session.query(Material).filter(Material.material_type == req.material_type, Material.status == 'available').all()
        if not candidates:
            candidates = [m for m in db_session.query(Material).filter(Material.status == 'available').all()
                          if req.material_type.lower() in m.material_type.lower() or m.material_type.lower() in req.material_type.lower()]

        activity.append(self._step('Matching Agent', f'Found {len(candidates)} candidate(s)', 400))
        match_results = self.matching_agent.find_matches(req, candidates)
        activity.append(self._step('Matching Agent', f'Scored {len(match_results)} match(es)', 500))

        saved = []
        for i, mr in enumerate(match_results[:5]):
            mat = db_session.query(Material).filter(Material.id == mr.material_id).first()
            if not mat:
                continue

            pricing = logistics = imp = None
            if i == 0:
                pricing = self.pricing_agent.estimate_price(mat.material_type, mat.condition or 'good', mat.quantity, mat.age or '', mat.location, mat.unit)
                activity.append(self._step('Pricing Agent', f'Price: \u20b9{pricing.recommended_price:,.0f} (saves \u20b9{pricing.buyer_savings:,.0f})', 350))
                logistics = self.logistics_agent.estimate_logistics(mat.location, req.location, mat.material_type, min(mat.quantity, req.quantity_needed), mat.latitude, mat.longitude, req.latitude, req.longitude)
                activity.append(self._step('Logistics Agent', f'{logistics.direct_distance_km:.0f} km, \u20b9{logistics.route_options[0].estimated_cost:,.0f}', 300))
                imp = self.impact_agent.calculate_impact(mat.material_type, min(mat.quantity, req.quantity_needed), mat.unit, logistics.direct_distance_km, mat.estimated_value or 0, pricing.new_material_total)
                activity.append(self._step('Impact Agent', f'{imp.co2_avoided_tonnes:.1f}t CO\u2082e avoided, circularity {imp.circularity_score}/100', 250))

            rec = Match(material_id=mr.material_id, requirement_id=requirement_id,
                        match_score=mr.match_score, quantity_score=mr.quantity_score,
                        quality_score=mr.quality_score, distance_score=mr.distance_score,
                        price_score=mr.price_score, carbon_score=mr.carbon_score,
                        ai_reasoning=mr.ai_reasoning,
                        recommended_price=pricing.recommended_price if pricing else mat.estimated_value,
                        transport_cost=logistics.route_options[0].estimated_cost if logistics else None,
                        transport_distance_km=mr.transport_distance_km,
                        co2_avoided_kg=imp.co2_avoided_kg if imp else mat.carbon_estimate, status='recommended')
            db_session.add(rec)
            db_session.flush()

            md = {'id': rec.id, 'material_id': mat.id,
                  'material': {'id': mat.id, 'material_type': mat.material_type, 'quantity': mat.quantity,
                               'unit': mat.unit, 'location': mat.location, 'condition': mat.condition,
                               'reuse_score': mat.reuse_score, 'estimated_value': mat.estimated_value},
                  'scores': {'overall': mr.match_score, 'quantity': mr.quantity_score, 'quality': mr.quality_score,
                             'distance': mr.distance_score, 'price': mr.price_score, 'carbon': mr.carbon_score},
                  'ai_reasoning': mr.ai_reasoning, 'transport_distance_km': mr.transport_distance_km}
            if pricing:
                md['pricing'] = {'recommended_price': pricing.recommended_price, 'price_range_min': pricing.price_range_min,
                                 'price_range_max': pricing.price_range_max, 'buyer_savings': pricing.buyer_savings,
                                 'new_material_total': pricing.new_material_total, 'reasoning': pricing.reasoning}
            if logistics:
                md['logistics'] = {'direct_distance_km': logistics.direct_distance_km, 'total_weight_kg': logistics.total_weight_kg,
                                   'recommended_route': logistics.recommended_route,
                                   'route_options': [{'route_name': r.route_name, 'distance_km': r.distance_km,
                                                      'estimated_cost': r.estimated_cost, 'estimated_time_hours': r.estimated_time_hours,
                                                      'co2_emissions_kg': r.co2_emissions_kg, 'vehicle_type': r.vehicle_type,
                                                      'recommended': r.recommended} for r in logistics.route_options],
                                   'reasoning': logistics.reasoning}
            if imp:
                md['impact'] = {'waste_diverted_kg': imp.waste_diverted_kg, 'waste_diverted_tonnes': imp.waste_diverted_tonnes,
                                'co2_avoided_kg': imp.co2_avoided_kg, 'co2_avoided_tonnes': imp.co2_avoided_tonnes,
                                'economic_savings': imp.economic_savings, 'circularity_score': imp.circularity_score,
                                'reasoning': imp.reasoning, 'disclaimer': imp.disclaimer}
            saved.append(md)

        if saved:
            db_session.add(Notification(user_id=req.buyer_id, title='Matches Found',
                                        message=f'{len(saved)} material(s) matched your {req.material_type} requirement',
                                        notification_type='match', reference_id=requirement_id, reference_type='requirement'))
        activity.append(self._step('Orchestrator', f'Complete. {len(saved)} match(es) found.', 100))
        db_session.commit()

        return {
            'requirement': {'id': req.id, 'material_type': req.material_type, 'quantity_needed': req.quantity_needed,
                            'max_budget': req.max_budget, 'location': req.location, 'purpose': req.purpose},
            'matches': saved, 'total_matches': len(saved), 'agent_activity': [asdict(a) for a in activity],
        }
