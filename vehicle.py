from dataclasses import dataclass


@dataclass(frozen=True)
class Vehicle:
    name: str
    capacity: float
    autonomy: float