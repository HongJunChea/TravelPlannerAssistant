import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.modules.itinerary import Itinerary
from src.utils.file import load_itineraries, save_itineraries


class ItineraryMenu:
    def __init__(self, root):
        self.root = root
        self.itineraries = load_itineraries()
        self.current_itinerary: str | None = None

        # Set window size a bit taller
        root.geometry("1100x500")
        root.configure(bg="#000000")

        # Dark theme styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Black.TFrame", background="#000000")
        style.configure("Black.TEntry",
                        fieldbackground="#000000",
                        foreground="white",
                        insertcolor="white")
        style.configure("Black.TCombobox",
                        fieldbackground="#000000",
                        background="#000000",
                        foreground="white")

        # Layout: split left form + right saved itineraries
        self.main_frame = ttk.Frame(root, style="Black.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= LEFT SIDE: Trip details =================
        left_frame = ttk.Frame(self.main_frame, style="Black.TFrame")
        left_frame.pack(side="left", fill="both", expand=True, padx=20)

        self.header_label = ttk.Label(
            left_frame,
            text="🗺️ Travel Itinerary Builder",
            font=("Segoe UI", 20, "bold"),
            background="#000000",
            foreground="white"
        )
        self.header_label.pack(pady=10)

        # Trip details frame
        self.input_frame = ttk.Frame(left_frame, style="Black.TFrame")
        self.input_frame.pack(fill="x", pady=20)

        # Row 1: Trip Title
        ttk.Label(self.input_frame, text="Trip Title:", background="#000000", foreground="white").grid(
            row=0, column=0, padx=5, pady=10, sticky="e"
        )
        self.trip_title_entry = ttk.Entry(self.input_frame, style="Black.TEntry", width=50)  # longer field
        self.trip_title_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Row 2: Location
        ttk.Label(self.input_frame, text="Location:", background="#000000", foreground="white").grid(
            row=1, column=0, padx=5, pady=10, sticky="e"
        )
        self.location_entry = ttk.Entry(self.input_frame, style="Black.TEntry", width=30)
        self.location_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Row 3: Start Date + End Date
        ttk.Label(self.input_frame, text="Start Date:", background="#000000", foreground="white").grid(
            row=2, column=0, padx=5, pady=10, sticky="e"
        )
        self.start_date_entry = ttk.Entry(self.input_frame, style="Black.TEntry", width=20)
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        ttk.Label(self.input_frame, text="End Date:", background="#000000", foreground="white").grid(
            row=3, column=0, padx=5, pady=10, sticky="e"
        )
        self.end_date_entry = ttk.Entry(self.input_frame, style="Black.TEntry", width=20)
        self.end_date_entry.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        # Row 4: Trip Type
        ttk.Label(self.input_frame, text="Type of Trip:", background="#000000", foreground="white").grid(
            row=4, column=0, padx=5, pady=10, sticky="e"
        )
        self.trip_type_combo = ttk.Combobox(self.input_frame,
                                            values=["General", "Business", "Vacation", "Adventure", "Family", "Other"],
                                            state="readonly", width=18)
        self.trip_type_combo.set("General")
        self.trip_type_combo.grid(row=4, column=1, padx=5, pady=10, sticky="w")

        # Bottom button bar
        self.button_frame = ttk.Frame(left_frame, style="Black.TFrame")
        self.button_frame.pack(fill="x", pady=15)

        self.save_button = ttk.Button(self.button_frame, text="💾 Save Itinerary", command=self.save_itinerary)
        self.save_button.pack(side="left", padx=10)

        self.update_button = ttk.Button(self.button_frame, text="✏️ Update Itinerary", command=self.update_itinerary)
        self.update_button.pack(side="left", padx=10)

        self.delete_button = ttk.Button(self.button_frame, text="🗑️ Delete Itinerary", command=self.delete_itinerary)
        self.delete_button.pack(side="left", padx=10)

        self.reset_button = ttk.Button(self.button_frame, text="🔄 Reset", command=self.reset_fields)
        self.reset_button.pack(side="left", padx=10)

        self.exit_button = ttk.Button(self.button_frame, text="❌ Exit", command=self.root.destroy)
        self.exit_button.pack(side="right", padx=10)

        # ================= RIGHT SIDE: Saved itineraries =================
        right_frame = ttk.Frame(self.main_frame, style="Black.TFrame", width=250)
        right_frame.pack(side="right", fill="y", padx=10)
        right_frame.pack_propagate(False)  # prevent frame from shrinking to fit children

        lbl = ttk.Label(right_frame, text="📂 Saved Itineraries",
                        background="#000000", foreground="white", font=("Segoe UI", 12, "bold"))
        lbl.pack(pady=5)

        self.itinerary_listbox = tk.Listbox(
            right_frame,
            bg="black",
            fg="white",
            height=25,
            width=30,  # make it wider in characters
            selectmode="single"
        )
        self.itinerary_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.itinerary_listbox.bind("<<ListboxSelect>>", self.load_selected_itinerary)

        self.refresh_itinerary_list()

    # ================= FUNCTIONS =================

    def reset_fields(self):
        """Clear input fields (reset)."""
        self.trip_title_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.trip_type_combo.set("General")
        self.current_itinerary = None
        self.itinerary_listbox.selection_clear(0, tk.END)

    def refresh_itinerary_list(self):
        """Refresh listbox with saved itineraries."""
        self.itinerary_listbox.delete(0, tk.END)
        for name in self.itineraries.keys():
            self.itinerary_listbox.insert(tk.END, name)

    def validate_date(self, date_text):
        """Check if date is in YYYY-mm-dd format."""
        if not date_text:
            return True
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def save_itinerary(self):
        """Create and save a new itinerary."""
        trip_title = self.trip_title_entry.get().strip()
        if not trip_title:
            messagebox.showwarning("Missing Info", "Trip Title is required.")
            return

        if not self.validate_date(self.start_date_entry.get()):
            messagebox.showerror("Invalid Date", "Start Date must be in YYYY-mm-dd format.")
            return
        if not self.validate_date(self.end_date_entry.get()):
            messagebox.showerror("Invalid Date", "End Date must be in YYYY-mm-dd format.")
            return

        list_name = trip_title

        # Handle duplicate
        if list_name in self.itineraries:
            overwrite = messagebox.askyesno("Overwrite?",
                                            f"Itinerary '{list_name}' already exists. Overwrite?")
            if not overwrite:
                return

        itinerary = Itinerary(
            list_name=list_name,
            trip_title=trip_title,
            location=self.location_entry.get(),
            start_date=self.start_date_entry.get(),
            end_date=self.end_date_entry.get(),
            trip_type=self.trip_type_combo.get(),
            activities=[]
        )

        self.itineraries[list_name] = itinerary
        save_itineraries(self.itineraries)
        self.refresh_itinerary_list()
        messagebox.showinfo("Saved", f"Itinerary '{list_name}' saved successfully.")

    def update_itinerary(self):
        if not self.current_itinerary:
            messagebox.showwarning("No Selection", "Select an itinerary from the list to update.")
            return

        if not self.validate_date(self.start_date_entry.get()):
            messagebox.showerror("Invalid Date", "Start Date must be in YYYY-mm-dd format.")
            return
        if not self.validate_date(self.end_date_entry.get()):
            messagebox.showerror("Invalid Date", "End Date must be in YYYY-mm-dd format.")
            return

        itinerary = Itinerary(
            list_name=self.current_itinerary,
            trip_title=self.trip_title_entry.get(),
            location=self.location_entry.get(),
            start_date=self.start_date_entry.get(),
            end_date=self.end_date_entry.get(),
            trip_type=self.trip_type_combo.get(),
            activities=[]
        )

        self.itineraries[self.current_itinerary] = itinerary
        save_itineraries(self.itineraries)
        self.refresh_itinerary_list()
        messagebox.showinfo("Updated", f"Itinerary '{self.current_itinerary}' updated successfully.")

    def delete_itinerary(self):
        list_name = self.itinerary_listbox.get(tk.ANCHOR)
        if not list_name:
            messagebox.showwarning("No Selection", "Select an itinerary to delete.")
            return

        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{list_name}'?")
        if not confirm:
            return

        if list_name in self.itineraries:
            del self.itineraries[list_name]
            save_itineraries(self.itineraries)
            self.refresh_itinerary_list()
            self.reset_fields()
            messagebox.showinfo("Deleted", f"Itinerary '{list_name}' deleted successfully.")

    def load_selected_itinerary(self, event):
        selection = self.itinerary_listbox.curselection()
        if not selection:
            return
        list_name = self.itinerary_listbox.get(selection[0])
        itinerary = self.itineraries[list_name]

        self.reset_fields()
        self.current_itinerary = list_name

        self.trip_title_entry.insert(0, itinerary.trip_title)
        self.location_entry.insert(0, itinerary.location)
        self.start_date_entry.insert(0, itinerary.start_date)
        self.end_date_entry.insert(0, itinerary.end_date)
        self.trip_type_combo.set(itinerary.trip_type)
