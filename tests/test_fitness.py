from genetic_algorithm import calculate_distance, calculate_fitness

def test_calculate_distance():
    point1 = (0, 0)
    point2 = (3, 4)

    distance = calculate_distance(point1, point2)

    assert distance == 5.0

def test_calculate_fitness_closed_route():
    path = [
        (0, 0),
        (3, 0),
        (3, 4),
        (0, 4),
    ]

    fitness = calculate_fitness(path)

    assert fitness == 14.0