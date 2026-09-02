import statistics

import numpy as np

from benchmark_att48 import att_48_cities_locations
from ga_runner import run_genetic_algorithm
from models import Delivery
from nearest_neighbor import nearest_neighbor_route
from routing import (
    calculate_fleet_fitness,
    calculate_fleet_metrics,
)
from vehicle import Vehicle
import csv
import os


WIDTH, HEIGHT = 750, 400
NODE_RADIUS = 10
PLOT_X_OFFSET = 450

POPULATION_SIZE = 100
N_GENERATIONS = 200
MUTATION_PROBABILITY = 0.5

SEEDS = [1, 2, 3, 4, 5]


def build_deliveries():
    att_cities_locations = np.array(att_48_cities_locations)

    max_x = max(point[0] for point in att_cities_locations)
    max_y = max(point[1] for point in att_cities_locations)

    scale_x = (WIDTH - PLOT_X_OFFSET - NODE_RADIUS) / max_x
    scale_y = HEIGHT / max_y

    return [
        Delivery(
            name=f"Hospital {index + 1}",
            x=int(point[0] * scale_x + PLOT_X_OFFSET),
            y=int(point[1] * scale_y),
            priority=(index % 3) + 1,
            demand=float((index % 5) + 1) * 10.0,
        )
        for index, point in enumerate(att_cities_locations)
    ]


def build_vehicles():
    return [
        Vehicle(
            f"Vehicle {index + 1}",
            capacity=250.0,
            autonomy=900.0,
        )
        for index in range(8)
    ]


def main():
    deliveries = build_deliveries()
    vehicles = build_vehicles()

    nearest_neighbor_solution = nearest_neighbor_route(deliveries)

    nearest_neighbor_fitness = calculate_fleet_fitness(
        nearest_neighbor_solution,
        vehicles,
    )

    nearest_neighbor_metrics = calculate_fleet_metrics(
        nearest_neighbor_solution,
        vehicles,
    )

    print("\n=== Experimental Configuration ===")
    print(f"Population size: {POPULATION_SIZE}")
    print(f"Generations: {N_GENERATIONS}")
    print(f"Mutation probability: {MUTATION_PROBABILITY}")
    print(f"Seeds: {SEEDS}")

    print("\n=== Nearest Neighbor Baseline ===")
    print(f"Fitness: {nearest_neighbor_fitness:.2f}")
    print(f"Distance: {nearest_neighbor_metrics['distance']:.2f}")
    print(
        f"Priority penalty: "
        f"{nearest_neighbor_metrics['priority_penalty']:.2f}"
    )
    print(
        f"Autonomy penalty: "
        f"{nearest_neighbor_metrics['autonomy_penalty']:.2f}"
    )
    print(f"Routes: {nearest_neighbor_metrics['routes']}")

    results = []

    for seed in SEEDS:
        print(f"\nRunning GA with seed {seed}...")

        result = run_genetic_algorithm(
            deliveries,
            vehicles,
            population_size=POPULATION_SIZE,
            generations=N_GENERATIONS,
            mutation_probability=MUTATION_PROBABILITY,
            seed=seed,
            verbose=False,
        )

        metrics = calculate_fleet_metrics(
            result["best_solution"],
            vehicles,
        )

        fitness_difference = (
            (result["best_fitness"] - nearest_neighbor_fitness)
            / nearest_neighbor_fitness
            * 100
        )

        experiment_result = {
            "seed": seed,
            "fitness": result["best_fitness"],
            "distance": metrics["distance"],
            "priority_penalty": metrics["priority_penalty"],
            "autonomy_penalty": metrics["autonomy_penalty"],
            "routes": metrics["routes"],
            "fitness_difference": fitness_difference,
        }

        results.append(experiment_result)

        print(
            f"Seed {seed}: "
            f"fitness={experiment_result['fitness']:.2f}, "
            f"distance={experiment_result['distance']:.2f}, "
            f"difference={experiment_result['fitness_difference']:.2f}%"
        )

    os.makedirs("results", exist_ok=True)

    output_file = os.path.join(
        "results",
        "ga_experiments.csv",
    )

    with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8",
    ) as csv_file:
        fieldnames = [
            "seed",
            "fitness",
            "distance",
            "priority_penalty",
            "autonomy_penalty",
            "routes",
            "fitness_difference",
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_file}")

    fitness_values = [
        result["fitness"]
        for result in results
    ]

    distance_values = [
        result["distance"]
        for result in results
    ]

    print("\n=== GA Summary ===")
    print(f"Average fitness: {statistics.mean(fitness_values):.2f}")
    print(f"Best fitness: {min(fitness_values):.2f}")
    print(f"Worst fitness: {max(fitness_values):.2f}")
    print(
        f"Fitness standard deviation: "
        f"{statistics.stdev(fitness_values):.2f}"
    )

    print(f"Average distance: {statistics.mean(distance_values):.2f}")
    print(f"Best distance: {min(distance_values):.2f}")
    print(f"Worst distance: {max(distance_values):.2f}")


if __name__ == "__main__":
    main()