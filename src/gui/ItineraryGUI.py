import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime, timedelta
import json
import os
from src.modules.itinerary import Itinerary


class ItineraryMenu:
    """
    Main application class that manages the different frames/screens
    based on the provided flowchart.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("✈️ Travel Itinerary Builder")
        self.root.geometry("800x700")
        self.root.configure(bg="#121212")

        # The filename for saving/loading data
        self.save_dir = "itineraries"
        os.makedirs(self.save_dir, exist_ok=True)

        # Dictionary to hold all created/loaded frames
        self.frames = {}

        # The current itinerary being edited/viewed
        self.current_itinerary: Itinerary = None

        self.setup_styles()
        self.create_frames()
        self.show_frame("main_menu")

    def setup_styles(self):
        """
        Configures the dark theme for the ttk widgets.
        """
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        relief="flat", background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", font=("Segoe UI", 11), background="#121212", foreground="white")
        style.configure("TEntry", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")
        style.configure("TCombobox", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")
        style.configure("Treeview", fieldbackground="#1f1f1f", foreground="white", background="#1f1f1f",
                        font=("Segoe UI", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#1f1f1f", foreground="white")
        style.map("Treeview", background=[('selected', '#333333')], foreground=[('selected', 'white')])

    def create_frames(self):
        """
        Initializes and stores all the main frames for the application.
        """
        # Main Menu Frame
        main_menu_frame = ttk.Frame(self.root, style="TLabel")
        self.frames["main_menu"] = main_menu_frame

        title = ttk.Label(main_menu_frame, text="Main Menu", font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

        ttk.Button(main_menu_frame, text="1. Add Itinerary", command=lambda: self.show_frame("add_itinerary")).pack(
            pady=10, ipadx=50)
        ttk.Button(main_menu_frame, text="2. Update Itinerary",
                   command=lambda: self.show_frame("update_itinerary")).pack(pady=10, ipadx=40)
        ttk.Button(main_menu_frame, text="3. View Itinerary", command=lambda: self.show_frame("view_itinerary")).pack(
            pady=10, ipadx=45)

        # Add Itinerary Frame
        add_frame = ttk.Frame(self.root, style="TLabel")
        self.frames["add_itinerary"] = add_frame
        self.setup_add_frame(add_frame)

        # Update Itinerary Frame
        update_frame = ttk.Frame(self.root, style="TLabel")
        self.frames["update_itinerary"] = update_frame
        self.setup_select_itinerary_frame(update_frame, self.setup_update_frame)

        # View Itinerary Frame
        view_frame = ttk.Frame(self.root, style="TLabel")
        self.frames["view_itinerary"] = view_frame
        self.setup_select_itinerary_frame(view_frame, self.setup_view_frame)

    def show_frame(self, frame_name):
        """
        Hides all frames and shows the selected one.
        """
        for frame in self.frames.values():
            frame.pack_forget()

        frame_to_show = self.frames.get(frame_name)
        if frame_to_show:
            frame_to_show.pack(fill="both", expand=True)

    def setup_add_frame(self, frame):
        """
        Creates the GUI for adding a new itinerary.
        """
        title = ttk.Label(frame, text="Add New Itinerary", font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

        fields_frame = ttk.Frame(frame, style="TLabel")
        fields_frame.pack(pady=10)

        self.add_vars = {
            "title": tk.StringVar(),
            "location": tk.StringVar(),
            "start_date": tk.StringVar(),
            "end_date": tk.StringVar(),
            "trip_type": tk.StringVar()
        }

        labels = ["Trip Title:", "Location:", "Start Date (YYYY-MM-DD):", "End Date (YYYY-MM-DD):", "Type of Trip:"]
        entries = ["title", "location", "start_date", "end_date", "trip_type"]

        for i, (label_text, var_name) in enumerate(zip(labels, entries)):
            ttk.Label(fields_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if var_name == "trip_type":
                combo = ttk.Combobox(fields_frame, textvariable=self.add_vars[var_name], width=27)
                combo['values'] = ('Leisure', 'Business', 'Adventure', 'Family')
                combo['state'] = 'readonly'
                combo.grid(row=i, column=1, padx=5, pady=5)
            else:
                ttk.Entry(fields_frame, textvariable=self.add_vars[var_name], width=30).grid(row=i, column=1, padx=5,
                                                                                             pady=5)

        ttk.Button(frame, text="Add Itinerary", command=self.add_new_itinerary).pack(pady=10)
        ttk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu")).pack(pady=5)

    def add_new_itinerary(self):
        """
        Saves the new itinerary and prompts the user to add another.
        """
        try:
            trip_data = {key: var.get() for key, var in self.add_vars.items()}

            if not all(trip_data.values()):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            start_date_obj = datetime.strptime(trip_data["start_date"], "%Y-%m-%d")
            end_date_obj = datetime.strptime(trip_data["end_date"], "%Y-%m-%d")
            if start_date_obj > end_date_obj:
                messagebox.showerror("Date Error", "Start date cannot be after the end date.")
                return

                # Create a new Itinerary object
            new_itinerary = Itinerary(
                list_name=f"{trip_data['title'].replace(' ', '_')}.json",
                trip_title=trip_data["title"],
                location=trip_data["location"],
                start_date=trip_data["start_date"],
                end_date=trip_data["end_date"],
                trip_type=trip_data["trip_type"]
            )

            # Save the itinerary
            filename = new_itinerary.list_name
            save_path = os.path.join(self.save_dir, filename)
            with open(save_path, 'w') as f:
                json.dump(new_itinerary.to_dict(), f, indent=4)

            messagebox.showinfo("Success", "Itinerary added successfully!")

            # Prompt to add another
            if messagebox.askyesno("Add More?", "Would you like to add another itinerary?"):
                for var in self.add_vars.values():
                    var.set("")
                self.show_frame("add_itinerary")
            else:
                self.show_frame("main_menu")

        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")

    def setup_select_itinerary_frame(self, frame, next_action):
        """
        Generates a generic frame for selecting an itinerary from a list.
        """
        title = ttk.Label(frame, text="Select Itinerary", font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

        self.tree_frame = ttk.Frame(frame, style="TLabel")
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.itinerary_tree = ttk.Treeview(self.tree_frame, columns=('Location', 'Dates'), show='headings')
        self.itinerary_tree.heading('#0', text='Trip Title')
        self.itinerary_tree.heading('Location', text='Location')
        self.itinerary_tree.heading('Dates', text='Dates')
        self.itinerary_tree.column('#0', width=200)
        self.itinerary_tree.column('Location', width=150)
        self.itinerary_tree.column('Dates', width=200)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.itinerary_tree.yview)
        self.itinerary_tree.configure(yscrollcommand=scrollbar.set)

        self.itinerary_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.itinerary_tree.bind('<Double-1>', lambda event: self.load_selected_itinerary(next_action))

        select_btn = ttk.Button(frame, text="Select Itinerary",
                                command=lambda: self.load_selected_itinerary(next_action))
        select_btn.pack(pady=10)

        ttk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu")).pack(pady=5)

        # This function will load the data for the treeview
        self.load_all_itineraries()

    def load_all_itineraries(self):
        """
        Loads all saved itineraries and populates the Treeview.
        """
        for item in self.itinerary_tree.get_children():
            self.itinerary_tree.delete(item)

        try:
            files = [f for f in os.listdir(self.save_dir) if f.endswith('.json')]
            if not files:
                self.itinerary_tree.insert('', 'end', text="No saved itineraries.", values=('', ''))
                return

            for file_name in files:
                file_path = os.path.join(self.save_dir, file_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    dates = f"{data.get('start_date', 'N/A')} to {data.get('end_date', 'N/A')}"
                    self.itinerary_tree.insert('', 'end', text=data.get('trip_title', 'N/A'),
                                               values=(data.get('location', 'N/A'), dates),
                                               tags=(file_name,))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files: {e}")

    def load_selected_itinerary(self, next_action):
        """
        Loads the selected itinerary from the Treeview and proceeds to the next frame.
        """
        selected_item = self.itinerary_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an itinerary first.")
            return

        file_name = self.itinerary_tree.item(selected_item, 'tags')[0]
        file_path = os.path.join(self.save_dir, file_name)

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Use from_dict to create an Itinerary object
                self.current_itinerary = Itinerary.from_dict(list_name=file_name, data=data)

                # Call the function to setup the next frame
            next_action(file_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load itinerary: {e}")

    def setup_view_frame(self, file_name):
        """
        Generates the GUI to view itinerary details.
        """
        view_frame = ttk.Frame(self.root, style="TLabel")
        self.frames["view_itinerary_details"] = view_frame

        title = ttk.Label(view_frame, text=f"Viewing: {self.current_itinerary.trip_title}",
                          font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

        info_text = f"Destination: {self.current_itinerary.location}\n" \
                    f"Dates: {self.current_itinerary.start_date} to {self.current_itinerary.end_date}\n" \
                    f"Type: {self.current_itinerary.trip_type}"
        ttk.Label(view_frame, text=info_text, font=("Segoe UI", 12)).pack(pady=10)

        # Treeview for activities
        activity_tree_frame = ttk.Frame(view_frame, style="TLabel")
        activity_tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.activity_tree = ttk.Treeview(activity_tree_frame, columns=('Activity', 'Time', 'Notes'), show='headings')
        self.activity_tree.heading('Activity', text='Activity')
        self.activity_tree.heading('Time', text='Time')
        self.activity_tree.heading('Notes', text='Notes')
        self.activity_tree.pack(fill="both", expand=True)

        for activity in self.current_itinerary.activities:
            self.activity_tree.insert('', 'end', values=(activity.description, activity.time, activity.notes))

        ttk.Button(view_frame, text="View another Itinerary", command=lambda: self.show_frame("view_itinerary")).pack(
            pady=10)
        ttk.Button(view_frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu")).pack(pady=5)

        self.show_frame("view_itinerary_details")

    def setup_update_frame(self, file_name):
        """
        Generates the GUI to update an itinerary.
        """
        update_frame = ttk.Frame(self.root, style="TLabel")
        self.frames["update_itinerary_details"] = update_frame

        title = ttk.Label(update_frame, text=f"Updating: {self.current_itinerary.trip_title}",
                          font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

        # Fields for updating trip details
        update_fields_frame = ttk.Frame(update_frame, style="TLabel")
        update_fields_frame.pack(pady=10)

        self.update_vars = {
            "title": tk.StringVar(value=self.current_itinerary.trip_title),
            "location": tk.StringVar(value=self.current_itinerary.location),
            "start_date": tk.StringVar(value=self.current_itinerary.start_date),
            "end_date": tk.StringVar(value=self.current_itinerary.end_date),
            "trip_type": tk.StringVar(value=self.current_itinerary.trip_type)
        }

        labels = ["Trip Title:", "Location:", "Start Date (YYYY-MM-DD):", "End Date (YYYY-MM-DD):", "Type of Trip:"]
        entries = ["title", "location", "start_date", "end_date", "trip_type"]

        for i, (label_text, var_name) in enumerate(zip(labels, entries)):
            ttk.Label(update_fields_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if var_name == "trip_type":
                combo = ttk.Combobox(update_fields_frame, textvariable=self.update_vars[var_name], width=27)
                combo['values'] = ('Leisure', 'Business', 'Adventure', 'Family')
                combo['state'] = 'readonly'
                combo.grid(row=i, column=1, padx=5, pady=5)
            else:
                ttk.Entry(update_fields_frame, textvariable=self.update_vars[var_name], width=30).grid(row=i, column=1,
                                                                                                       padx=5, pady=5)

        ttk.Button(update_frame, text="Update Trip Details", command=lambda: self.update_trip_details(file_name)).pack(
            pady=10)

        # Separator for Activity Management
        ttk.Separator(update_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)
        ttk.Label(update_frame, text="Manage Activities", font=("Segoe UI", 16, "bold")).pack()

        # Activity management controls
        activity_controls = ttk.Frame(update_frame, style="TLabel")
        activity_controls.pack(pady=5)
        self.activity_vars = {
            "description": tk.StringVar(),
            "time": tk.StringVar(),
            "notes": tk.StringVar()
        }

        ttk.Label(activity_controls, text="Description:").grid(row=0, column=0, padx=5)
        ttk.Entry(activity_controls, textvariable=self.activity_vars["description"], width=30).grid(row=0, column=1,
                                                                                                    padx=5)
        ttk.Label(activity_controls, text="Time:").grid(row=0, column=2, padx=5)
        ttk.Entry(activity_controls, textvariable=self.activity_vars["time"], width=10).grid(row=0, column=3, padx=5)
        ttk.Label(activity_controls, text="Notes:").grid(row=0, column=4, padx=5)
        ttk.Entry(activity_controls, textvariable=self.activity_vars["notes"], width=20).grid(row=0, column=5, padx=5)

        ttk.Button(activity_controls, text="Add Activity", command=lambda: self.add_activity(file_name)).grid(row=1,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              pady=5)
        ttk.Button(activity_controls, text="Delete Selected", command=lambda: self.delete_activity(file_name)).grid(
            row=1, column=2, columnspan=2, pady=5)

        # Treeview to display activities
        self.update_activity_tree = ttk.Treeview(update_frame, columns=('Activity', 'Time', 'Notes'), show='headings')
        self.update_activity_tree.heading('Activity', text='Activity')
        self.update_activity_tree.heading('Time', text='Time')
        self.update_activity_tree.heading('Notes', text='Notes')
        self.update_activity_tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.populate_activity_tree()

        ttk.Button(update_frame, text="Update another Itinerary",
                   command=lambda: self.show_frame("update_itinerary")).pack(pady=10)
        ttk.Button(update_frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu")).pack(pady=5)

        self.show_frame("update_itinerary_details")

    def populate_activity_tree(self):
        """
        Populates the activity Treeview in the update frame.
        """
        for item in self.update_activity_tree.get_children():
            self.update_activity_tree.delete(item)

        for i, activity in enumerate(self.current_itinerary.activities):
            self.update_activity_tree.insert('', 'end', values=(activity.description, activity.time, activity.notes),
                                             iid=i)

    def update_trip_details(self, file_name):
        """
        Updates the top-level trip details in the JSON file.
        """
        try:
            # Update the attributes of the current Itinerary object
            self.current_itinerary.trip_title = self.update_vars["title"].get()
            self.current_itinerary.location = self.update_vars["location"].get()
            self.current_itinerary.start_date = self.update_vars["start_date"].get()
            self.current_itinerary.end_date = self.update_vars["end_date"].get()
            self.current_itinerary.trip_type = self.update_vars["trip_type"].get()

            # Save the updated itinerary
            self.save_itinerary_file(file_name)

            messagebox.showinfo("Success", "Trip details updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update trip details: {e}")

    def add_activity(self, file_name):
        """
        Adds a new activity to the current itinerary.
        """
        description = self.activity_vars["description"].get()
        time = self.activity_vars["time"].get()
        notes = self.activity_vars["notes"].get()

        if not description:
            messagebox.showwarning("Input Error", "Activity description cannot be empty.")
            return

            # Add the new activity using the Itinerary object's method
        self.current_itinerary.add_activity(description=description, date=self.current_itinerary.start_date, time=time,
                                            notes=notes)

        self.populate_activity_tree()
        self.save_itinerary_file(file_name)

        self.activity_vars["description"].set("")
        self.activity_vars["time"].set("")
        self.activity_vars["notes"].set("")

    def delete_activity(self, file_name):
        """
        Deletes the selected activity from the current itinerary.
        """
        selected_item = self.update_activity_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an activity to delete.")
            return

        index_to_delete = int(self.update_activity_tree.item(selected_item, 'iid'))

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this activity?")
        if confirm:
            # Delete the activity using the Itinerary object's method
            # Note: This is a simplification; a more robust method might use a unique ID
            del self.current_itinerary.activities[index_to_delete]
            self.populate_activity_tree()
            self.save_itinerary_file(file_name)

    def save_itinerary_file(self, file_name):
        """
        Helper function to save the current itinerary to a file.
        """
        try:
            save_path = os.path.join(self.save_dir, file_name)
            with open(save_path, 'w') as f:
                # Use to_dict() method of the Itinerary object for serialization
                json.dump(self.current_itinerary.to_dict(), f, indent=4)
            messagebox.showinfo("Success", "Itinerary saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save itinerary: {e}")