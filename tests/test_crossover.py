from genetic_algorithm import order_crossover

def test_order_crossover_preserves_all_cities():
    parent1 = ["A", "B", "C", "D", "E"]
    parent2 = ["E", "D", "C", "B", "A"]

    for _ in range(1000):
        child = order_crossover(parent1, parent2)

        assert len(child) == len(parent1)
        assert sorted(child) == sorted(parent1)

def test_order_crossover_can_generate_different_child():
    parent1 = ["A", "B", "C", "D", "E"]
    parent2 = ["E", "D", "C", "B", "A"]

    generated_different_child = False

    for _ in range(1000):
        child = order_crossover(parent1, parent2)

        if child != parent1:
            generated_different_child = True
            break

    assert generated_different_child