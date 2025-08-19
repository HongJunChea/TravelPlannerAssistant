# ===== Main Menu for Travel Planner Assistant App =====

from src.Modules.budget_estimator import run_budget_estimator
# from itinerary_builder import run_itinerary       # (other teammate)
# from packing_list import run_packing_list         # (other teammate)
# from emergency_contact import run_emergency_list  # (other teammate)

def main_menu():
    while True:
        print("\n=== Travel Planner Assistant App ===")
        print("1. Itinerary Builder")
        print("2. Packing List Generator")
        print("3. Travel Budget Estimator")
        print("4. Emergency Contact List")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            print("Itinerary Builder module not yet implemented.")  # placeholder
            # run_itinerary()
        elif choice == "2":
            print("Packing List Generator module not yet implemented.")  # placeholder
            # run_packing_list()
        elif choice == "3":
            run_budget_estimator()
        elif choice == "4":
            print("Emergency Contact List module not yet implemented.")  # placeholder
            # run_emergency_list()
        elif choice == "5":
            print("Goodbye")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
