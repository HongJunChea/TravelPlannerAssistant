from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Budget:
    trip_name: str
    total_budget: float
    categories: Dict[str, float] = field(default_factory=dict)

    @property
    def allocated(self) -> float:
        """Total allocated amount across all categories."""
        return sum(self.categories.values())

    @property
    def remaining(self) -> float:
        """Remaining budget balance."""
        return self.total_budget - self.allocated

    def to_dict(self) -> dict:
        """Convert a Budget object to dict with RM formatting."""
        return {
            "total_budget": f"RM{self.total_budget:.2f}",
            "categories": {cat: f"RM{amt:.2f}" for cat, amt in self.categories.items()}
        }

    @staticmethod
    def from_dict(trip_name: str, data: dict) -> "Budget":
        """Recreate a Budget object from dict (parse RM strings)."""
        total_budget = float(str(data["total_budget"]).replace("RM", ""))
        budget = Budget(trip_name, total_budget)
        budget.categories = {
            cat: float(str(amt).replace("RM", "")) for cat, amt in data["categories"].items()
        }
        return budget
