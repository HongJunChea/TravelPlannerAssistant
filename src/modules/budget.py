from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Budget:
    trip_name: str
    total_budget: float
    categories: Dict[str, float] = field(default_factory=dict)

    def add_category(self, category: str, amount: float) -> None:
        """Add a new category with allocated amount"""
        self.categories[category] = amount

    def update_category(self, category: str, amount: float) -> None:
        """Update existing category allocation"""
        if category in self.categories:
            self.categories[category] = amount
        else:
            raise ValueError(f"Category '{category}' not found!")

    def calculate_total(self) -> float:
        """Calculate the total allocated budget"""
        return sum(self.categories.values())

    def remaining_budget(self) -> float:
        """Check the remaining balance"""
        return self.total_budget - self.calculate_total()
