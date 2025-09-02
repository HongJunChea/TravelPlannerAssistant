def display_main_menu():
    """Displays the main menu options to the user."""
    print("\nTravel Planner Assistant")
    print("--------------------------")
    print("1. Add Itinerary")
    print("2. Update Itinerary")
    print("3. View Itinerary")
    print("4. Exit")
    return input("Enter your choice: ")


def display_list_of_itineraries(itineraries):
    """Displays a numbered list of all existing itinerary titles."""
    print("\nList of Itineraries:")
    print("--------------------")
    if not itineraries:
        print("No itineraries found.")
        return False
    for i, trip in enumerate(itineraries):
        print(f"{i + 1}. {trip['title']}")
    return True


def add_itinerary(itineraries):
    """
    Implements the flow for adding a new itinerary (Flowchart 1).
    """
    while True:
        print("\nDisplay Add Itinerary Menu")
        print("----------------------------")
        title = input("Input trip title: ")
        location = input("Input location: ")
        start_date = input("Input start date: ")
        end_date = input("Input end date: ")
        event_type = input("Input type of event/trip: ")

        new_itinerary = {
            'title': title,
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'event_type': event_type
        }

        itineraries.append(new_itinerary)

        print("\nDisplay overall itinerary inserted.")
        print(f"Trip: {title} | Location: {location} | Dates: {start_date} to {end_date}")

        add_another = input("Add another itinerary? (Yes/No): ").lower()
        if add_another != 'yes':
            break

    print("Back to main menu.")


def update_itinerary(itineraries):
    """
    Implements the flow for updating an existing itinerary (Flowchart 2).
    """
    if not display_list_of_itineraries(itineraries):
        print("Back to main menu.")
        return

    while True:
        try:
            choice = int(input("Select one itinerary (enter the number): ")) - 1
            if 0 <= choice < len(itineraries):
                selected_itinerary = itineraries[choice]

                while True:
                    print("\nSelect what to update:")
                    print("1. Title")
                    print("2. Location")
                    print("3. Start and End Date")
                    print("4. Done Updating this Itinerary")
                    update_choice = input("Enter your choice: ")

                    if update_choice == '1':
                        selected_itinerary['title'] = input("Input new trip title: ")
                    elif update_choice == '2':
                        selected_itinerary['location'] = input("Input new location: ")
                    elif update_choice == '3':
                        selected_itinerary['start_date'] = input("Input new start date: ")
                        selected_itinerary['end_date'] = input("Input new end date: ")
                    elif update_choice == '4':
                        break
                    else:
                        print("Invalid choice. Please try again.")

                    print("\nDisplay overall itinerary updated.")

                update_another_itinerary = input("Update another itinerary? (Yes/No): ").lower()
                if update_another_itinerary != 'yes':
                    break
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Back to main menu.")


def view_itinerary(itineraries):
    """
    Implements the flow for viewing an existing itinerary (Flowchart 3).
    """
    if not display_list_of_itineraries(itineraries):
        print("Back to main menu.")
        return

    while True:
        try:
            choice = int(input("Select one itinerary (enter the number): ")) - 1
            if 0 <= choice < len(itineraries):
                selected_itinerary = itineraries[choice]
                print("\nDisplay the details of the itinerary:")
                print("---------------------------------")
                print(f"Title: {selected_itinerary['title']}")
                print(f"Location: {selected_itinerary['location']}")
                print(f"Dates: {selected_itinerary['start_date']} to {selected_itinerary['end_date']}")
                print(f"Event Type: {selected_itinerary['event_type']}")
            else:
                print("Invalid number. Please try again.")

            view_another = input("View another itinerary? (Yes/No): ").lower()
            if view_another != 'yes':
                break

        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Back to main menu.")


# Main program loop
def main():
    itineraries = []

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