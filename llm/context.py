from genetic_algorithm import calculate_fitness
from routing import (
    calculate_fleet_fitness,
    calculate_fleet_metrics,
    split_deliveries_by_capacity,
)


def build_route_context(
    optimized_solution,
    vehicles,
    baseline_solution=None,
):
    optimized_metrics = calculate_fleet_metrics(
        optimized_solution,
        vehicles,
    )

    optimized_fitness = calculate_fleet_fitness(
        optimized_solution,
        vehicles,
    )

    routes = split_deliveries_by_capacity(
        optimized_solution,
        vehicles,
    )

    route_details = []

    for route, vehicle in zip(routes, vehicles):
        total_load = sum(
            delivery.demand
            for delivery in route[1:]
        )

        route_distance = calculate_fitness(route)

        route_details.append(
            {
                "vehicle": vehicle.name,
                "capacity": vehicle.capacity,
                "load": total_load,
                "autonomy": vehicle.autonomy,
                "distance": route_distance,
                "autonomy_exceeded": (
                    route_distance > vehicle.autonomy
                ),
                "stops": [
                    {
                        "name": delivery.name,
                        "priority": delivery.priority,
                        "demand": delivery.demand,
                    }
                    for delivery in route
                ],
            }
        )

    context = {
        "optimized": {
            "fitness": optimized_fitness,
            "distance": optimized_metrics["distance"],
            "priority_penalty": optimized_metrics[
                "priority_penalty"
            ],
            "autonomy_penalty": optimized_metrics[
                "autonomy_penalty"
            ],
            "routes": optimized_metrics["routes"],
        },
        "route_details": route_details,
    }

    if baseline_solution is not None:
        baseline_metrics = calculate_fleet_metrics(
            baseline_solution,
            vehicles,
        )

        baseline_fitness = calculate_fleet_fitness(
            baseline_solution,
            vehicles,
        )

        fitness_difference = (
            (optimized_fitness - baseline_fitness)
            / baseline_fitness
            * 100
        )

        context["baseline"] = {
            "fitness": baseline_fitness,
            "distance": baseline_metrics["distance"],
            "priority_penalty": baseline_metrics[
                "priority_penalty"
            ],
            "autonomy_penalty": baseline_metrics[
                "autonomy_penalty"
            ],
            "routes": baseline_metrics["routes"],
        }

        context["comparison"] = {
            "fitness_difference_percent": fitness_difference,
        }

    return context


def build_summary_context(
    context: dict,
) -> dict:
    optimized = context["optimized"]
    baseline = context.get("baseline")

    summary = {
        "optimized": optimized,
        "distance_unit": "scaled simulation units",
    }

    if baseline is not None:
        summary["baseline"] = baseline

        comparison = {}

        if baseline["fitness"] != 0:
            comparison["fitness_difference_percent"] = (
                (optimized["fitness"] - baseline["fitness"])
                / baseline["fitness"]
                * 100
            )

        if baseline["distance"] != 0:
            comparison["distance_difference_percent"] = (
                (optimized["distance"] - baseline["distance"])
                / baseline["distance"]
                * 100
            )

        if baseline["priority_penalty"] != 0:
            comparison[
                "priority_penalty_difference_percent"
            ] = (
                (
                    optimized["priority_penalty"]
                    - baseline["priority_penalty"]
                )
                / baseline["priority_penalty"]
                * 100
            )

        comparison["fitness_change"] = (
            "lower"
            if optimized["fitness"] < baseline["fitness"]
            else "higher"
            if optimized["fitness"] > baseline["fitness"]
            else "unchanged"
        )

        comparison["distance_change"] = (
            "lower"
            if optimized["distance"] < baseline["distance"]
            else "higher"
            if optimized["distance"] > baseline["distance"]
            else "unchanged"
        )

        comparison["priority_penalty_change"] = (
            "lower"
            if optimized["priority_penalty"]
            < baseline["priority_penalty"]
            else "higher"
            if optimized["priority_penalty"]
            > baseline["priority_penalty"]
            else "unchanged"
        )

        summary["comparison"] = comparison

    summary["vehicles"] = [
        {
            "vehicle": route["vehicle"],
            "capacity": route["capacity"],
            "load": route["load"],
            "autonomy": route["autonomy"],
            "distance": route["distance"],
            "autonomy_exceeded": route[
                "autonomy_exceeded"
            ],
            "number_of_stops": len(
                route["stops"]
            ),
        }
        for route in context["route_details"]
    ]

    return summary
