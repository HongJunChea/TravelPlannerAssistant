# TravelPlannerAssistant


## Features

- **Main Menu**: Central hub for accessing all travel planning tools in a simple, intuitive interface.
- **Itinerary Builder**: Create, edit, and organize daily travel plans with destinations and activities.
- **Packing List Generator**: Automatically generate and manage packing checklists, with progress tracking.
- **Budget Estimator**: Estimate travel expenses and manage costs for transportation, accommodation, and activities.

## Screenshots

*Main Menu*
ss

*Itinerary Builder*
ss

*Packing List Generator*
ss

*Budget Estimator*
ss

## Authors

- **Chea Hong Jun** - cheahj-wm23@student.tarc.edu.my
- **Ng Zhe Wei** - ngzw-wm23@student.tarc.edu.my
- **Teoh Yong Ming** - teohym-wm23@student.tarc.edu.my

## Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.11 or above**
- Works on Windows / macOS / Linux

### Required Python Libraries

The application requires the following Python packages, which are included in the standard library or can be installed via pip:
* `tkinter` (Usually included with Python standard library)
* `tkcalendar` (Needs to be installed)

## Installation

1.  **Clone or Download the Repository**
    ```bash
    git clone https://github.com/HongJunChea/TravelPlannerAssistant.git  
    cd TravelPlannerAssistant
    ```

2.  **Install the Required Package**
    The `tkcalendar` library is needed. Install it using pip:
    ```bash
    pip install tkcalendar
    ```

## How to Run the Application

1.  Navigate to the project directory in your terminal or command prompt.
2.  Run the main Python file:
    ```bash
    python main.py  
    ```

## How to Use

1.  **Main Menu:** Launch the app to start. Choose between the three tools.

2.  **Itinerary Builder:**
    -   Enter trip details (Title, Dates, Location).
    -  	Use **"+ Add Activity"** to schedule your days with times and locations.
    -   Use **Update** or **Remove** to edit your plan.

3.  **Packing List Generator:**
    -   Answer questions about your trip (destination, weather, etc.).
    -   The app **auto-generates** a categorized list.
    -   **Check off items** as you pack them and add your own custom items.

4.  **Budget Estimator:**
    -   Set your **Total Budget**.
    -   **"Add Category"** for expenses like Flights, Food, etc., and allocate funds to each.
    -   Track your spending against the allocated amounts.

## Project Structure

```
TravelPlannerAssistant/
├── .venv/                    # Python virtual environment 
├── src/                      # Main source code directory
│   ├── controllers/          # Business logic layer 
│   │   ├── __init__.py
│   │   ├── BudgetController.py  # Manages budget calculations & data
│   │   ├── ItineraryBuilder.py  # Manages itinerary logic & sequencing
│   │   └── PackageController.py # Manages packing list generation
│   ├── datafiles/            # Directory for JSON data storage
│   │   ├── budgets.json      # Stores all saved budget data
│   │   └── itineraries.json  # Stores all saved itinerary data
│   ├── gui/                  # Presentation UI layer 
│   │   ├── __init__.py
│   │   ├── BudgetGUI.py      # Tkinter window for the Budget Estimator
│   │   ├── ItineraryGUI.py   # Tkinter window for the Itinerary Builder
│   │   ├── MainMenu.py       # Tkinter window for the main navigation menu
│   │   └── PackageGUI.py     # Tkinter window for the Packing List Generator
│   ├── modules/              # Data models & core classes
│   │   ├── __init__.py
│   │   ├── Budget.py         # Defines the Budget class and its properties
│   │   ├── Itinerary.py      # Defines the Itinerary and Activity classes
│   │   ├── Package.py        # Defines the PackingList and Item classes
│   │   └── Trip.py           # Defines a core Trip class (Inheritance)
│   └── utils/                # Utility/helper functions
│       ├── __init__.py
│       └── file.py           # Contains functions for reading/writing JSON files
└── requirements.txt          # List of Python dependencies
```

### Development Guidelines

- Follow the existing MVC architecture pattern
- Use Tkinter for all UI components
- Maintain the dark theme consistency
- Add appropriate error handling
- Update tests when adding new features

## Acknowledgments

- Thanks to our course instructor for guidance.
- Built with the Tkinter library.
