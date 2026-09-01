from genetic_algorithm import (
    calculate_distance,
    calculate_fitness,
    calculate_hospital_fitness,
    calculate_capacity_penalty
)
from models import Delivery

def test_calculate_distance():
    point1 = (0, 0)
    point2 = (3, 4)

    distance = calculate_distance(point1, point2)

    assert distance == 5.0

def test_calculate_fitness_closed_route():
    path = [
        (0, 0),
        (3, 0),
        (3, 4),
        (0, 4),
    ]

    fitness = calculate_fitness(path)

    assert fitness == 14.0

def test_calculate_distance_between_deliveries():
    delivery1 = Delivery(
        name="Hospital A",
        x=0.0,
        y=0.0,
        priority=1,
        demand=10.0,
    )

    delivery2 = Delivery(
        name="Hospital B",
        x=3.0,
        y=4.0,
        priority=3,
        demand=5.0,
    )

    distance = calculate_distance(delivery1, delivery2)

    assert distance == 5.0

def test_calculate_fitness_with_deliveries():
    path = [
        Delivery(
            name="Hospital A",
            x=0.0,
            y=0.0,
            priority=1,
            demand=10.0,
        ),
        Delivery(
            name="Hospital B",
            x=3.0,
            y=0.0,
            priority=2,
            demand=5.0,
        ),
        Delivery(
            name="Hospital C",
            x=3.0,
            y=4.0,
            priority=3,
            demand=8.0,
        ),
        Delivery(
            name="Hospital D",
            x=0.0,
            y=4.0,
            priority=1,
            demand=6.0,
        ),
    ]

    fitness = calculate_fitness(path)

    assert fitness == 14.0

def test_hospital_fitness_prefers_critical_delivery_earlier():
    start = Delivery("Start", 0.0, 0.0, 1, 0.0)
    normal = Delivery("Normal Hospital", 10.0, 0.0, 1, 5.0)
    critical = Delivery("Critical Hospital", 0.0, 10.0, 3, 5.0)

    critical_late = [
        start,
        normal,
        critical,
    ]

    critical_early = [
        start,
        critical,
        normal,
    ]

    late_fitness = calculate_hospital_fitness(critical_late)
    early_fitness = calculate_hospital_fitness(critical_early)

    assert early_fitness < late_fitness

def test_capacity_penalty_is_zero_when_within_capacity():
    path = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 20.0, 0.0, 2, 15.0),
    ]

    penalty = calculate_capacity_penalty(
        path,
        vehicle_capacity=30.0,
    )

    assert penalty == 0.0

def test_capacity_penalty_increases_when_capacity_is_exceeded():
    path = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 20.0),
        Delivery("Hospital B", 20.0, 0.0, 2, 20.0),
    ]

    penalty = calculate_capacity_penalty(
        path,
        vehicle_capacity=30.0,
        penalty_weight=1000.0,
    )

    assert penalty == 10000.0