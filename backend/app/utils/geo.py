import math
from typing import Optional

KERALA_CITIES = {
    'thrissur': (10.5276, 76.2144),
    'kochi': (9.9312, 76.2673),
    'palakkad': (10.7867, 76.6548),
    'kozhikode': (11.2588, 75.7804),
    'thiruvananthapuram': (8.5241, 76.9366),
    'kannur': (11.8745, 75.3704),
    'kollam': (8.8932, 76.6141),
    'alappuzha': (9.4981, 76.3388),
    'malappuram': (11.0510, 76.0711),
    'kottayam': (9.5916, 76.5222),
}

MATERIAL_WEIGHTS = {
    'brick': 3.0, 'steel_beam': 120.0, 'steel': 120.0,
    'wood': 8.0, 'wood/door': 25.0, 'door': 25.0,
    'window': 15.0, 'glass': 12.0, 'tile': 2.5,
    'concrete': 2.0, 'pipe': 3.5, 'granite': 25.0,
    'bamboo': 2.0, 'roof_tile': 1.8,
}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in km using Haversine formula."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


def get_city_coordinates(location: str) -> Optional[tuple]:
    """Get lat/lng for a Kerala city. Fuzzy match."""
    loc_lower = location.lower().strip()
    for city, coords in KERALA_CITIES.items():
        if city in loc_lower or loc_lower in city:
            return coords
    return None


def calculate_distance_between_locations(
    loc1: str, loc2: str,
    lat1: float = None, lon1: float = None,
    lat2: float = None, lon2: float = None
) -> float:
    """Calculate distance between two locations."""
    if lat1 and lon1 and lat2 and lon2:
        return haversine_distance(lat1, lon1, lat2, lon2)
    coords1 = (lat1, lon1) if lat1 and lon1 else get_city_coordinates(loc1)
    coords2 = (lat2, lon2) if lat2 and lon2 else get_city_coordinates(loc2)
    if coords1 and coords2:
        return haversine_distance(coords1[0], coords1[1], coords2[0], coords2[1])
    return 50.0


def estimate_transport_cost(distance_km: float, material_type: str, quantity: float) -> float:
    """Estimate transport cost in INR."""
    weight_per_unit = MATERIAL_WEIGHTS.get(material_type, 5.0)
    total_weight_tons = (quantity * weight_per_unit) / 1000.0
    base_cost = distance_km * 15.0
    weight_cost = total_weight_tons * distance_km * 8.0
    return round(max(500.0, base_cost + weight_cost), 0)


def estimate_transport_emissions(distance_km: float, weight_kg: float) -> float:
    """Estimate transport CO2 emissions in kg. 0.12 kg CO2 per ton-km."""
    return round(distance_km * (weight_kg / 1000.0) * 0.12, 2)


def get_material_weight(material_type: str, quantity: float) -> float:
    """Get total weight in kg for a material quantity."""
    return quantity * MATERIAL_WEIGHTS.get(material_type, 5.0)
