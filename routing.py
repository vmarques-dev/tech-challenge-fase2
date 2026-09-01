from models import Delivery
from vehicle import Vehicle
from genetic_algorithm import calculate_hospital_fitness


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
) -> float:
    routes = split_deliveries_by_capacity(deliveries, vehicles)

    total_fitness = 0.0

    for route in routes:
        total_fitness += calculate_hospital_fitness(
            route,
            distance_weight=distance_weight,
            priority_weight=priority_weight,
        )

    return total_fitness