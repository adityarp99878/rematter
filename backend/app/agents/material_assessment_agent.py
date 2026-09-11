from dataclasses import dataclass
from typing import Optional
from .base_agent import BaseAgent

STRUCTURAL_MATERIALS = {'steel_beam', 'steel', 'concrete'}
CONDITION_SCORES = {'excellent': 95, 'good': 80, 'fair': 60, 'poor': 30}
DEMAND_SCORES = {
    'brick': 85, 'steel_beam': 75, 'steel': 75, 'wood': 70, 'door': 65,
    'wood/door': 65, 'window': 60, 'glass': 55, 'tile': 80, 'concrete': 70,
    'pipe': 65, 'granite': 90, 'bamboo': 75, 'roof_tile': 70
}
MATERIAL_DEFECTS = {
    'brick': {'good': ['minor edge chipping on ~5% of units'], 'fair': ['visible cracks on ~15%', 'moderate edge damage'], 'poor': ['extensive cracking', 'significant breakage']},
    'steel_beam': {'good': ['light surface rust', 'minor scratches'], 'fair': ['moderate surface corrosion', 'minor deformation'], 'poor': ['heavy corrosion', 'visible deformation']},
    'steel': {'good': ['light surface rust'], 'fair': ['moderate corrosion'], 'poor': ['heavy corrosion']},
    'wood': {'good': ['minor surface scratches'], 'fair': ['visible cracks', 'some warping'], 'poor': ['visible rot', 'insect damage']},
    'door': {'good': ['minor edge damage', 'slight finish deterioration'], 'fair': ['visible scratches', 'minor warping'], 'poor': ['significant warping', 'panel damage']},
    'wood/door': {'good': ['minor edge damage'], 'fair': ['visible scratches', 'hinge wear'], 'poor': ['rot at base', 'panel damage']},
    'window': {'good': ['minor frame deterioration'], 'fair': ['frame corrosion', 'seal degradation'], 'poor': ['significant frame damage', 'glass cracks']},
    'glass': {'good': ['minor frame wear'], 'fair': ['minor chips at edges'], 'poor': ['visible cracks', 'significant chipping']},
    'concrete': {'good': ['hairline surface cracks'], 'fair': ['visible cracking', 'minor spalling'], 'poor': ['extensive cracking', 'exposed reinforcement']},
    'tile': {'good': ['minor edge chips on ~3%'], 'fair': ['chipped edges on ~10%', 'surface scratches'], 'poor': ['significant chipping', 'cracks']},
    'pipe': {'good': ['minor surface oxidation'], 'fair': ['moderate corrosion', 'minor dents'], 'poor': ['heavy corrosion', 'joint damage']},
    'granite': {'good': ['minor edge chips'], 'fair': ['edge chipping', 'surface scratches'], 'poor': ['cracks', 'staining']},
    'bamboo': {'good': ['minor surface wear'], 'fair': ['splitting at ends'], 'poor': ['extensive splitting', 'mold']},
    'roof_tile': {'good': ['minor edge wear'], 'fair': ['chips on edges'], 'poor': ['broken tiles', 'extensive cracking']},
}


@dataclass
class AssessmentResult:
    material: str
    quantity: float
    condition: str
    visible_defects: list
    reuse_score: float
    risk_level: str
    confidence: float
    recommendation: str
    verification_required: bool
    reasoning: list
    safety_disclaimer: str = ""


