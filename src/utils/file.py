import json
import os
from typing import Dict

def load_budgets(filename: str = "datafiles/budgets.json") -> Dict:
    """Load budgets from a file"""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_budgets(budgets: Dict, filename: str = "datafiles/budgets.json") -> None:
    """Save budgets to file"""
    with open(filename, "w") as f:
        json.dump(budgets, f, indent=4)
