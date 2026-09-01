from models import Delivery
from nearest_neighbor import nearest_neighbor_route


def test_nearest_neighbor_keeps_fixed_start():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 5.0, 0.0, 1, 10.0),
    ]

    route = nearest_neighbor_route(deliveries)

    assert route[0] == deliveries[0]


def test_nearest_neighbor_visits_all_deliveries_once():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Hospital A", 10.0, 0.0, 1, 10.0),
        Delivery("Hospital B", 5.0, 0.0, 1, 10.0),
        Delivery("Hospital C", 20.0, 0.0, 1, 10.0),
    ]

    route = nearest_neighbor_route(deliveries)

    assert len(route) == len(deliveries)
    assert set(route) == set(deliveries)


def test_nearest_neighbor_selects_closest_delivery_first():
    deliveries = [
        Delivery("Base", 0.0, 0.0, 1, 0.0),
        Delivery("Far Hospital", 20.0, 0.0, 1, 10.0),
        Delivery("Near Hospital", 5.0, 0.0, 1, 10.0),
        Delivery("Middle Hospital", 10.0, 0.0, 1, 10.0),
    ]

    route = nearest_neighbor_route(deliveries)

    assert route[1].name == "Near Hospital"