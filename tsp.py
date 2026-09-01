import pygame
from pygame.locals import *
import random
import itertools
from genetic_algorithm import (
    mutate,
    order_crossover,
    generate_random_population,
    calculate_fitness,
    calculate_hospital_fitness,
    sort_population,
    default_problems,
)
from draw_functions import draw_paths, draw_plot, draw_cities
import sys
import numpy as np
import pygame
from benchmark_att48 import *
from models import Delivery
from vehicle import Vehicle
from routing import (
    calculate_fleet_fitness,
    split_deliveries_by_capacity,
)
from nearest_neighbor import nearest_neighbor_route
from routing import calculate_fleet_metrics

# Define constant values
# pygame
WIDTH, HEIGHT = 800, 400
NODE_RADIUS = 10
FPS = 30
PLOT_X_OFFSET = 450

# GA
N_CITIES = 15
POPULATION_SIZE = 100
N_GENERATIONS = None
MUTATION_PROBABILITY = 0.5

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ROUTE_COLORS = [
    (0, 102, 255),    # Vehicle 1 - blue
    (0, 180, 0),      # Vehicle 2 - green
    (255, 140, 0),    # Vehicle 3 - orange
    (180, 0, 255),    # Vehicle 4 - purple
    (0, 200, 200),    # Vehicle 5 - cyan
    (255, 0, 150),    # Vehicle 6 - pink
    (150, 75, 0),     # Vehicle 7 - brown
    (80, 80, 80),     # Vehicle 8 - gray
]


# Initialize problem
# Using Random cities generation
# cities_locations = [(random.randint(NODE_RADIUS + PLOT_X_OFFSET, WIDTH - NODE_RADIUS), random.randint(NODE_RADIUS, HEIGHT - NODE_RADIUS))
#                     for _ in range(N_CITIES)]


# # # Using Deault Problems: 10, 12 or 15
# WIDTH, HEIGHT = 800, 400
# cities_locations = default_problems[15]


# Using att48 benchmark
WIDTH, HEIGHT = 750, 400
att_cities_locations = np.array(att_48_cities_locations)
max_x = max(point[0] for point in att_cities_locations)
max_y = max(point[1] for point in att_cities_locations)
scale_x = (WIDTH - PLOT_X_OFFSET - NODE_RADIUS) / max_x
scale_y = HEIGHT / max_y
deliveries = [
    Delivery(
        name=f"Hospital {index + 1}",
        x=int(point[0] * scale_x + PLOT_X_OFFSET),
        y=int(point[1] * scale_y),
        priority=(index % 3) + 1,
        demand=float((index % 5) + 1) * 10.0,
    )
    for index, point in enumerate(att_cities_locations)
]
vehicles = [
    Vehicle(f"Vehicle {index + 1}", capacity=250.0, autonomy=900.0)
    for index in range(8)
]
nearest_neighbor_solution = nearest_neighbor_route(deliveries)

nearest_neighbor_fitness = calculate_fleet_fitness(
    nearest_neighbor_solution,
    vehicles,
)
target_solution = [deliveries[i - 1] for i in att_48_cities_order]
fitness_target_solution = calculate_fitness(target_solution)
print(f"Best Solution: {fitness_target_solution}")
# ----- Using att48 benchmark


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSP Solver using Pygame")
clock = pygame.time.Clock()
generation_counter = itertools.count(start=1)  # Start the counter at 1


# Create Initial Population
# TODO:- use some heuristic like Nearest Neighbour our Convex Hull to initialize
population = generate_random_population(
    deliveries,
    POPULATION_SIZE,
)

population[0] = nearest_neighbor_solution.copy()
best_fitness_values = []
best_solutions = []


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    generation = next(generation_counter)

    screen.fill(WHITE)

    population_fitness = [
        calculate_fleet_fitness(individual, vehicles)
        for individual in population
    ]

    population, population_fitness = sort_population(
        population,  population_fitness)

    best_fitness = calculate_fleet_fitness(
        population[0],
        vehicles,
    )
    best_solution = population[0]
    best_routes = split_deliveries_by_capacity(
        best_solution,
        vehicles
    )

    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    draw_plot(screen, list(range(len(best_fitness_values))),
              best_fitness_values, y_label="Hospital Fitness")

    draw_cities(screen, deliveries, RED, NODE_RADIUS)
    for vehicle_index, route in enumerate(best_routes):
        route_color = ROUTE_COLORS[vehicle_index % len(ROUTE_COLORS)]

        draw_paths(
            screen,
            route,
            route_color,
            width=3,
        )

    print(f"Generation {generation}: Best fitness = {round(best_fitness, 2)}")

    new_population = [population[0]]  # Keep the best individual: ELITISM

    while len(new_population) < POPULATION_SIZE:

        # selection
        # simple selection based on first 10 best solutions
        # parent1, parent2 = random.choices(population[:10], k=2)

        # solution based on fitness probability
        probability = 1 / np.array(population_fitness)
        parent1, parent2 = random.choices(population, weights=probability, k=2)

        child1 = order_crossover(parent1, parent2)

        child1 = mutate(child1, MUTATION_PROBABILITY)

        new_population.append(child1)

    population = new_population

    pygame.display.flip()
    clock.tick(FPS)


# TODO: save the best individual in a file if it is better than the one saved.

ga_fitness = calculate_fleet_fitness(
    best_solution,
    vehicles,
)

improvement = (
    (nearest_neighbor_fitness - ga_fitness)
    / nearest_neighbor_fitness
    * 100
)

print("\n--- Routing Comparison ---")
print(f"Nearest Neighbor fitness: {nearest_neighbor_fitness:.2f}")
print(f"Genetic Algorithm fitness: {ga_fitness:.2f}")
fitness_difference = (
    (ga_fitness - nearest_neighbor_fitness)
    / nearest_neighbor_fitness
    * 100
)
print(
    f"GA fitness difference vs. Nearest Neighbor: "
    f"{fitness_difference:.2f}%"
)
print("--------------------------")

nn_metrics = calculate_fleet_metrics(
    nearest_neighbor_solution,
    vehicles,
)

ga_metrics = calculate_fleet_metrics(
    best_solution,
    vehicles,
)

print("\n--- Detailed Routing Metrics ---")
print(
    f"Nearest Neighbor: "
    f"distance={nn_metrics['distance']:.2f}, "
    f"priority={nn_metrics['priority_penalty']:.2f}, "
    f"autonomy={nn_metrics['autonomy_penalty']:.2f}, "
    f"routes={nn_metrics['routes']}"
)
print(
    f"Genetic Algorithm: "
    f"distance={ga_metrics['distance']:.2f}, "
    f"priority={ga_metrics['priority_penalty']:.2f}, "
    f"autonomy={ga_metrics['autonomy_penalty']:.2f}, "
    f"routes={ga_metrics['routes']}"
)

# exit software
pygame.quit()
sys.exit()
