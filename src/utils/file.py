import json
import os
from typing import Dict

def load_budgets(filename: str = "datafiles/budgets.json") -> Dict:
    """Load budgets from a JSON file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_budgets(budgets: Dict, filename: str = "datafiles/budgets.json") -> None:
    """Validate and save budgets to a JSON file."""
    validated = {}

    for trip_name, data in budgets.items():
        if not isinstance(data, dict):
            raise ValueError(f"Invalid data for trip '{trip_name}': Expected dict, got {type(data)}")

        if "total_budget" not in data or "categories" not in data:
            raise ValueError(f"Missing keys in trip '{trip_name}'. Required: total_budget, categories")

        if not isinstance(data["total_budget"], (int, float)):
            raise ValueError(f"total_budget for '{trip_name}' must be a number")

        if not isinstance(data["categories"], dict):
            raise ValueError(f"categories for '{trip_name}' must be a dictionary")

        validated[trip_name] = {
            "total_budget": float(data["total_budget"]),
            "categories": data["categories"]
        }

    # Ensure folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        json.dump(validated, f, indent=4)
