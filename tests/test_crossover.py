from genetic_algorithm import order_crossover
from models import Delivery

def test_order_crossover_preserves_all_cities():
    parent1 = ["A", "B", "C", "D", "E"]
    parent2 = ["E", "D", "C", "B", "A"]

    for _ in range(1000):
        child = order_crossover(parent1, parent2)

        assert len(child) == len(parent1)
        assert sorted(child) == sorted(parent1)

def test_order_crossover_can_generate_different_child():
    parent1 = ["A", "B", "C", "D", "E"]
    parent2 = ["E", "D", "C", "B", "A"]

    generated_different_child = False

    for _ in range(1000):
        child = order_crossover(parent1, parent2)

        if child != parent1:
            generated_different_child = True
            break

    assert generated_different_child

def test_order_crossover_with_deliveries():
    parent1 = [
        Delivery("Hospital A", 0.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 3.0, 0.0, 2, 5.0),
        Delivery("Hospital C", 3.0, 4.0, 3, 8.0),
    ]

    parent2 = list(reversed(parent1))

    child = order_crossover(parent1, parent2)

    assert len(child) == len(parent1)
    assert set(child) == set(parent1)