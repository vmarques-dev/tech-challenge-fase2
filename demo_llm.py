import numpy as np

from benchmark_att48 import att_48_cities_locations
from ga_runner import run_genetic_algorithm
from llm.context import build_route_context
from llm.service import LLMService
from models import Delivery
from nearest_neighbor import nearest_neighbor_route
from vehicle import Vehicle
from llm.context import build_summary_context

WIDTH = 750
HEIGHT = 400
NODE_RADIUS = 10
PLOT_X_OFFSET = 450

POPULATION_SIZE = 100
N_GENERATIONS = 200
MUTATION_PROBABILITY = 0.5
SEED = 5


def build_deliveries():
    cities = np.array(
        att_48_cities_locations
    )

    max_x = max(point[0] for point in cities)
    max_y = max(point[1] for point in cities)

    scale_x = (
        WIDTH - PLOT_X_OFFSET - NODE_RADIUS
    ) / max_x

    scale_y = HEIGHT / max_y

    return [
        Delivery(
            name=f"Hospital {index + 1}",
            x=int(
                point[0] * scale_x
                + PLOT_X_OFFSET
            ),
            y=int(point[1] * scale_y),
            priority=(index % 3) + 1,
            demand=float(
                (index % 5) + 1
            ) * 10.0,
        )
        for index, point in enumerate(cities)
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
    print("Building hospital routing scenario...")

    deliveries = build_deliveries()
    vehicles = build_vehicles()

    baseline_solution = nearest_neighbor_route(
        deliveries
    )

    print("Running Genetic Algorithm...")

    ga_result = run_genetic_algorithm(
        deliveries,
        vehicles,
        population_size=POPULATION_SIZE,
        generations=N_GENERATIONS,
        mutation_probability=MUTATION_PROBABILITY,
        seed=SEED,
        verbose=True,
    )

    print("\nBuilding LLM context...")

    context = build_route_context(
        optimized_solution=ga_result[
            "best_solution"
        ],
        vehicles=vehicles,
        baseline_solution=baseline_solution,
    )

    print(
        f"Optimized fitness: "
        f"{context['optimized']['fitness']:.2f}"
    )

    print(
        f"Optimized distance: "
        f"{context['optimized']['distance']:.2f}"
    )

    print(
        f"Baseline fitness: "
        f"{context['baseline']['fitness']:.2f}"
    )

    print(
        f"Fitness difference: "
        f"{context['comparison']['fitness_difference_percent']:.2f}%"
    )

    summary_context = build_summary_context(
        context
    )

    print(
        f"Distance difference: "
        f"{summary_context['comparison']['distance_difference_percent']:.2f}%"
    )

    print(
        f"Priority penalty difference: "
        f"{summary_context['comparison']['priority_penalty_difference_percent']:.2f}%"
    )

    print("\nSending real routing data to local LLM...\n")

    service = LLMService()

    response = service.generate_route_report(
        context,
        period="daily",
    )

    print("=== LOCAL LLM ROUTE REPORT ===")
    print(response)


if __name__ == "__main__":
    main()