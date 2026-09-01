from genetic_algorithm import generate_random_population, sort_population

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