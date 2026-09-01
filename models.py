from dataclasses import dataclass

@dataclass(frozen=True)
class Delivery:
    name: str
    x: float
    y: float
    priority: int
    demand: float