from ga_runner import run_genetic_algorithm
from models import Delivery
from vehicle import Vehicle


def test_ga_runner_returns_expected_result():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 0.0, 10.0, 2, 10.0),
        Delivery("Hospital C", 10.0, 10.0, 3, 10.0),
    ]

    vehicles = [
        Vehicle(
            "Vehicle 1",
            capacity=100.0,
            autonomy=1000.0,
        )
    ]

    result = run_genetic_algorithm(
        deliveries,
        vehicles,
        population_size=10,
        generations=5,
        mutation_probability=0.5,
        seed=42,
    )

    assert len(result["best_solution"]) == len(deliveries)
    assert result["best_fitness"] > 0
    assert len(result["fitness_history"]) == 5
    assert result["generations"] == 5


def test_ga_runner_is_reproducible_with_same_seed():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 0.0, 10.0, 2, 10.0),
        Delivery("Hospital C", 10.0, 10.0, 3, 10.0),
    ]

    vehicles = [
        Vehicle(
            "Vehicle 1",
            capacity=100.0,
            autonomy=1000.0,
        )
    ]

    result1 = run_genetic_algorithm(
        deliveries,
        vehicles,
        population_size=10,
        generations=5,
        seed=42,
    )

    result2 = run_genetic_algorithm(
        deliveries,
        vehicles,
        population_size=10,
        generations=5,
        seed=42,
    )

    assert result1["best_fitness"] == result2["best_fitness"]
    assert result1["best_solution"] == result2["best_solution"]