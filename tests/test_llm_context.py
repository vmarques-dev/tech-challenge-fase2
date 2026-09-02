from llm.context import (
    build_route_context,
    build_summary_context,
)
from models import Delivery
from nearest_neighbor import nearest_neighbor_route
from vehicle import Vehicle


def build_test_data():
    deliveries = [
        Delivery(
            "Base",
            0.0,
            0.0,
            1,
            0.0,
        ),
        Delivery(
            "Hospital A",
            10.0,
            0.0,
            3,
            20.0,
        ),
        Delivery(
            "Hospital B",
            0.0,
            10.0,
            2,
            30.0,
        ),
    ]

    vehicles = [
        Vehicle(
            "Vehicle 1",
            capacity=100.0,
            autonomy=1000.0,
        )
    ]

    return deliveries, vehicles


def test_build_route_context_contains_optimized_metrics():
    deliveries, vehicles = build_test_data()

    context = build_route_context(
        deliveries,
        vehicles,
    )

    assert "optimized" in context
    assert context["optimized"]["fitness"] > 0
    assert context["optimized"]["distance"] > 0
    assert context["optimized"]["routes"] == 1


def test_build_route_context_contains_route_details():
    deliveries, vehicles = build_test_data()

    context = build_route_context(
        deliveries,
        vehicles,
    )

    route = context["route_details"][0]

    assert route["vehicle"] == "Vehicle 1"
    assert route["capacity"] == 100.0
    assert route["load"] == 50.0
    assert route["autonomy"] == 1000.0
    assert route["autonomy_exceeded"] is False
    assert len(route["stops"]) == 3


def test_build_route_context_contains_baseline_comparison():
    deliveries, vehicles = build_test_data()

    baseline_solution = nearest_neighbor_route(
        deliveries
    )

    context = build_route_context(
        deliveries,
        vehicles,
        baseline_solution=baseline_solution,
    )

    assert "baseline" in context
    assert "comparison" in context

    assert (
        context["comparison"][
            "fitness_difference_percent"
        ]
        == 0.0
    )

def test_build_summary_context_removes_stop_details():
    deliveries, vehicles = build_test_data()

    full_context = build_route_context(
        deliveries,
        vehicles,
    )

    summary_context = build_summary_context(
        full_context
    )

    assert "optimized" in summary_context
    assert "vehicles" in summary_context

    vehicle = summary_context["vehicles"][0]

    assert vehicle["vehicle"] == "Vehicle 1"
    assert vehicle["number_of_stops"] == 3
    assert "stops" not in vehicle