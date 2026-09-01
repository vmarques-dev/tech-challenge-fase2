from vehicle import Vehicle


def test_vehicle_stores_operational_limits():
    vehicle = Vehicle(
        name="Vehicle 1",
        capacity=100.0,
        autonomy=500.0,
    )

    assert vehicle.name == "Vehicle 1"
    assert vehicle.capacity == 100.0
    assert vehicle.autonomy == 500.0