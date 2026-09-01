from models import Delivery
from routing import (
    split_deliveries_by_capacity,
    calculate_fleet_fitness,
    calculate_autonomy_penalty
)
from vehicle import Vehicle


def test_split_deliveries_uses_multiple_vehicles_when_needed():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 20.0),
        Delivery("Hospital B", 20.0, 0.0, 2, 20.0),
        Delivery("Hospital C", 30.0, 0.0, 3, 20.0),
    ]

    vehicles = [
        Vehicle("Vehicle 1", capacity=40.0, autonomy=500.0),
        Vehicle("Vehicle 2", capacity=40.0, autonomy=500.0),
    ]

    routes = split_deliveries_by_capacity(deliveries, vehicles)

    assert len(routes) == 2

    assert routes[0] == [
        deliveries[0],
        deliveries[1],
        deliveries[2],
    ]

    assert routes[1] == [
        deliveries[0],
        deliveries[3],
    ]

def test_split_deliveries_keeps_each_route_within_capacity():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 15.0),
        Delivery("Hospital B", 20.0, 0.0, 2, 15.0),
        Delivery("Hospital C", 30.0, 0.0, 3, 15.0),
    ]

    vehicles = [
        Vehicle("Vehicle 1", capacity=30.0, autonomy=500.0),
        Vehicle("Vehicle 2", capacity=30.0, autonomy=500.0),
    ]

    routes = split_deliveries_by_capacity(deliveries, vehicles)

    for route, vehicle in zip(routes, vehicles):
        total_demand = sum(delivery.demand for delivery in route)

        assert total_demand <= vehicle.capacity

def test_split_deliveries_fails_when_fleet_capacity_is_insufficient():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 30.0),
        Delivery("Hospital B", 20.0, 0.0, 2, 30.0),
        Delivery("Hospital C", 30.0, 0.0, 3, 30.0),
    ]

    vehicles = [
        Vehicle("Vehicle 1", capacity=40.0, autonomy=500.0),
        Vehicle("Vehicle 2", capacity=40.0, autonomy=500.0),
    ]

    try:
        split_deliveries_by_capacity(deliveries, vehicles)

        assert False, "Expected ValueError"

    except ValueError as error:
        assert str(error) == (
            "Fleet capacity is insufficient for all deliveries."
        )

def test_fleet_fitness_prefers_better_delivery_order():
    base = Delivery("Base", 0.0, 0.0, 1, 0.0)
    normal = Delivery("Normal Hospital", 10.0, 0.0, 1, 10.0)
    critical = Delivery("Critical Hospital", 0.0, 10.0, 3, 10.0)

    vehicles = [
        Vehicle("Vehicle 1", capacity=30.0, autonomy=500.0),
    ]

    critical_late = [
        base,
        normal,
        critical,
    ]

    critical_early = [
        base,
        critical,
        normal,
    ]

    late_fitness = calculate_fleet_fitness(
        critical_late,
        vehicles,
    )

    early_fitness = calculate_fleet_fitness(
        critical_early,
        vehicles,
    )

    assert early_fitness < late_fitness

def test_fleet_fitness_supports_multiple_vehicle_routes():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 20.0),
        Delivery("Hospital B", 20.0, 0.0, 2, 20.0),
        Delivery("Hospital C", 30.0, 0.0, 3, 20.0),
    ]

    vehicles = [
        Vehicle("Vehicle 1", capacity=40.0, autonomy=500.0),
        Vehicle("Vehicle 2", capacity=40.0, autonomy=500.0),
    ]

    fitness = calculate_fleet_fitness(
        deliveries,
        vehicles,
    )

    assert fitness > 0.0

def test_autonomy_penalty_is_zero_when_route_is_within_limit():
    route = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 3.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 3.0, 4.0, 2, 10.0),
    ]

    vehicle = Vehicle(
        "Vehicle 1",
        capacity=100.0,
        autonomy=20.0,
    )

    penalty = calculate_autonomy_penalty(route, vehicle)

    assert penalty == 0.0

def test_autonomy_penalty_increases_when_route_exceeds_limit():
    route = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 3.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 3.0, 4.0, 2, 10.0),
    ]

    vehicle = Vehicle(
        "Vehicle 1",
        capacity=100.0,
        autonomy=10.0,
    )

    penalty = calculate_autonomy_penalty(
        route,
        vehicle,
        penalty_weight=1000.0,
    )

    assert penalty == 2000.0

def test_fleet_fitness_penalizes_insufficient_autonomy():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 3.0, 4.0, 2, 10.0),
    ]

    vehicle_with_enough_autonomy = [
        Vehicle(
            "Vehicle 1",
            capacity=100.0,
            autonomy=20.0,
        )
    ]

    vehicle_with_low_autonomy = [
        Vehicle(
            "Vehicle 1",
            capacity=100.0,
            autonomy=5.0,
        )
    ]

    valid_fitness = calculate_fleet_fitness(
        deliveries,
        vehicle_with_enough_autonomy,
    )

    penalized_fitness = calculate_fleet_fitness(
        deliveries,
        vehicle_with_low_autonomy,
    )

    assert penalized_fitness > valid_fitness