import json
import os


def load_budgets(filename="budgets.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)


def save_budgets(budgets, filename="budgets.json"):
    """
    Save budgets dictionary to JSON with validation.
    Each entry must be in the format:
    {
        "trip_name": {
            "total_budget": float,
            "categories": dict
        }
    }
    """
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

    with open(filename, "w") as f:
        json.dump(validated, f, indent=4)
