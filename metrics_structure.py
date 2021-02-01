from dataclasses import dataclass


@dataclass
class Metrics:
    name: str
    value: float
    timestamp: int
