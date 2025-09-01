from src.modules.budget import Budget
from src.utils.file import load_budgets, save_budgets

class BudgetController:
    def __init__(self):
        self.budgets = load_budgets()  # dict[str, Budget]

    # Trip management
    def get_trips(self):
        return list(self.budgets.keys())

    def add_trip(self, trip_name):
        if trip_name in self.budgets:
            raise ValueError(f"Trip '{trip_name}' already exists")
        self.budgets[trip_name] = Budget(trip_name=trip_name, total_budget=0, categories={})
        save_budgets(self.budgets)

    def delete_trip(self, trip_name):
        if trip_name not in self.budgets:
            raise ValueError(f"Trip '{trip_name}' not found")
        del self.budgets[trip_name]
        save_budgets(self.budgets)

    def get_trip(self, trip_name):
        return self.budgets.get(trip_name)

    # Budget details
    def update_total(self, trip_name, total):
        self.budgets[trip_name].total_budget = total
        save_budgets(self.budgets)

    def add_category(self, trip_name, category, amount):
        self.budgets[trip_name].categories[category] = amount
        save_budgets(self.budgets)

    def edit_category(self, trip_name, category, amount):
        if category not in self.budgets[trip_name].categories:
            raise ValueError(f"Category '{category}' not found")
        self.budgets[trip_name].categories[category] = amount
        save_budgets(self.budgets)

    def delete_category(self, trip_name, category):
        if category not in self.budgets[trip_name].categories:
            raise ValueError(f"Category '{category}' not found")
        del self.budgets[trip_name].categories[category]
        save_budgets(self.budgets)
