from models import Delivery
from vehicle import Vehicle
from genetic_algorithm import (
    calculate_fitness,
    calculate_hospital_fitness,
    calculate_priority_penalty,
)


def split_deliveries_by_capacity(
    deliveries: list[Delivery],
    vehicles: list[Vehicle],
) -> list[list[Delivery]]:
    if not deliveries:
        return []

    if not vehicles:
        raise ValueError("At least one vehicle is required.")

    base = deliveries[0]
    pending_deliveries = deliveries[1:]

    routes = []
    current_route = [base]
    current_load = 0.0
    vehicle_index = 0

    for delivery in pending_deliveries:
        vehicle = vehicles[vehicle_index]

        if delivery.demand > vehicle.capacity:
            raise ValueError(
                f"Delivery '{delivery.name}' exceeds vehicle capacity."
            )

        if current_load + delivery.demand > vehicle.capacity:
            routes.append(current_route)

            vehicle_index += 1

            if vehicle_index >= len(vehicles):
                raise ValueError(
                    "Fleet capacity is insufficient for all deliveries."
                )

            current_route = [base]
            current_load = 0.0
            vehicle = vehicles[vehicle_index]

            if delivery.demand > vehicle.capacity:
                raise ValueError(
                    f"Delivery '{delivery.name}' exceeds vehicle capacity."
                )

        current_route.append(delivery)
        current_load += delivery.demand

    if len(current_route) > 1:
        routes.append(current_route)

    return routes

def calculate_fleet_fitness(
    deliveries: list[Delivery],
    vehicles: list[Vehicle],
    distance_weight: float = 1.0,
    priority_weight: float = 1.0,
    autonomy_penalty_weight: float = 1000.0,
) -> float:
    routes = split_deliveries_by_capacity(deliveries, vehicles)

    total_fitness = 0.0

    for route, vehicle in zip(routes, vehicles):
        total_fitness += calculate_hospital_fitness(
            route,
            distance_weight=distance_weight,
            priority_weight=priority_weight,
        )

        total_fitness += calculate_autonomy_penalty(
            route,
            vehicle,
            penalty_weight=autonomy_penalty_weight,
        )

    return total_fitness

def calculate_autonomy_penalty(
    route: list[Delivery],
    vehicle: Vehicle,
    penalty_weight: float = 1000.0,
) -> float:
    from genetic_algorithm import calculate_fitness

    route_distance = calculate_fitness(route)
    excess_distance = max(0.0, route_distance - vehicle.autonomy)

    return excess_distance * penalty_weight

def calculate_fleet_metrics(
    deliveries: list[Delivery],
    vehicles: list[Vehicle],
) -> dict:
    routes = split_deliveries_by_capacity(deliveries, vehicles)

    total_distance = 0.0
    total_priority_penalty = 0.0
    total_autonomy_penalty = 0.0

    for route, vehicle in zip(routes, vehicles):
        total_distance += calculate_fitness(route)
        total_priority_penalty += calculate_priority_penalty(route)
        total_autonomy_penalty += calculate_autonomy_penalty(
            route,
            vehicle,
        )

    return {
        "distance": total_distance,
        "priority_penalty": total_priority_penalty,
        "autonomy_penalty": total_autonomy_penalty,
        "routes": len(routes),
    }