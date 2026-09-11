from dataclasses import dataclass
from .base_agent import BaseAgent

SECOND_LIFE = {
    'brick': [('Building construction', 96, 'Direct reuse in walls'), ('Garden landscaping', 88, 'Pathways and borders'), ('Decorative cladding', 82, 'Accent walls'), ('Aggregate', 60, 'Crushed for road base')],
    'steel_beam': [('Structural reuse', 90, 'Load-bearing (needs certification)'), ('Furniture', 78, 'Industrial tables/shelving'), ('Art installations', 65, 'Sculptures'), ('Scrap recycling', 55, 'Melt and reforge')],
    'steel': [('Structural reuse', 90, 'Structural applications'), ('Fabrication', 80, 'Custom projects'), ('Scrap recycling', 55, 'Melt and reforge')],
    'wood': [('Construction timber', 92, 'Framing and cladding'), ('Furniture', 87, 'Tables and shelving'), ('Wall paneling', 78, 'Interior panels'), ('Garden structures', 72, 'Pergolas and fencing')],
    'door': [('Door reuse', 96, 'Reuse as door'), ('Furniture conversion', 87, 'Tables and headboards'), ('Wall panels', 78, 'Decorative paneling'), ('Decorative use', 71, 'Art pieces')],
    'wood/door': [('Door reuse', 96, 'Reuse as door'), ('Furniture', 87, 'Tables and headboards'), ('Wall panels', 78, 'Paneling'), ('Decorative', 71, 'Art pieces')],
    'window': [('Window reuse', 90, 'Reuse in similar opening'), ('Greenhouse', 82, 'Greenhouse panels'), ('Picture frames', 68, 'Large frames'), ('Glass recycling', 45, 'Recycle glass')],
    'glass': [('Glazing reuse', 88, 'New frames'), ('Tabletops', 75, 'Furniture tops'), ('Partitions', 70, 'Interior partitions'), ('Aggregate', 40, 'Decorative aggregate')],
    'tile': [('Floor/wall tiling', 94, 'Direct reuse'), ('Mosaic art', 82, 'Mosaic patterns'), ('Stepping stones', 75, 'Garden paths'), ('Aggregate', 40, 'Drainage fill')],
    'concrete': [('Building blocks', 75, 'Reuse as blocks'), ('Retaining walls', 70, 'Non-structural walls'), ('Aggregate', 60, 'Road base'), ('Landscaping', 55, 'Garden borders')],
    'pipe': [('Plumbing reuse', 85, 'Non-critical plumbing'), ('Furniture', 72, 'Industrial fixtures'), ('Garden irrigation', 68, 'Watering systems'), ('Scrap metal', 45, 'Recycle')],
    'granite': [('Countertops', 95, 'Direct reuse'), ('Garden features', 85, 'Benches and stepping stones'), ('Wall cladding', 80, 'Accent features')],
    'bamboo': [('Scaffolding', 88, 'Temporary supports'), ('Furniture', 82, 'Chairs and shelving'), ('Garden structures', 78, 'Fencing and trellises'), ('Crafts', 65, 'Handicrafts')],
    'roof_tile': [('Roof tiling', 92, 'Direct reuse'), ('Garden edging', 75, 'Decorative borders'), ('Drainage', 55, 'Drainage layers')],
}


@dataclass
class SecondLifeOption:
    use_case: str
    suitability_score: float
    description: str
    category: str


class SecondLifeAgent(BaseAgent):
    """Suggests alternative uses for recovered materials."""

    def suggest_uses(self, material_type: str, condition: str = 'good') -> list:
        if 'rejected' in str(condition):
            return []
        key = (material_type or 'brick').lower().replace(' ', '_')
        options = SECOND_LIFE.get(key, SECOND_LIFE.get('brick', []))
        result = []
        for name, score, desc in options:
            adj = score
            if condition == 'poor':
                adj = max(20, score - 25)
            elif condition == 'fair':
                adj = max(30, score - 10)
            cat = 'primary_reuse' if adj >= 85 else ('repurpose' if adj >= 65 else ('creative' if adj >= 45 else 'downcycle'))
            result.append(SecondLifeOption(name, round(adj, 0), desc, cat))
        result.sort(key=lambda x: x.suitability_score, reverse=True)
        return result
