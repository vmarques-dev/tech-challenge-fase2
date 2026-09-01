from models import Delivery

def test_delivery_stores_hospital_data():
    delivery = Delivery(
        name="Hospital A",
        x=10.0,
        y=25.0,
        priority=3,
        demand=12.5,
    )

    assert delivery.name == "Hospital A"
    assert delivery.x == 10.0
    assert delivery.y == 25.0
    assert delivery.priority == 3
    assert delivery.demand == 12.5