import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json

def load_itineraries():
    """Loads a dictionary of itineraries from a JSON file."""
    try:
        with open("itineraries.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty dictionary if the file doesn't exist or is invalid


def save_itineraries(itineraries):
    """Saves the dictionary of itineraries to a JSON file."""
    with open("itineraries.json", "w") as file:
        json.dump(itineraries, file, indent=4)

class ItineraryGUI:
    def __init__(self, root, trip_name, itineraries):
        self.root = root
        self.trip_name = trip_name
        self.itineraries = itineraries  # dict[str, list[dict]]

        self.root.title(f"Itinerary Builder - {self.trip_name}")
        self.root.configure(bg="#121212")

        # Apply the same ttk dark styling as the budget app
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        relief="flat", background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", font=("Segoe UI", 11), background="#121212", foreground="white")
        style.configure("TEntry", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")
        style.configure("TCombobox", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")

        # Inputs frame for trip details
        frame_trip_details = tk.Frame(root, bg="#121212")
        frame_trip_details.pack(pady=10)

        ttk.Label(frame_trip_details, text="Trip Title:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.trip_title_entry = ttk.Entry(frame_trip_details, width=25)
        self.trip_title_entry.insert(0, trip_name)
        self.trip_title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Inputs frame for adding itinerary items
        frame_add_event = tk.Frame(root, bg="#121212")
        frame_add_event.pack(pady=10)

        ttk.Label(frame_add_event, text="Event Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.event_type_combo = ttk.Combobox(frame_add_event,
                                             values=["Activity", "Hotel", "Transportation", "Dining", "Other"],
                                             width=22)
        self.event_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.event_type_combo.set("Activity")

        ttk.Label(frame_add_event, text="Event Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.event_name_entry = ttk.Entry(frame_add_event, width=25)
        self.event_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_add_event, text="Date:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.event_date_entry = ttk.Entry(frame_add_event, width=25)
        self.event_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_add_event, text="Time:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.event_time_entry = ttk.Entry(frame_add_event, width=25)
        self.event_time_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_add_event, text="Location:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.event_location_entry = ttk.Entry(frame_add_event, width=25)
        self.event_location_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons frame
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ Add Event", command=self.add_event).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="✏️ Edit Event", command=self.edit_event).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="🗑️ Delete Event", command=self.delete_event).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(root, text="💾 Save Itinerary", command=self.save_itinerary).pack(pady=10)

        # Display area for itinerary items
        self.itinerary_listbox = tk.Listbox(root, height=15, width=70,
                                            bg="#1f1f1f", fg="white",
                                            selectbackground="#333333", font=("Segoe UI", 11))
        self.itinerary_listbox.pack(pady=10)

        ttk.Button(root, text="⬅️ Go Back", command=self.go_back).pack(pady=10)

        self.view_itinerary()

    # Methods
    def add_event(self):
        event_type = self.event_type_combo.get()
        event_name = self.event_name_entry.get().strip()
        event_date = self.event_date_entry.get().strip()
        event_time = self.event_time_entry.get().strip()
        event_location = self.event_location_entry.get().strip()

        if not all([event_name, event_date, event_time, event_location]):
            messagebox.showerror("Error", "All event fields must be filled out!")
            return

        new_event = {
            'type': event_type,
            'name': event_name,
            'date': event_date,
            'time': event_time,
            'location': event_location
        }

        if self.trip_name not in self.itineraries:
            self.itineraries[self.trip_name] = []

        self.itineraries[self.trip_name].append(new_event)
        self.save_itinerary()
        self.view_itinerary()
        messagebox.showinfo("Success", "Event added successfully!")

        # Clear fields
        self.event_name_entry.delete(0, tk.END)
        self.event_date_entry.delete(0, tk.END)
        self.event_time_entry.delete(0, tk.END)
        self.event_location_entry.delete(0, tk.END)

    def edit_event(self):
        try:
            selection_index = self.itinerary_listbox.curselection()[0]
            selected_event = self.itineraries[self.trip_name][selection_index]

            new_name = simpledialog.askstring("Edit Event", f"Edit name for '{selected_event['name']}'?",
                                              initialvalue=selected_event['name'])
            new_date = simpledialog.askstring("Edit Event", f"Edit date for '{selected_event['date']}'?",
                                              initialvalue=selected_event['date'])
            new_time = simpledialog.askstring("Edit Event", f"Edit time for '{selected_event['time']}'?",
                                              initialvalue=selected_event['time'])
            new_location = simpledialog.askstring("Edit Event", f"Edit location for '{selected_event['location']}'?",
                                                  initialvalue=selected_event['location'])

            if new_name:
                selected_event['name'] = new_name
            if new_date:
                selected_event['date'] = new_date
            if new_time:
                selected_event['time'] = new_time
            if new_location:
                selected_event['location'] = new_location

            self.save_itinerary()
            self.view_itinerary()
            messagebox.showinfo("Success", "Event updated!")

        except IndexError:
            messagebox.showwarning("No Selection", "Please select an event to edit.")

    def delete_event(self):
        try:
            selection_index = self.itinerary_listbox.curselection()[0]
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?")
            if confirm:
                del self.itineraries[self.trip_name][selection_index]
                self.save_itinerary()
                self.view_itinerary()
                messagebox.showinfo("Deleted", "Event deleted successfully!")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select an event to delete.")

    def save_itinerary(self):
        save_itineraries(self.itineraries)

    def view_itinerary(self):
        self.itinerary_listbox.delete(0, tk.END)
        if self.trip_name in self.itineraries:
            for event in self.itineraries[self.trip_name]:
                display_text = f"[{event['date']} | {event['time']}] {event['name']} ({event['type']}) at {event['location']}"
                self.itinerary_listbox.insert(tk.END, display_text)

    def go_back(self):
        self.root.destroy()


# =========================================================================
# ITINERARY MENU CLASS
# This class manages the main menu for creating and managing trips.
# =========================================================================

class ItineraryMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("🗺️ Travel Plans")
        self.root.configure(bg="#121212")

        self.itineraries = load_itineraries()  # dict[str, list]

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", background="#121212", foreground="white")

        # Title
        title = ttk.Label(root, text="🗺️ Manage Travel Plans", font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)

        # Listbox for existing plans
        frame = tk.Frame(root, bg="#121212")
        frame.pack(pady=10, fill="both", expand=True)

        self.listbox = tk.Listbox(frame, height=12, bg="#1f1f1f", fg="white",
                                  selectbackground="#333333", font=("Segoe UI", 11))
        self.listbox.pack(side="left", fill="both", expand=True, padx=10)

        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="➕ Add New Plan", command=self.add_plan).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="✏️ Open Plan", command=self.open_plan).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="🗑 Delete Plan", command=self.delete_plan).grid(row=0, column=2, padx=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for trip_name in self.itineraries.keys():
            self.listbox.insert(tk.END, trip_name)

    def add_plan(self):
        trip_name = simpledialog.askstring("New Plan", "Enter trip name:", parent=self.root)
        if not trip_name:
            return
        if trip_name in self.itineraries:
            messagebox.showerror("Error", f"A plan named '{trip_name}' already exists.")
            return

        self.itineraries[trip_name] = []
        save_itineraries(self.itineraries)
        self.refresh_list()

        # Open the new plan automatically after creation
        win = tk.Toplevel(self.root)
        ItineraryGUI(win, trip_name, self.itineraries)

    def open_plan(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a plan to open.")
            return
        trip_name = self.listbox.get(selection[0])
        win = tk.Toplevel(self.root)
        ItineraryGUI(win, trip_name, self.itineraries)

    def delete_plan(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a plan to delete.")
            return
        trip_name = self.listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Delete plan '{trip_name}'?")
        if confirm:
            del self.itineraries[trip_name]
            save_itineraries(self.itineraries)
            self.refresh_list()


# Main entry point for the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ItineraryMenu(root)
    root.mainloop()
