from genetic_algorithm import order_crossover
from models import Delivery

def test_order_crossover_preserves_all_cities():
    parent1 = ["A", "B", "C", "D", "E"]
    parent2 = ["A", "E", "D", "C", "B"]

    for _ in range(1000):
        child = order_crossover(parent1, parent2)

        assert len(child) == len(parent1)
        assert sorted(child) == sorted(parent1)

def test_order_crossover_can_generate_different_child():
    parent1 = ["A", "B", "C", "D", "E"]
    parent2 = ["A", "E", "D", "C", "B"]

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

    parent2 = [parent1[0]] + list(reversed(parent1[1:]))

    child = order_crossover(parent1, parent2)

    assert len(child) == len(parent1)
    assert set(child) == set(parent1)

def test_order_crossover_keeps_start_fixed():
    parent1 = ["Base", "A", "B", "C", "D"]
    parent2 = ["Base", "D", "C", "B", "A"]

    for _ in range(100):
        child = order_crossover(parent1, parent2)

        assert child[0] == "Base"
        assert set(child) == set(parent1)