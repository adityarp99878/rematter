from dataclasses import dataclass
from .base_agent import BaseAgent

BASE_NEW_PRICES = {
    'brick': 12.0, 'steel_beam': 4500.0, 'steel': 4500.0, 'wood': 600.0,
    'wood/door': 5000.0, 'door': 5000.0, 'window': 3500.0, 'glass': 3000.0,
    'tile': 45.0, 'concrete': 18.0, 'pipe': 400.0, 'granite': 1500.0,
    'bamboo': 80.0, 'roof_tile': 35.0,
}
CONDITION_MULT = {'excellent': 0.70, 'good': 0.60, 'fair': 0.45, 'poor': 0.25}


@dataclass
class PricingResult:
    new_material_price: float
    new_material_total: float
    recommended_price: float
    price_range_min: float
    price_range_max: float
    buyer_savings: float
    buyer_savings_percent: float
    per_unit_price: float
    reasoning: list


class PricingAgent(BaseAgent):
    """AI agent for estimating fair prices for recovered materials."""

    def estimate_price(self, material_type: str, condition: str, quantity: float,
                       age: str = '', location: str = '', unit: str = 'units') -> PricingResult:
        if not material_type:
            material_type = 'brick'
        key = material_type.lower().replace(' ', '_')
        base = BASE_NEW_PRICES.get(key, 0.0 if 'rejected' in str(condition) else 100.0)
        mult = CONDITION_MULT.get(condition, 0.0 if 'rejected' in str(condition) else 0.5)
        age_factor = 1.0
        if age:
            try:
                y = int(''.join(filter(str.isdigit, str(age))))
                if y <= 5: age_factor = 1.0
                elif y <= 10: age_factor = 0.95
                elif y <= 20: age_factor = 0.88
                elif y <= 40: age_factor = 0.78
                else: age_factor = 0.65
            except (ValueError, TypeError):
                pass
        per_unit = round(base * mult * age_factor, 2)
        new_total = round(base * quantity, 0)
        recommended = round(per_unit * quantity, 0)
        savings = round(new_total - recommended, 0)
        pct = round((savings / new_total * 100) if new_total > 0 else 0, 1)
        return PricingResult(
            new_material_price=base, new_material_total=new_total,
            recommended_price=recommended,
            price_range_min=round(recommended * 0.92, 0),
            price_range_max=round(recommended * 1.08, 0),
            buyer_savings=savings, buyer_savings_percent=pct,
            per_unit_price=per_unit,
            reasoning=[
                f'New {material_type} price: \u20b9{base:,.0f}/{unit}',
                f'Condition ({condition}): {mult*100:.0f}% of new',
                f'Recommended: \u20b9{per_unit:,.2f}/{unit}',
                f'Total for {quantity:,.0f} {unit}: \u20b9{recommended:,.0f}',
                f'Buyer saves \u20b9{savings:,.0f} ({pct}%) vs new'
            ]
        )
