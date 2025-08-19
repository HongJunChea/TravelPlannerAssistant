from src.modules.budget import Budget
from src.utils.file import load_budgets, save_budgets


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
            print("✅ Budget plan saved!")

        elif choice == "2":
            if not budgets:
                print("No budget plans found.")
                continue

            print("\nAvailable Trips:")
            for trip in budgets.keys():
                print(f"- {trip}")

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

            print("\n=== Budget Plans ===")
            for trip, data in budgets.items():
                if isinstance(data, dict) and "total_budget" in data and "categories" in data:
                    print(f"\nTrip: {trip}")
                    print(f"Total Budget: {data['total_budget']}")
                    print(f"Categories: {data['categories']}")
                else:
                    print(f"Skipping invalid entry for trip '{trip}'")


        elif choice == "4":
            print("⬅ Returning to Main Menu...")
            break

        else:
            print("Invalid choice, try again.")
