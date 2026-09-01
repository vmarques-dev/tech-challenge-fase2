

import random
import math
import copy 
from typing import List, Tuple
from models import Delivery

default_problems = {
5: [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)],
10:[(470, 169), (602, 202), (754, 239), (476, 233), (468, 301), (522, 29), (597, 171), (487, 325), (746, 232), (558, 136)],
12:[(728, 67), (560, 160), (602, 312), (712, 148), (535, 340), (720, 354), (568, 300), (629, 260), (539, 46), (634, 343), (491, 135), (768, 161)],
15:[(512, 317), (741, 72), (552, 50), (772, 346), (637, 12), (589, 131), (732, 165), (605, 15), (730, 38), (576, 216), (589, 381), (711, 387), (563, 228), (494, 22), (787, 288)]
}

def generate_random_population(cities_location, population_size):
    if not cities_location:
        return []

    start = cities_location[0]
    remaining = cities_location[1:]

    population = []

    for _ in range(population_size):
        individual = [start] + random.sample(remaining, len(remaining))
        population.append(individual)

    return population

def calculate_distance(point1, point2) -> float:
    if isinstance(point1, Delivery) and isinstance(point2, Delivery):
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
    else:
        x1, y1 = point1
        x2, y2 = point2

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def calculate_fitness(path: List[Tuple[float, float]]) -> float:
    """
    Calculate the fitness of a given path based on the total Euclidean distance.

    Parameters:
    - path (List[Tuple[float, float]]): A list of tuples representing the path,
      where each tuple contains the coordinates of a point.

    Returns:
    float: The total Euclidean distance of the path.
    """
    distance = 0
    n = len(path)
    for i in range(n):
        distance += calculate_distance(path[i], path[(i + 1) % n])

    return distance

def calculate_priority_penalty(path) -> float:
    cumulative_distance = 0.0
    priority_penalty = 0.0
    n = len(path)

    for i in range(n - 1):
        cumulative_distance += calculate_distance(path[i], path[i + 1])
        priority_penalty += cumulative_distance * path[i + 1].priority

    return priority_penalty


def calculate_hospital_fitness(
    path,
    distance_weight: float = 1.0,
    priority_weight: float = 1.0,
) -> float:
    total_distance = calculate_fitness(path)
    priority_penalty = calculate_priority_penalty(path)

    return (
        distance_weight * total_distance
        + priority_weight * priority_penalty
    )


def order_crossover(parent1, parent2):
    if len(parent1) <= 1:
        return parent1.copy()

    if parent1[0] != parent2[0]:
        raise ValueError("Parents must have the same fixed starting point.")

    start_node = parent1[0]

    route1 = parent1[1:]
    route2 = parent2[1:]

    length = len(route1)

    start_index = random.randint(0, length - 1)
    end_index = random.randint(start_index + 1, length)

    child_route = route1[start_index:end_index]

    remaining_positions = [
        i for i in range(length)
        if i < start_index or i >= end_index
    ]

    remaining_genes = [
        gene for gene in route2
        if gene not in child_route
    ]

    for position, gene in zip(remaining_positions, remaining_genes):
        child_route.insert(position, gene)

    return [start_node] + child_route

def mutate(solution, mutation_probability):
    mutated_solution = copy.deepcopy(solution)

    if random.random() < mutation_probability:
        if len(solution) <= 2:
            return mutated_solution

        index = random.randint(1, len(solution) - 2)

        mutated_solution[index], mutated_solution[index + 1] = (
            mutated_solution[index + 1],
            mutated_solution[index],
        )

    return mutated_solution

def sort_population(population: List[List[Tuple[float, float]]], fitness: List[float]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
    """
    Sort a population based on fitness values.

    Parameters:
    - population (List[List[Tuple[float, float]]]): The population of solutions, where each solution is represented as a list.
    - fitness (List[float]): The corresponding fitness values for each solution in the population.

    Returns:
    Tuple[List[List[Tuple[float, float]]], List[float]]: A tuple containing the sorted population and corresponding sorted fitness values.
    """
    # Combine lists into pairs
    combined_lists = list(zip(population, fitness))

    # Sort based on the values of the fitness list
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1])

    # Separate the sorted pairs back into individual lists
    sorted_population, sorted_fitness = zip(*sorted_combined_lists)

    return sorted_population, sorted_fitness


if __name__ == '__main__':
    N_CITIES = 10
    
    POPULATION_SIZE = 100
    N_GENERATIONS = 100
    MUTATION_PROBABILITY = 0.3
    cities_locations = [(random.randint(0, 100), random.randint(0, 100))
              for _ in range(N_CITIES)]
    
    # CREATE INITIAL POPULATION
    population = generate_random_population(cities_locations, POPULATION_SIZE)

    # Lists to store best fitness and generation for plotting
    best_fitness_values = []
    best_solutions = []
    
    for generation in range(N_GENERATIONS):
  
        
        population_fitness = [calculate_fitness(individual) for individual in population]    
        
        population, population_fitness = sort_population(population,  population_fitness)
        
        best_fitness = calculate_fitness(population[0])
        best_solution = population[0]
           
        best_fitness_values.append(best_fitness)
        best_solutions.append(best_solution)    

        print(f"Generation {generation}: Best fitness = {best_fitness}")

        new_population = [population[0]]  # Keep the best individual: ELITISM
        
        while len(new_population) < POPULATION_SIZE:
            
            # SELECTION
            parent1, parent2 = random.choices(population[:10], k=2)  # Select parents from the top 10 individuals
            
            # CROSSOVER
            child1 = order_crossover(parent1, parent2)
            
            ## MUTATION
            child1 = mutate(child1, MUTATION_PROBABILITY)
            
            new_population.append(child1)
            
    
        print('generation: ', generation)
        population = new_population
    


