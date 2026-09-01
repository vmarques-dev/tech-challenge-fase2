from genetic_algorithm import mutate
from models import Delivery

def test_mutation_preserves_all_cities():
    solution = ["A", "B", "C", "D", "E"]

    for _ in range(1000):
        mutated = mutate(solution, mutation_probability=0.0)

        assert len(mutated) == len(solution)
        assert sorted(mutated) == sorted(solution)

def test_mutation_with_zero_probability_does_not_change_solution():
    solution = ["A", "B", "C", "D", "E"]

    mutated = mutate(solution, mutation_probability=0.0)

    assert mutated == solution

def test_mutation_swaps_adjacent_cities():
    solution = ["A", "B", "C", "D", "E"]

    mutated = mutate(solution, mutation_probability=1.0)

    changed_positions = [
        index
        for index, (original, changed) in enumerate(zip(solution, mutated))
        if original != changed
    ]

    assert len(changed_positions) == 2
    assert changed_positions[1] - changed_positions[0] == 1

def test_mutation_with_deliveries():
    solution = [
        Delivery("Hospital A", 0.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 3.0, 0.0, 2, 5.0),
        Delivery("Hospital C", 3.0, 4.0, 3, 8.0),
    ]

    mutated = mutate(solution, mutation_probability=1.0)

    assert len(mutated) == len(solution)
    assert set(mutated) == set(solution)