class MaterialAssessmentAgent(BaseAgent):
    """AI agent for assessing material condition and reuse score."""

    def assess(self, detections: list, material_type: str, metadata: dict, image_paths: list = None) -> AssessmentResult:
        if not self.is_demo_mode:
            result = self._llm_assess(detections, material_type, metadata, image_paths or [])
            if result:
                return result
        return self._mock_assess(detections, material_type, metadata)

    def _determine_condition(self, material_type: str, metadata: dict) -> str:
        if metadata.get('condition'):
            return metadata['condition']
        age = metadata.get('age', '')
        if age:
            try:
                years = int(''.join(filter(str.isdigit, str(age))))
                if years <= 5: return 'excellent'
                elif years <= 15: return 'good'
                elif years <= 30: return 'fair'
                else: return 'poor'
            except (ValueError, TypeError):
                pass
        return 'good'

    def calculate_reuse_score(self, condition: str, material_type: str,
                              has_docs: bool = False, age: str = '') -> float:
        """Condition 35%, Integrity 25%, Documentation 15%, Age 15%, Demand 10%."""
        cond = CONDITION_SCORES.get(condition, 60)
        integrity = {'excellent': 98, 'good': 85, 'fair': 65, 'poor': 35}.get(condition, 65)
        doc = 80 if has_docs else 50
        age_score = 70
        if age:
            try:
                y = int(''.join(filter(str.isdigit, str(age))))
                if y <= 5: age_score = 95
                elif y <= 10: age_score = 85
                elif y <= 20: age_score = 70
                elif y <= 40: age_score = 55
                else: age_score = 35
            except (ValueError, TypeError):
                pass
        demand = DEMAND_SCORES.get(material_type, 60)
        return round(cond * 0.35 + integrity * 0.25 + doc * 0.15 + age_score * 0.15 + demand * 0.10, 1)

    def _mock_assess(self, detections, material_type, metadata, cv_data=None) -> AssessmentResult:
        if cv_data and cv_data.get('has_deep_split'):
            condition = 'poor'
            defects = cv_data.get('detected_defects', ['severe structural fracture/breakage'])
            score = float(cv_data.get('integrity_score', 25))
            recommendation = 'recycle'
            risk = 'high'
            confidence = 0.94
            reasoning = [
                'Computer vision detected a deep fracture splitting the material into detached segments.',
                'Severe structural compromise renders the item unsuitable for load-bearing or direct reuse.',
                'Recommended for downcycling or crushing as aggregate.'
            ]
        else:
            condition = self._determine_condition(material_type, metadata)
            key = material_type.lower().replace(' ', '_')
            defects_map = MATERIAL_DEFECTS.get(key, MATERIAL_DEFECTS.get('brick', {}))
            defects = defects_map.get(condition, defects_map.get('good', []))
            if condition == 'excellent':
                defects = []
            has_docs = bool(metadata.get('previous_use') or metadata.get('description'))
            score = self.calculate_reuse_score(condition, key, has_docs, metadata.get('age', ''))
            risk = 'low' if score >= 80 else ('medium' if score >= 50 else 'high')
            is_structural = key in STRUCTURAL_MATERIALS
            if is_structural and risk == 'low' and score < 85:
                risk = 'medium'
            confidence = 0.88
            recommendation = 'reuse' if score >= 80 else ('verify_then_reuse' if score >= 50 else 'recycle')
            reasoning = [f'Material appears in {condition} condition overall']
            if defects:
                reasoning.append(f'Defects noted: {", ".join(defects)}')
            reasoning.append(f'Reuse score {score}/100 - {"High" if score >= 80 else "Moderate" if score >= 50 else "Low"} reuse potential')

        is_structural = material_type.lower().replace(' ', '_') in STRUCTURAL_MATERIALS
        verification = is_structural and score < 80
        safety = ''
        if is_structural:
            safety = ('AI assessment is a preliminary visual assessment and does not replace '
                      'professional structural inspection or engineering certification.')
        quantity = metadata.get('quantity', 0)
        if quantity == 0 and detections:
            d = detections[0]
            quantity = d.get('count_estimate', 100) if isinstance(d, dict) else getattr(d, 'count_estimate', 100)

        return AssessmentResult(
            material=material_type, quantity=float(quantity), condition=condition,
            visible_defects=defects, reuse_score=score, risk_level=risk,
            confidence=confidence, recommendation=recommendation,
            verification_required=verification, reasoning=reasoning,
            safety_disclaimer=safety
        )

    def _llm_assess(self, detections, material_type, metadata, image_paths: list) -> Optional[AssessmentResult]:
        import json
        import os
        from app.config import get_settings
        from app.vision.cv_analyzer import analyze_material_image

        cv_info = {}
        if image_paths:
            settings = get_settings()
            real_path = os.path.join(settings.UPLOAD_DIR, os.path.basename(image_paths[0]))
            if os.path.exists(real_path):
                try:
                    cv_info = analyze_material_image(real_path)
                except Exception as e:
                    print("CV Analyzer exception:", e)

        prompt = f"""Assess this construction material for circular reuse.
Material Type: {material_type}
User Metadata: {json.dumps(metadata)}
Computer Vision Optical Analysis: {json.dumps(cv_info)}

CRITICAL INSTRUCTIONS:
- If Computer Vision Optical Analysis indicates 'has_deep_split': true or 'condition_estimate': 'poor', the material is fractured/broken. You MUST rate condition as 'poor', reuse_score between 15-30, risk_level as 'high', and recommendation as 'recycle'.
- If the material is intact with good integrity, rate condition appropriately ('good' or 'excellent') with score >= 75.
- Output ONLY valid JSON matching the schema."""

        system = """You are an expert civil engineering AI agent assessing salvaged materials. Output ONLY a valid JSON object:
{
  "material": "string",
  "quantity": number,
  "condition": "excellent|good|fair|poor",
  "visible_defects": ["list of strings"],
  "reuse_score": number (0-100),
  "risk_level": "low|medium|high",
  "confidence": number (0.0-1.0),
  "recommendation": "reuse|verify_then_reuse|recycle",
  "verification_required": boolean,
  "reasoning": ["list of strings explaining the engineering judgment"],
  "safety_disclaimer": "string"
}"""
        result = self.llm_call(prompt, system)
        parsed = self.parse_json_response(result)
        if parsed:
            try:
                return AssessmentResult(**parsed)
            except Exception as e:
                print("Failed to parse LLM AssessmentResult:", e)
        
        # Fallback to CV grounded assessment
        return self._mock_assess(detections, material_type, metadata, cv_data=cv_info)
