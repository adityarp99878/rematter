from dataclasses import dataclass
from .base_agent import BaseAgent
from app.utils.geo import get_material_weight, estimate_transport_emissions

NEW_MATERIAL_EMISSIONS = {
    'brick': 0.74, 'steel_beam': 285.0, 'steel': 285.0,
    'wood': 5.2, 'wood/door': 42.0, 'door': 42.0,
    'window': 35.0, 'glass': 12.5, 'tile': 2.8,
    'concrete': 0.13, 'pipe': 3.5, 'granite': 8.2,
    'bamboo': 0.45, 'roof_tile': 1.2,
}
WASTE_WEIGHT = {
    'brick': 3.0, 'steel_beam': 120.0, 'steel': 120.0,
    'wood': 8.0, 'wood/door': 25.0, 'door': 25.0,
    'window': 15.0, 'glass': 12.0, 'tile': 2.5,
    'concrete': 2.0, 'pipe': 3.5, 'granite': 25.0,
    'bamboo': 2.0, 'roof_tile': 1.8,
}


@dataclass
class ImpactResult:
    material_type: str
    quantity: float
    unit: str
    waste_diverted_kg: float
    waste_diverted_tonnes: float
    co2_avoided_kg: float
    co2_avoided_tonnes: float
    transport_emissions_kg: float
    net_co2_saved_kg: float
    economic_savings: float
    circularity_score: float
    trees_equivalent: float
    reasoning: list
    disclaimer: str


class ImpactAgent(BaseAgent):
    """AI agent for calculating environmental sustainability impact."""

    def calculate_impact(self, material_type: str, quantity: float,
                        unit: str = 'units', transport_distance_km: float = 0,
                        material_value: float = 0, new_material_cost: float = 0) -> ImpactResult:
        mat_str = (material_type or 'brick').lower().replace(' ', '_')
        key = mat_str
        w_per = WASTE_WEIGHT.get(key, 5.0)
        waste_kg = round(quantity * w_per, 1)
        waste_t = round(waste_kg / 1000, 2)
        e_per = NEW_MATERIAL_EMISSIONS.get(key, 1.0)
        co2_kg = round(quantity * e_per, 1)
        co2_t = round(co2_kg / 1000, 2)
        trans_em = estimate_transport_emissions(transport_distance_km, waste_kg) if transport_distance_km > 0 else 0.0
        net = round(co2_kg - trans_em, 1)
        savings = round(new_material_cost - material_value, 0) if new_material_cost and material_value else round(material_value * 0.4, 0) if material_value else 0
        circ = min(100, 70 + (10 if net > 0 else 0) + (5 if waste_t > 1 else 0) + (10 if transport_distance_km < 50 else 5 if transport_distance_km < 100 else 0))
        trees = round(co2_kg / 22, 1)
        return ImpactResult(
            material_type=material_type, quantity=quantity, unit=unit,
            waste_diverted_kg=waste_kg, waste_diverted_tonnes=waste_t,
            co2_avoided_kg=co2_kg, co2_avoided_tonnes=co2_t,
            transport_emissions_kg=trans_em, net_co2_saved_kg=net,
            economic_savings=savings, circularity_score=circ,
            trees_equivalent=trees,
            reasoning=[
                f'Reusing {quantity:,.0f} {unit} diverts {waste_t:.1f}t from landfill',
                f'Estimated {co2_t:.1f}t CO\u2082e avoided vs new production',
                f'Net CO\u2082 saved: {net/1000:.2f}t',
                f'Equivalent to planting {trees:.0f} trees for one year',
                f'Circularity score: {circ}/100',
            ],
            disclaimer='Environmental figures are estimates based on industry-average emission factors.'
        )
