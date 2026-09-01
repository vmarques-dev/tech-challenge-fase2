from genetic_algorithm import generate_random_population, sort_population
from models import Delivery

def test_generate_random_population_preserves_all_cities():
    cities = ["A", "B", "C", "D", "E"]

    population = generate_random_population(cities, population_size=50)

    assert len(population) == 50

    for individual in population:
        assert len(individual) == len(cities)
        assert sorted(individual) == sorted(cities)

def test_sort_population_orders_by_fitness():
    population = [
        ["A", "B", "C"],
        ["C", "B", "A"],
        ["B", "A", "C"],
    ]

    fitness = [30, 10, 20]

    sorted_population, sorted_fitness = sort_population(population, fitness)

    assert list(sorted_fitness) == [10, 20, 30]
    assert list(sorted_population) == [
        ["C", "B", "A"],
        ["B", "A", "C"],
        ["A", "B", "C"],
    ]

def test_generate_random_population_with_deliveries():
    deliveries = [
        Delivery("Hospital A", 0.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 3.0, 0.0, 2, 5.0),
        Delivery("Hospital C", 3.0, 4.0, 3, 8.0),
    ]

    population = generate_random_population(deliveries, population_size=20)

    assert len(population) == 20

    for individual in population:
        assert len(individual) == len(deliveries)
        assert set(individual) == set(deliveries)

def test_generate_random_population_keeps_start_fixed():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 5.0),
        Delivery("Hospital B", 20.0, 0.0, 3, 8.0),
        Delivery("Hospital C", 30.0, 0.0, 2, 6.0),
    ]

    population = generate_random_population(
        deliveries,
        population_size=50,
    )

    for individual in population:
        assert individual[0] == deliveries[0]
        assert set(individual) == set(deliveries)