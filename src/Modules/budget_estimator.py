import json
import os

# class
class Budget:
    def __init__(self, trip_name, total_budget):
        self.trip_name = trip_name
        self.total_budget = total_budget
        self.categories = {}

    def add_category(self, category, amount):
        self.categories[category] = amount

    def update_category(self, category, amount):
        if category in self.categories:
            self.categories[category] = amount
        else:
            raise ValueError(f"Category '{category}' not found!")

    def calculate_total(self):
        return sum(self.categories.values())

    def remaining_budget(self):
        return self.total_budget - self.calculate_total()


# files
def load_budgets(filename="budgets.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_budgets(budgets, filename="budgets.json"):
    with open(filename, "w") as f:
        json.dump(budgets, f, indent=4)


# main
def run_budget_estimator():
    budgets = load_budgets()

    while True:
        print("\n=== Travel Budget Estimator ===")
        print("1. Add New Budget Plan")
        print("2. Edit Existing Budget Plan")
        print("3. View Budget Plan")
        print("4. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            trip_name = input("Enter trip name: ").strip()
            try:
                total_budget = float(input("Enter total budget: "))
            except ValueError:
                print("Invalid input, please enter a number.")
                continue

            budget = Budget(trip_name, total_budget)

            while True:
                category = input("Enter category (e.g., Hotel, Food, Transport): ").strip()
                try:
                    amount = float(input(f"Enter budget for {category}: "))
                except ValueError:
                    print("Invalid input, must be a number.")
                    continue

                budget.add_category(category, amount)

                more = input("Add another category? (y/n): ").lower()
                if more != "y":
                    break

            budgets[trip_name] = {
                "total_budget": budget.total_budget,
                "categories": budget.categories
            }
            save_budgets(budgets)
            print("Budget plan saved!")

        elif choice == "2":
            if not budgets:
                print("No budget plans found.")
                continue

            print("\nAvailable Trips:")
            for i, trip in enumerate(budgets.keys(), 1):
                print(f"{i}. {trip}")

            trip_choice = input("Enter trip name to edit: ").strip()
            if trip_choice not in budgets:
                print("Trip not found.")
                continue

            budget_data = budgets[trip_choice]
            budget = Budget(trip_choice, budget_data["total_budget"])
            budget.categories = budget_data["categories"]

            print("\nCurrent Categories:", budget.categories)
            category = input("Enter category to update: ").strip()

            try:
                new_amount = float(input("Enter new amount: "))
                budget.update_category(category, new_amount)
                budgets[trip_choice] = {
                    "total_budget": budget.total_budget,
                    "categories": budget.categories
                }
                save_budgets(budgets)
                print("Category updated!")
            except ValueError as e:
                print(f"{e}")

        elif choice == "3":
            if not budgets:
                print("No budget plans available.")
                continue

            print("\nAvailable Trips:")
            for trip, data in budgets.items():
                print(f"- {trip}: Total = {data['total_budget']}, Categories = {data['categories']}")

        elif choice == "4":
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid choice, try again.")
