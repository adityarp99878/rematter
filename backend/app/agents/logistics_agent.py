from dataclasses import dataclass
from .base_agent import BaseAgent
from app.utils.geo import (
    calculate_distance_between_locations, estimate_transport_cost,
    estimate_transport_emissions, get_material_weight
)


@dataclass
class RouteOption:
    route_name: str
    distance_km: float
    estimated_cost: float
    estimated_time_hours: float
    co2_emissions_kg: float
    vehicle_type: str
    recommended: bool = False


@dataclass
class LogisticsResult:
    source_location: str
    destination_location: str
    direct_distance_km: float
    total_weight_kg: float
    route_options: list
    recommended_route: str
    reasoning: list


class LogisticsAgent(BaseAgent):
    """AI agent for logistics estimation."""

    def estimate_logistics(self, source: str, dest: str, material_type: str,
                          quantity: float, src_lat=None, src_lng=None,
                          dst_lat=None, dst_lng=None) -> LogisticsResult:
        distance = calculate_distance_between_locations(
            source, dest, src_lat, src_lng, dst_lat, dst_lng)
        weight = get_material_weight(material_type, quantity)
        tons = weight / 1000.0

        cost_d = estimate_transport_cost(distance, material_type, quantity)
        em_d = estimate_transport_emissions(distance, weight)
        time_d = round(max(0.5, distance / 40), 1)

        hw_dist = round(distance * 1.3, 1)
        cost_h = round(cost_d * 1.15, 0)
        em_h = estimate_transport_emissions(hw_dist, weight)
        time_h = round(max(0.5, hw_dist / 55), 1)

        eco_dist = round(distance * 1.1, 1)
        cost_e = round(cost_d * 0.85, 0) if tons < 5 else round(cost_d * 1.3, 0)
        em_e = round(em_d * 0.7, 2)
        time_e = round(max(0.5, eco_dist / 35), 1)

        vehicle = 'Mini Truck (1T)' if tons <= 1 else ('Light Truck (5T)' if tons <= 5 else 'Heavy Truck (10T+)')
        eco_v = 'Electric Van' if tons <= 1 else ('CNG Truck' if tons <= 5 else 'Rail + Last Mile')

        direct_rec = distance <= 30
        routes = [
            RouteOption('Direct Route', distance, cost_d, time_d, em_d, vehicle, direct_rec),
            RouteOption('Highway Route', hw_dist, cost_h, time_h, em_h, vehicle, not direct_rec),
            RouteOption('Eco Route', eco_dist, cost_e, time_e, em_e, eco_v, False),
        ]
        rec = 'Direct Route' if direct_rec else 'Highway Route'
        return LogisticsResult(
            source, dest, distance, weight, routes, rec,
            [f'Distance: {distance:.1f} km', f'Weight: {weight:,.0f} kg ({tons:.1f}t)',
             f'{rec} recommended', f'Eco option with 30% lower emissions via {eco_v}']
        )
