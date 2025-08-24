import json
import os
from typing import Dict
from src.modules.budget import Budget

def load_budgets(filename: str = "datafiles/budgets.json") -> Dict[str, Budget]:
    if not os.path.exists(filename):
        return {}

    with open(filename, "r") as f:
        raw_data = json.load(f)

    return {
        trip_name: Budget.from_dict(trip_name, data)
        for trip_name, data in raw_data.items()
    }

def save_budgets(budgets: Dict[str, Budget], filename: str = "datafiles/budgets.json") -> None:
    """Serialize Budget objects and save to JSON."""
    serializable = {trip_name: budget.to_dict() for trip_name, budget in budgets.items()}

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=4)
