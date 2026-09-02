import random

import numpy as np

from genetic_algorithm import (
    generate_random_population,
    mutate,
    order_crossover,
    sort_population,
)
from nearest_neighbor import nearest_neighbor_route
from routing import calculate_fleet_fitness


def run_genetic_algorithm(
    deliveries,
    vehicles,
    population_size: int = 100,
    generations: int = 200,
    mutation_probability: float = 0.5,
    seed: int | None = None,
    verbose: bool = False,
):
    if seed is not None:
        random.seed(seed)

    nearest_neighbor_solution = nearest_neighbor_route(deliveries)

    population = generate_random_population(
        deliveries,
        population_size,
    )

    population[0] = nearest_neighbor_solution.copy()

    best_fitness_values = []

    for generation in range(1, generations + 1):
        population_fitness = [
            calculate_fleet_fitness(individual, vehicles)
            for individual in population
        ]

        population, population_fitness = sort_population(
            population,
            population_fitness,
        )

        best_solution = population[0].copy()
        best_fitness = population_fitness[0]

        if verbose and (
                generation == 1
                or generation % 20 == 0
                or generation == generations
        ):
            print(
                f"Generation {generation}/{generations} "
                f"- Best fitness: {best_fitness:.2f}"
            )

        best_fitness_values.append(best_fitness)

        new_population = [best_solution.copy()]

        while len(new_population) < population_size:
            probability = 1 / np.array(population_fitness)

            parent1, parent2 = random.choices(
                population,
                weights=probability,
                k=2,
            )

            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_probability)

            new_population.append(child)

        population = new_population

    return {
        "best_solution": best_solution,
        "best_fitness": best_fitness,
        "fitness_history": best_fitness_values,
        "generations": generations,
    }