from genetic_algorithm import calculate_distance, calculate_fitness
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