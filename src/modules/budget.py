from dataclasses import dataclass, field
from typing import Dict, Self

@dataclass
class Budget:
    trip_name: str
    total_budget: float
    currency: str = "RM"
    categories: Dict[str, float] = field(default_factory=dict)

    @property
    def allocated(self) -> float:  # allocate total amount of all categories
        return sum(self.categories.values())

    @property
    def remaining(self) -> float: # display remaining balance
        return self.total_budget - self.allocated

    def to_dict(self) -> dict:
        # convert budget object to dictionary
        return {
            "total_budget": self.total_budget,
            "categories": self.categories
        }

    @classmethod
    def from_dict(cls, trip_name: str, data: dict) -> Self:
        # convert dictionary to object
        return cls(
            trip_name=trip_name,
            total_budget=float(data["total_budget"]),
            categories={k: float(v) for k, v in data.get("categories", {}).items()}
        )
