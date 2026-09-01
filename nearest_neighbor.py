from models import Delivery
from genetic_algorithm import calculate_distance


def nearest_neighbor_route(deliveries: list[Delivery]) -> list[Delivery]:
    if not deliveries:
        return []

    start = deliveries[0]
    unvisited = deliveries[1:].copy()

    route = [start]
    current = start

    while unvisited:
        next_delivery = min(
            unvisited,
            key=lambda delivery: calculate_distance(current, delivery),
        )

        route.append(next_delivery)
        unvisited.remove(next_delivery)
        current = next_delivery

    return route