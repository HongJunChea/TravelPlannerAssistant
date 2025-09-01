import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.modules.itinerary import Itinerary, Activity
from src.utils.file import load_itineraries, save_itineraries
from tkcalendar import DateEntry


class ItineraryMenu:
    def __init__(self, root):
        self.root = root
        self.itineraries = load_itineraries()
        self.current_itinerary: str | None = None
        self.activities = []

        root.geometry("1050x800")
        root.configure(bg="#000000")

        # Dark theme styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Black.TFrame", background="#000000")
        style.configure("Black.TEntry",
                        fieldbackground="#000000",
                        foreground="white",
                        insertcolor="white")
        style.configure("Treeview",
                        background="black",
                        foreground="white",
                        fieldbackground="black",
                        rowheight=24)
        style.configure("Treeview.Heading",
                        background="black",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))

        # ================= MAIN LAYOUT =================
        self.main_frame = ttk.Frame(root, style="Black.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ================= TOP SECTION (Trip details + Saved itineraries) =================
        top_frame = ttk.Frame(self.main_frame, style="Black.TFrame")
        top_frame.pack(fill="x", pady=5)

        # ---- Trip Details (LEFT) ----
        trip_frame = ttk.Frame(top_frame, style="Black.TFrame")
        trip_frame.pack(side="left", fill="x", expand=True, padx=10)

        self.header_label = ttk.Label(
            trip_frame,
            text="🗺️ Travel Itinerary Builder",
            font=("Segoe UI", 18, "bold"),
            background="#000000",
            foreground="white"
        )
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(trip_frame, text="Trip Title:", background="#000000", foreground="white").grid(
            row=1, column=0, padx=5, pady=6, sticky="e")
        self.trip_title_entry = ttk.Entry(trip_frame, style="Black.TEntry", width=30)
        self.trip_title_entry.grid(row=1, column=1, padx=5, pady=6, sticky="w")

        ttk.Label(trip_frame, text="Location:", background="#000000", foreground="white").grid(
            row=2, column=0, padx=5, pady=6, sticky="e")
        self.location_entry = ttk.Entry(trip_frame, style="Black.TEntry", width=25)
        self.location_entry.grid(row=2, column=1, padx=5, pady=6, sticky="w")

        ttk.Label(trip_frame, text="Start Date:", background="#000000", foreground="white").grid(
            row=3, column=0, padx=5, pady=6, sticky="e")
        self.start_date_entry = DateEntry(trip_frame, width=12, date_pattern="yyyy-mm-dd")
        self.start_date_entry.grid(row=3, column=1, padx=5, pady=6, sticky="w")

        ttk.Label(trip_frame, text="End Date:", background="#000000", foreground="white").grid(
            row=4, column=0, padx=5, pady=6, sticky="e")
        self.end_date_entry = DateEntry(trip_frame, width=12, date_pattern="yyyy-mm-dd")
        self.end_date_entry.grid(row=4, column=1, padx=5, pady=6, sticky="w")

        ttk.Label(trip_frame, text="Type of Trip:", background="#000000", foreground="white").grid(
            row=5, column=0, padx=5, pady=6, sticky="e")
        self.trip_type_combo = ttk.Combobox(trip_frame,
                                            values=["General", "Company", "Vacation", "Adventure", "Family", "Other"],
                                            state="readonly", width=15)
        self.trip_type_combo.set("General")
        self.trip_type_combo.grid(row=5, column=1, padx=5, pady=6, sticky="w")

        # ---- Saved Itineraries (RIGHT) ----
        right_frame = ttk.Frame(top_frame, style="Black.TFrame", width=260)
        right_frame.pack(side="right", fill="y", padx=10)
        right_frame.pack_propagate(False)

        lbl = ttk.Label(right_frame, text="📂 Saved Itineraries",
                        background="#000000", foreground="white", font=("Segoe UI", 12, "bold"))
        lbl.pack(pady=5)

        self.itinerary_listbox = tk.Listbox(
            right_frame,
            bg="black",
            fg="white",
            height=14,
            width=28,
            selectmode="single"
        )
        self.itinerary_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.itinerary_listbox.bind("<<ListboxSelect>>", self.load_selected_itinerary)

        # ================= MIDDLE SECTION: Activities =================
        activity_frame = ttk.Frame(self.main_frame, style="Black.TFrame")
        activity_frame.pack(fill="both", expand=True, pady=10)

        # Custom header for Activities (bigger, black bg, white text)
        header_label = tk.Label(
            activity_frame,
            text="Activities",
            bg="black",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            anchor="center",
            pady=6
        )
        header_label.pack(fill="x")

        columns = ("Date", "Start Time", "End Time", "Location", "Detail", "Notes")
        self.activity_tree = ttk.Treeview(activity_frame, columns=columns, show="headings")

        # ✅ Updated column widths
        col_widths = [60, 80, 80, 100, 150, 120]
        for col, width in zip(columns, col_widths):
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(
                col,
                width=width,
                anchor="center" if col in ("Date", "Start Time", "End Time") else "w"
            )

        self.activity_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # ================= BOTTOM SECTION: Activity Buttons =================
        act_btns = ttk.Frame(self.main_frame, style="Black.TFrame")
        act_btns.pack(fill="x", pady=5)
        ttk.Button(act_btns, text="➕ Add Activity", command=self.add_activity_popup).pack(side="left", padx=5)
        ttk.Button(act_btns, text="✏️ Update Activity", command=self.update_activity_popup).pack(side="left", padx=5)
        ttk.Button(act_btns, text="❌ Remove Activity", command=self.remove_activity).pack(side="left", padx=5)

        # ================= BOTTOM SECTION: Itinerary Buttons =================
        self.button_frame = ttk.Frame(self.main_frame, style="Black.TFrame")
        self.button_frame.pack(side="bottom", fill="x", pady=10)  # ✅ keeps buttons at bottom

        self.save_button = ttk.Button(self.button_frame, text="➕ Add Itinerary", command=self.save_itinerary)
        self.save_button.pack(side="left", padx=8)

        self.update_button = ttk.Button(self.button_frame, text="✏️ Update Itinerary", command=self.update_itinerary)
        self.update_button.pack(side="left", padx=8)

        self.delete_button = ttk.Button(self.button_frame, text="🗑 Delete Itinerary", command=self.delete_itinerary)
        self.delete_button.pack(side="left", padx=8)

        self.reset_button = ttk.Button(self.button_frame, text="🔄 Reset", command=self.reset_fields)
        self.reset_button.pack(side="left", padx=8)

        self.exit_button = ttk.Button(self.button_frame, text="❌ Exit", command=self.root.destroy)
        self.exit_button.pack(side="right", padx=8)

        # Fill itineraries
        self.refresh_itinerary_list()

    # ================= FUNCTIONS =================
    def validate_dates(self, start_date, end_date):
        try:
            sd = datetime.strptime(start_date, "%Y-%m-%d")
            ed = datetime.strptime(end_date, "%Y-%m-%d")
            if ed < sd:
                messagebox.showerror("Invalid Dates", "End Date cannot be before Start Date.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Dates", "Please enter valid dates.")
            return False

    def validate_activity_date(self, date):
        """ Ensure activity date is within itinerary range """
        try:
            act_date = datetime.strptime(date, "%Y-%m-%d")
            sd = datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d")
            ed = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d")
            if not (sd <= act_date <= ed):
                messagebox.showerror("Invalid Date",
                                     f"Activity date {date} must be between trip dates ({sd.date()} - {ed.date()}).")
                return False
            return True
        except Exception:
            return False

    def validate_times(self, start_time, end_time):
        try:
            st = datetime.strptime(start_time, "%H:%M")
            et = datetime.strptime(end_time, "%H:%M")
            if et < st:
                messagebox.showerror("Invalid Time", "End Time cannot be before Start Time.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Time Format", "Please use HH:MM format.")
            return False

    def reset_fields(self):
        self.trip_title_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.trip_type_combo.set("General")
        self.activities.clear()
        for i in self.activity_tree.get_children():
            self.activity_tree.delete(i)
        self.current_itinerary = None
        self.itinerary_listbox.selection_clear(0, tk.END)

    def refresh_itinerary_list(self):
        self.itinerary_listbox.delete(0, tk.END)
        for name in sorted(self.itineraries.keys()):
            self.itinerary_listbox.insert(tk.END, name)

    def add_activity_popup(self):
        self.activity_popup(mode="add")

    def update_activity_popup(self):
        selection = self.activity_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an activity to update.")
            return
        self.activity_popup(mode="update", selection=selection[0])

    def activity_popup(self, mode="add", selection=None):
        popup = tk.Toplevel(self.root)
        popup.title("Activity")
        popup.configure(bg="black")

        tk.Label(popup, text="Date:", bg="black", fg="white").grid(row=0, column=0, pady=5, sticky="e")
        date_entry = DateEntry(popup, width=12, date_pattern="yyyy-mm-dd")
        date_entry.grid(row=0, column=1, pady=5)

        tk.Label(popup, text="Start Time (HH:MM):", bg="black", fg="white").grid(row=1, column=0, pady=5, sticky="e")
        start_entry = tk.Entry(popup, bg="black", fg="white")
        start_entry.grid(row=1, column=1, pady=5)

        tk.Label(popup, text="End Time (HH:MM):", bg="black", fg="white").grid(row=2, column=0, pady=5, sticky="e")
        end_entry = tk.Entry(popup, bg="black", fg="white")
        end_entry.grid(row=2, column=1, pady=5)

        tk.Label(popup, text="Location:", bg="black", fg="white").grid(row=3, column=0, pady=5, sticky="e")
        location_entry = tk.Entry(popup, bg="black", fg="white", width=30)
        location_entry.grid(row=3, column=1, pady=5)

        tk.Label(popup, text="Detail:", bg="black", fg="white").grid(row=4, column=0, pady=5, sticky="e")
        detail_entry = tk.Entry(popup, bg="black", fg="white", width=30)
        detail_entry.grid(row=4, column=1, pady=5)

        tk.Label(popup, text="Notes:", bg="black", fg="white").grid(row=5, column=0, pady=5, sticky="e")
        notes_entry = tk.Entry(popup, bg="black", fg="white", width=30)
        notes_entry.grid(row=5, column=1, pady=5)

        # Pre-fill if updating
        if mode == "update" and selection:
            values = self.activity_tree.item(selection, "values")
            date_entry.set_date(values[0])
            start_entry.insert(0, values[1])
            end_entry.insert(0, values[2])
            location_entry.insert(0, values[3])
            detail_entry.insert(0, values[4])
            notes_entry.insert(0, values[5])

        def save_activity():
            date = date_entry.get()
            start_time = start_entry.get()
            end_time = end_entry.get()

            if not self.validate_activity_date(date):
                return
            if not self.validate_times(start_time, end_time):
                return

            activity = Activity(
                date=date,
                start_time=start_time,
                end_time=end_time,
                location=location_entry.get(),
                detail=detail_entry.get(),
                notes=notes_entry.get()
            )

            if mode == "add":
                self.activities.append(activity)
            elif mode == "update" and selection:
                idx = self.activity_tree.index(selection)
                self.activities[idx] = activity

            self.refresh_activity_table()
            popup.destroy()

        btn_text = "Update" if mode == "update" else "Add"
        tk.Button(popup, text=btn_text, command=save_activity, bg="black", fg="white").grid(row=6, column=0,
                                                                                           columnspan=2, pady=10)

    def refresh_activity_table(self):
        """ Refresh and auto-sort by date & time """
        self.activity_tree.delete(*self.activity_tree.get_children())
        sorted_acts = sorted(self.activities, key=lambda a: (
            datetime.strptime(a.date, "%Y-%m-%d"),
            datetime.strptime(a.start_time, "%H:%M")
        ))
        self.activities = sorted_acts
        for act in sorted_acts:
            self.activity_tree.insert("", "end", values=(
                act.date, act.start_time, act.end_time,
                act.location, act.detail, act.notes
            ))

    def remove_activity(self):
        selection = self.activity_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an activity to remove.")
            return
        for item in selection:
            idx = self.activity_tree.index(item)
            del self.activities[idx]
            self.activity_tree.delete(item)

    def save_itinerary(self):
        trip_title = self.trip_title_entry.get().strip()
        if not trip_title:
            messagebox.showwarning("Missing Info", "Trip Title is required.")
            return
        if not self.validate_dates(self.start_date_entry.get(), self.end_date_entry.get()):
            return

        list_name = trip_title

        if list_name in self.itineraries:
            confirm = messagebox.askyesno(
                "Overwrite Itinerary",
                f"An itinerary named '{list_name}' already exists.\nDo you want to overwrite it?"
            )
            if not confirm:
                return

        itinerary = Itinerary(
            list_name=list_name,
            trip_title=trip_title,
            location=self.location_entry.get(),
            start_date=self.start_date_entry.get(),
            end_date=self.end_date_entry.get(),
            trip_type=self.trip_type_combo.get(),
            activities=self.activities
        )

        self.itineraries[list_name] = itinerary
        save_itineraries(self.itineraries)
        self.refresh_itinerary_list()
        messagebox.showinfo("Saved", f"Itinerary '{list_name}' saved successfully.")

    def update_itinerary(self):
        if not self.current_itinerary:
            messagebox.showwarning("No Selection", "Select an itinerary from the list to update.")
            return
        if not self.validate_dates(self.start_date_entry.get(), self.end_date_entry.get()):
            return

        itinerary = Itinerary(
            list_name=self.current_itinerary,
            trip_title=self.trip_title_entry.get(),
            location=self.location_entry.get(),
            start_date=self.start_date_entry.get(),
            end_date=self.end_date_entry.get(),
            trip_type=self.trip_type_combo.get(),
            activities=self.activities
        )

        self.itineraries[self.current_itinerary] = itinerary
        save_itineraries(self.itineraries)
        self.refresh_itinerary_list()
        self.refresh_activity_table()  # FIX: ensures activities reload properly
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
        self.start_date_entry.set_date(itinerary.start_date)
        self.end_date_entry.set_date(itinerary.end_date)
        self.trip_type_combo.set(itinerary.trip_type)

        self.activities = list(itinerary.activities)
        self.refresh_activity_table()
