from dataclasses import dataclass
from typing import Optional
from .base_agent import BaseAgent
from app.utils.geo import calculate_distance_between_locations


@dataclass
class MatchResult:
    material_id: int
    requirement_id: int
    match_score: float
    quantity_score: float
    quality_score: float
    distance_score: float
    price_score: float
    carbon_score: float
    ai_reasoning: str
    recommended_price: float
    transport_distance_km: float
    co2_avoided_kg: float


class MatchingAgent(BaseAgent):
    """AI agent for matching materials with buyer requirements."""

    def find_matches(self, requirement, materials, db_session=None) -> list:
        matches = []
        for mat in materials:
            score = self._score_match(mat, requirement)
            if score:
                matches.append(score)
        matches.sort(key=lambda m: m.match_score, reverse=True)
        return matches

    def _score_match(self, material, requirement) -> Optional[MatchResult]:
        # Quantity score
        if requirement.quantity_needed <= 0:
            qs = 50.0
        else:
            ratio = material.quantity / requirement.quantity_needed
            qs = min(100, 100 - (ratio - 1.0) * 10) if ratio >= 1.0 else max(0, ratio * 100)

        # Quality
        qual = material.reuse_score or 50.0

        # Distance
        dist = calculate_distance_between_locations(
            material.location, requirement.location,
            material.latitude, material.longitude,
            requirement.latitude, requirement.longitude)
        if dist <= 10: ds = 100.0
        elif dist <= 25: ds = 95.0 - (dist - 10) * 0.5
        elif dist <= 50: ds = 87.5 - (dist - 25) * 1.0
        elif dist <= 100: ds = 62.5 - (dist - 50) * 0.5
        else: ds = max(10, 37.5 - (dist - 100) * 0.2)

        # Price
        if requirement.max_budget and material.estimated_value:
            if material.estimated_value <= requirement.max_budget:
                ps = 70 + (1 - material.estimated_value / requirement.max_budget) * 30
            else:
                ps = max(0, 70 - (material.estimated_value / requirement.max_budget - 1) * 50)
        else:
            ps = 60.0

        # Carbon
        cs = min(100, max(0, 100 - dist * 0.5) + min(10, (material.reuse_score or 50) * 0.1))

        overall = qs * 0.25 + qual * 0.25 + ds * 0.20 + ps * 0.15 + cs * 0.15

        parts = []
        if qs >= 80:
            parts.append(f'Sufficient quantity: {material.quantity} available for {requirement.quantity_needed} needed')
        if qual >= 80:
            parts.append(f'High quality with reuse score {material.reuse_score}/100')
        parts.append(f'Distance: {dist:.0f} km')
        if ps >= 80 and requirement.max_budget:
            parts.append(f'Within budget with savings of \u20b9{requirement.max_budget - (material.estimated_value or 0):,.0f}')
        if cs >= 80:
            parts.append('Low transport emissions due to proximity')
        reasoning = '. '.join(parts) + '.'

        return MatchResult(
            material_id=material.id, requirement_id=requirement.id,
            match_score=round(overall, 1), quantity_score=round(qs, 1),
            quality_score=round(qual, 1), distance_score=round(ds, 1),
            price_score=round(ps, 1), carbon_score=round(cs, 1),
            ai_reasoning=reasoning, recommended_price=material.estimated_value or 0,
            transport_distance_km=round(dist, 1),
            co2_avoided_kg=material.carbon_estimate or 0
        )
