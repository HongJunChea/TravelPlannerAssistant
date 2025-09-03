from src.modules.itinerary import Itinerary   # your dataclass version
from typing import List


def display_main_menu():
    """Displays the main menu options to the user."""
    print("\nTravel Planner Assistant")
    print("--------------------------")
    print("1. Add Itinerary")
    print("2. Update Itinerary")
    print("3. View Itinerary")
    print("4. Exit")
    return input("Enter your choice: ")


def display_list_of_itineraries(itineraries: List[Itinerary]):
    """Displays a numbered list of all existing itineraries."""
    print("\nList of Itineraries:")
    print("--------------------")
    if not itineraries:
        print("No itineraries found.")
        return False
    for i, trip in enumerate(itineraries):
        print(f"{i + 1}. {trip.trip_name}")
    return True


def add_itinerary(itineraries: List[Itinerary]):
    """Flow for adding a new itinerary."""
    while True:
        print("\nDisplay Add Itinerary Menu")
        print("----------------------------")
        trip_name = input("Input trip title: ")
        location = input("Input location: ")
        start_date = input("Input start date: ")
        end_date = input("Input end date: ")
        trip_type = input("Input type of event/trip: ")

        new_itinerary = Itinerary(
            trip_name=trip_name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            trip_type=trip_type,
            activities=[]
        )

        itineraries.append(new_itinerary)

        print("\nDisplay overall itinerary inserted.")
        print(f"Trip: {trip_name} | Location: {location} | Dates: {start_date} to {end_date}")

        add_another = input("Add another itinerary? (Yes/No): ").lower()
        if add_another != 'yes':
            break

    print("Back to main menu.")


def update_itinerary(itineraries: List[Itinerary]):
    """Flow for updating an itinerary."""
    if not display_list_of_itineraries(itineraries):
        print("Back to main menu.")
        return

    while True:
        try:
            choice = int(input("Select one itinerary (enter the number): ")) - 1
            if 0 <= choice < len(itineraries):
                selected = itineraries[choice]

                while True:
                    print("\nSelect what to update:")
                    print("1. Title")
                    print("2. Location")
                    print("3. Start and End Date")
                    print("4. Done Updating this Itinerary")
                    update_choice = input("Enter your choice: ")

                    if update_choice == '1':
                        selected.trip_name = input("Input new trip title: ")
                    elif update_choice == '2':
                        selected.location = input("Input new location: ")
                    elif update_choice == '3':
                        selected.start_date = input("Input new start date: ")
                        selected.end_date = input("Input new end date: ")
                    elif update_choice == '4':
                        break
                    else:
                        print("Invalid choice. Please try again.")

                    print("\nDisplay overall itinerary updated.")

                update_another = input("Update another itinerary? (Yes/No): ").lower()
                if update_another != 'yes':
                    break
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Back to main menu.")


def view_itinerary(itineraries: List[Itinerary]):
    """Flow for viewing an itinerary."""
    if not display_list_of_itineraries(itineraries):
        print("Back to main menu.")
        return

    while True:
        try:
            choice = int(input("Select one itinerary (enter the number): ")) - 1
            if 0 <= choice < len(itineraries):
                selected = itineraries[choice]
                print("\nDisplay the details of the itinerary:")
                print("---------------------------------")
                print(f"Title: {selected.trip_name}")
                print(f"Location: {selected.location}")
                print(f"Dates: {selected.start_date} to {selected.end_date}")
                print(f"Event Type: {selected.trip_type}")
            else:
                print("Invalid number. Please try again.")

            view_another = input("View another itinerary? (Yes/No): ").lower()
            if view_another != 'yes':
                break

        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Back to main menu.")


def main():
    itineraries: List[Itinerary] = []

    while True:
        choice = display_main_menu()

        if choice == '1':
            add_itinerary(itineraries)
        elif choice == '2':
            update_itinerary(itineraries)
        elif choice == '3':
            view_itinerary(itineraries)
        elif choice == '4':
            print("End. Exiting the program. Happy travels!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
