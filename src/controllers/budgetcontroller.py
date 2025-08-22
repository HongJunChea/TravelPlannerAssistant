from src.modules.budget import Budget
from src.utils.file import load_budgets, save_budgets

def run_budget_estimator():
    # load budgets from JSON and convert dicts -> Budget objects
    raw_budgets = load_budgets()
    budgets: dict[str, Budget] = {
        trip: Budget.from_dict(trip, data) for trip, data in raw_budgets.items()
    }

    while True:
        print("\n=== Travel Budget Estimator ===")
        print("1. Add New Budget Plan")
        print("2. Edit Existing Budget Plan")
        print("3. View Budget Plans")
        print("4. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        # Add New Budget
        if choice == "1":
            trip_name = input("Enter trip name: ").strip()
            try:
                total_budget = float(input("Enter total budget (RM): "))
            except ValueError:
                print("Invalid input, please enter a number.")
                continue

            budget = Budget(trip_name, total_budget)

            # Add categories interactively
            while True:
                category = input("Enter category (e.g., Hotel, Food, Transport): ").strip()
                try:
                    amount = float(input(f"Enter budget for {category} (RM): "))
                except ValueError:
                    print("Invalid input, must be a number.")
                    continue

                # controller logic: add category
                budget.categories[category] = amount

                more = input("Add another category? (y/n): ").lower()
                if more != "y":
                    break

            budgets[trip_name] = budget
            save_budgets({t: b.to_dict() for t, b in budgets.items()})
            print("Budget plan saved!")

        # ---------------- Edit Budget ----------------
        elif choice == "2":
            if not budgets:
                print("No budget plans found.")
                continue

            print("\nAvailable Trips:")
            for trip in budgets.keys():
                print(f"- {trip}")

            trip_choice = input("Enter trip name to edit: ").strip()
            if trip_choice not in budgets:
                print("⚠ Trip not found.")
                continue

            budget = budgets[trip_choice]

            print(f"\nCurrent Categories: {budget.categories}")
            category = input("Enter category to update (or add new): ").strip()

            try:
                new_amount = float(input("Enter new amount (RM): "))
                # controller logic: update / add category
                budget.categories[category] = new_amount

                budgets[trip_choice] = budget
                save_budgets({t: b.to_dict() for t, b in budgets.items()})
                print("Category updated!")
            except ValueError:
                print("Invalid input, must be a number.")

        # ---------------- View Budgets ----------------
        elif choice == "3":
            if not budgets:
                print("No budget plans available.")
                continue

            print("\n=== Budget Plans ===")
            for trip, budget in budgets.items():
                print(f"\nTrip: {trip}")
                print(f"Total Budget: RM{budget.total_budget:.2f}")
                print(f"Allocated: RM{budget.allocated:.2f}")
                print(f"Remaining: RM{budget.remaining:.2f}")
                print("Categories:")
                for cat, amt in budget.categories.items():
                    print(f"  - {cat}: RM{amt:.2f}")

        # ---------------- Back ----------------
        elif choice == "4":
            print("⬅ Returning to Main Menu...")
            break

        else:
            print("⚠ Invalid choice, try again.")
