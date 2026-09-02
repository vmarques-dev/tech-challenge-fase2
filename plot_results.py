import csv
import os

import matplotlib.pyplot as plt


RESULTS_FILE = os.path.join(
    "results",
    "ga_experiments.csv",
)

PLOTS_DIR = os.path.join(
    "results",
    "plots",
)

NEAREST_NEIGHBOR_FITNESS = 27971.74
NEAREST_NEIGHBOR_DISTANCE = 3466.52


def load_results():
    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        return [
            {
                "seed": int(row["seed"]),
                "fitness": float(row["fitness"]),
                "distance": float(row["distance"]),
                "fitness_difference": float(
                    row["fitness_difference"]
                ),
            }
            for row in reader
        ]


def plot_fitness_by_seed(results):
    seeds = [
        result["seed"]
        for result in results
    ]

    fitness_values = [
        result["fitness"]
        for result in results
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        seeds,
        fitness_values,
        marker="o",
        label="Genetic Algorithm",
    )

    plt.axhline(
        y=NEAREST_NEIGHBOR_FITNESS,
        linestyle="--",
        label="Nearest Neighbor",
    )

    plt.xlabel("Seed")
    plt.ylabel("Fitness")
    plt.title("GA Fitness by Seed vs. Nearest Neighbor")
    plt.xticks(seeds)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(
        PLOTS_DIR,
        "fitness_by_seed.png",
    )

    plt.savefig(
        output_file,
        dpi=300,
    )

    plt.close()

    print(f"Saved: {output_file}")


def plot_distance_by_seed(results):
    seeds = [
        result["seed"]
        for result in results
    ]

    distance_values = [
        result["distance"]
        for result in results
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        seeds,
        distance_values,
        marker="o",
        label="Genetic Algorithm",
    )

    plt.axhline(
        y=NEAREST_NEIGHBOR_DISTANCE,
        linestyle="--",
        label="Nearest Neighbor",
    )

    plt.xlabel("Seed")
    plt.ylabel("Total Distance")
    plt.title("GA Distance by Seed vs. Nearest Neighbor")
    plt.xticks(seeds)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(
        PLOTS_DIR,
        "distance_by_seed.png",
    )

    plt.savefig(
        output_file,
        dpi=300,
    )

    plt.close()

    print(f"Saved: {output_file}")


def plot_fitness_difference(results):
    seeds = [
        result["seed"]
        for result in results
    ]

    differences = [
        result["fitness_difference"]
        for result in results
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(
        seeds,
        differences,
    )

    plt.axhline(
        y=0,
        linestyle="--",
    )

    plt.xlabel("Seed")
    plt.ylabel("Difference vs. Nearest Neighbor (%)")
    plt.title("GA Fitness Difference vs. Nearest Neighbor")
    plt.xticks(seeds)
    plt.tight_layout()

    output_file = os.path.join(
        PLOTS_DIR,
        "fitness_difference.png",
    )

    plt.savefig(
        output_file,
        dpi=300,
    )

    plt.close()

    print(f"Saved: {output_file}")


def main():
    os.makedirs(
        PLOTS_DIR,
        exist_ok=True,
    )

    results = load_results()

    plot_fitness_by_seed(results)
    plot_distance_by_seed(results)
    plot_fitness_difference(results)


if __name__ == "__main__":
    main()