import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.controllers.packageController import PackingController
from src.modules.package import PackingList
from src.utils.file import load_packing_lists, save_packing_lists


class PackingListGUI:
    """open generate packing lists and control menu"""

    def __init__(self, root):
        self.root = root
        self.root.title("📦 Generate Packing List")
        self.root.geometry("900x900")
        self.root.configure(bg="#121212")

        self.controller = PackingController()
        self.current_list = None

        # ttk
        self.setup_styles()

        # create menu
        self.create_input_frame()
        self.create_display_frame()
        self.create_button_frame()

    def setup_styles(self):
        """theme"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        relief="flat", background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", font=("Segoe UI", 11), background="#121212", foreground="white")
        style.configure("TEntry", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")
        style.configure("TCombobox", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")

    def create_input_frame(self):
        """Create Input Parameter Framework"""
        input_frame = tk.Frame(self.root, bg="#121212")
        input_frame.pack(pady=10, padx=20, fill="x")

        # title
        title = ttk.Label(input_frame, text="📦 Generate Packing List",
                          font=("Segoe UI", 20, "bold"))
        title.pack(pady=10)

        # Input Grid
        grid_frame = tk.Frame(input_frame, bg="#121212")
        grid_frame.pack()

        # travel duration
        ttk.Label(grid_frame, text="Travel Duration:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.duration_var = tk.StringVar(value="7")
        duration_spinbox = ttk.Spinbox(grid_frame, from_=1, to=30, textvariable=self.duration_var, width=20)
        duration_spinbox.grid(row=0, column=1, padx=5, pady=5)

        # type of destination
        style = ttk.Style()
        style.configure("TCombobox", foreground="black", font=("Segoe UI", 11))
        ttk.Label(grid_frame, text="Destination Type:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.destination_var = tk.StringVar()
        destination_combo = ttk.Combobox(grid_frame, textvariable=self.destination_var, width=21)
        destination_combo['values'] = ('Beach', 'Mountain', 'City', 'Countryside')
        destination_combo['state'] = 'readonly'
        destination_combo.set('City')
        destination_combo.grid(row=1, column=1, padx=5, pady=5)

        # weather
        style = ttk.Style()
        style.configure("TCombobox", foreground="black", font=("Segoe UI", 11))
        ttk.Label(grid_frame, text="Weather:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.weather_var = tk.StringVar()
        weather_combo = ttk.Combobox(grid_frame, textvariable=self.weather_var, width=21)
        weather_combo['values'] = ('Sunny', 'Rainy', 'Cold', 'Mild')
        weather_combo['state'] = 'readonly'
        weather_combo.set('Mild')
        weather_combo.grid(row=2, column=1, padx=5, pady=5)

        # Number of travelers
        ttk.Label(grid_frame, text="Number of travelers:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.travelers_var = tk.StringVar(value="1")
        travelers_spinbox = ttk.Spinbox(grid_frame, from_=1, to=10, textvariable=self.travelers_var, width=20)
        travelers_spinbox.grid(row=3, column=1, padx=5, pady=5)

        # button
        button_row = tk.Frame(grid_frame, bg="#121212")
        button_row.grid(row=4, column=0, columnspan=2, pady=10)

        style = ttk.Style()
        style.configure("White.TButton", background="white", foreground="black")
        generate_btn = ttk.Button(button_row, text="🎯 Generate Packing List", command=self.generate_list,
                                  style="White.TButton")
        generate_btn.pack(side="left", padx=5)

        view_saved_btn = ttk.Button(button_row, text="📂 View Saved Lists", command=self.show_saved_lists,
                                    style="White.TButton")
        view_saved_btn.pack(side="left", padx=5)

    def create_display_frame(self):
        """create display frame"""
        display_frame = tk.Frame(self.root, bg="#121212")
        display_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # list info
        info_frame = tk.Frame(display_frame, bg="#121212")
        info_frame.pack(fill="x", pady=5)

        self.info_label = ttk.Label(info_frame, text="⬆ Click the Generate button to create the packing list ⬆",
                                    font=("Segoe UI", 12))
        self.info_label.pack()

        # create treeview show item list
        tree_frame = tk.Frame(display_frame, bg="#121212")
        tree_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=('Category', 'Quantity', 'Packed'), show='tree headings',
                                 height=15)
        self.tree.heading('#0', text='Item Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Packed', text='Packed')

        self.tree.column('#0', width=200)
        self.tree.column('Category', width=120, anchor="center")
        self.tree.column('Quantity', width=80, anchor="center")
        self.tree.column('Packed', width=80, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind('<Double-1>', self.toggle_packed_status)

        # add item frame
        add_frame = tk.Frame(display_frame, bg="#121212")
        add_frame.pack(fill="x", pady=5)

        row_frame = tk.Frame(add_frame, bg="#121212")
        row_frame.pack(anchor="center")

        style = ttk.Style()
        style.configure("White.TEntry", fieldbackground="white", background="white", foreground="black")

        ttk.Label(row_frame, text="Add Item:").pack(side="left", padx=5)
        self.new_item_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=self.new_item_var, width=20, style="White.TEntry").pack(side="left", padx=5)

        ttk.Label(row_frame, text="Category:").pack(side="left", padx=5)
        self.new_category_var = tk.StringVar()
        category_combo = ttk.Combobox(row_frame, textvariable=self.new_category_var, width=15)
        category_combo['values'] = ('Clothing', 'Toiletries', 'Electronics', 'Documents', 'Medicines', 'Others')
        style.configure("TCombobox", fieldbackground="white", background="white")
        category_combo.pack(side="left", padx=5)

        style.configure("White.TButton", background="white", foreground="black", padding=(8, 1))
        ttk.Button(row_frame, text="➕ Add", command=self.add_custom_item, style="White.TButton").pack(side="left", padx=5)
        ttk.Button(row_frame, text="🗑️ Delete", command=self.delete_item, style="White.TButton").pack(side="left", padx=5)

    def create_button_frame(self):
        """create bottom button frame"""
        button_frame = tk.Frame(self.root, bg="#121212")
        button_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("White.TButton", background="white", foreground="black")
        ttk.Button(button_frame, text="💾 Save List", command=self.save_list, style="White.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="⬅️ Back to Menu", command=self.go_back, style="White.TButton").grid(row=0, column=2, padx=10)

    def show_saved_lists(self):
        """show saved lists"""
        saved_lists_window = tk.Toplevel(self.root)
        SavedListsSelector(saved_lists_window, self)

    def load_saved_list(self, packing_list: PackingList):
        """load saved lists"""
        self.current_list = packing_list

        self.duration_var.set(str(packing_list.duration))
        self.destination_var.set(packing_list.destination_type)
        self.weather_var.set(packing_list.weather)
        self.travelers_var.set(str(packing_list.travelers))

        self.update_display()

        messagebox.showinfo("Loading successful", f"Trip loaded: {packing_list.trip_name}", parent=self.root)

    def generate_list(self):
        """generate packing list"""
        try:
            duration = int(self.duration_var.get())
            destination = self.destination_var.get()
            weather = self.weather_var.get()
            travelers = int(self.travelers_var.get())

            if not destination or not weather:
                messagebox.showwarning("Input error", "Please select destination type and weather！", parent=self.root)
                return

            # trip_name = simpledialog.askstring("Trip Name", "Enter a name for this trip:", parent=self.root)
            # if not trip_name:
            #     trip_name = f"{destination.capitalize()} Trip"

            self.current_list = self.controller.generate_packing_list(destination, duration, weather, travelers)

            self.update_display()

            messagebox.showinfo("Generation successful",
                                f"Your packing list has been generated with {len(self.current_list.items)} items!",
                                parent=self.root)

        except ValueError:
            messagebox.showerror("Input error", "Please enter a valid number of days and number of travelers！", parent=self.root)

    def update_display(self):
        """update display content"""
        if not self.current_list:
            return

        info_text = f"Destination: {self.current_list.destination_type} | Duration: {self.current_list.duration} | "
        info_text += f"Weather: {self.current_list.weather} | Number of travelers: {self.current_list.travelers} | "
        info_text += f"Progress: {self.current_list.packed_items}/{self.current_list.total_items} "
        info_text += f"({self.current_list.packing_progress:.1f}%)"
        self.info_label.config(text=info_text)

        for item in self.tree.get_children():
            self.tree.delete(item)

        categories = self.current_list.get_items_by_category()

        for category, items in categories.items():
            category_id = self.tree.insert('', 'end', text=f"📂 {category}", values=('', '', ''))
            for item in items:
                packed_status = "✅" if item.is_packed else "❌"
                self.tree.insert(category_id, 'end', text=item.name,
                                 values=(item.category, item.quantity, packed_status))

        for item in self.tree.get_children():
            self.tree.item(item, open=True)

    def toggle_packed_status(self, event):
        """change pack status to True"""
        if not self.current_list:
            return

        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")

        if not item_text.startswith("📂"):
            success = self.current_list.toggle_packed(item_text)
            if success:
                self.update_display()

    def add_custom_item(self):
        """add custom item"""
        if not self.current_list:
            messagebox.showwarning("WARNING!", "Please create a packing list！", parent=self.root)
            return

        item_name = self.new_item_var.get().strip()
        category = self.new_category_var.get().strip()

        if not item_name or not category:
            messagebox.showwarning("Input error", "Please enter the item name and category！", parent=self.root)
            return

        self.current_list.add_item(item_name, category)
        self.update_display()

        self.new_item_var.set("")
        self.new_category_var.set("")

        messagebox.showinfo("Added successfully", f"Items added: {item_name}", parent=self.root)

    def delete_item(self):
        """delete selected item"""
        if not self.current_list:
            return

        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Incorrect selection", "Please select the items to be deleted！", parent=self.root)
            return

        selected_item = selection[0]
        item_text = self.tree.item(selected_item, "text")

        if not item_text.startswith("📂"):
            confirm = messagebox.askyesno("Confirm delete", f"Confirm delete of item?: '{item_text}'", parent=self.root)
            if confirm:
                success = self.current_list.remove_item(item_text)
                if success:
                    self.update_display()
                    messagebox.showinfo("Delete successful", f"Deleted items: {item_text}", parent=self.root)

    def save_list(self):
        """save list"""
        duration = int(self.duration_var.get())
        destination = self.destination_var.get()
        weather = self.weather_var.get()
        travelers = int(self.travelers_var.get())

        if not self.current_list:
            messagebox.showwarning("WARNING!", "Please create a packing list!", parent=self.root)
            return

        trip_name = simpledialog.askstring("Trip Name", "Enter a name for this trip:", parent=self.root)
        if not trip_name:
            trip_name = f"{destination.capitalize()} Trip"

        # self.current_list = self.controller.generate_packing_list(
        #     destination, duration, weather, travelers, trip_name=trip_name
        # )

        # list_name = self.current_list.trip_name
        self.current_list.trip_name = trip_name
        success = self.controller.save_packing_list(self.current_list)

        if success:
            messagebox.showinfo("Saved successfully", f"The trip '{trip_name}' has been saved!", parent=self.root)
        else:
            messagebox.showerror("Save failed", "An error occurred while saving the trip!", parent=self.root)

    def go_back(self):
        """back to menu"""
        self.root.destroy()
        from src.gui.mainmenu import MainApp
        root = tk.Tk()
        MainApp(root)
        root.mainloop()

class SavedListsSelector:
    """saved lists selector"""

    def __init__(self, root, parent_gui):
        self.root = root
        self.parent_gui = parent_gui
        self.controller = PackingController()

        self.root.title("📚 Select a saved list")
        self.root.geometry("900x800")
        self.root.configure(bg="#121212")

        self.setup_styles()
        self.create_interface()
        self.load_saved_lists()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        relief="flat", background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", font=("Segoe UI", 11), background="#121212", foreground="white")

    def create_interface(self):
        title_frame = tk.Frame(self.root, bg="#121212")
        title_frame.pack(pady=10, fill="x")

        title = ttk.Label(title_frame, text="📚 Select the list to load", font=("Segoe UI", 20, "bold"))
        title.pack()

        list_frame = tk.Frame(self.root, bg="#121212")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(list_frame, columns=('Destination', 'Duration', 'Weather', 'Progress'),
                                 show='tree headings', height=15)
        self.tree.heading('#0', text='Trip Name')
        self.tree.heading('Destination', text='Destination')
        self.tree.heading('Duration', text='Duration')
        self.tree.heading('Weather', text='Weather')
        self.tree.heading('Progress', text='Progress')

        self.tree.column('#0', width=150)
        self.tree.column('Destination', width=100, anchor="center")
        self.tree.column('Duration', width=80, anchor="center")
        self.tree.column('Weather', width=80, anchor="center")
        self.tree.column('Progress', width=120, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind('<Double-1>', self.load_selected_list)

        button_frame = tk.Frame(self.root, bg="#121212")
        button_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("White.TButton", background="white", foreground="black", font=("Segoe UI", 11), padding=(8, 5))
        ttk.Button(button_frame, text="✅ Load List", command=self.load_selected_list,
                   style="White.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="🗑️ Delete List", command=self.delete_selected_list,
                   style="White.TButton").grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="❌ Cancel", command=self.close_window,
                   style="White.TButton").grid(row=0, column=2, padx=10)

    def load_saved_lists(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            saved_lists = self.controller.load_all_lists()

            if not saved_lists:
                self.tree.insert('', 'end', text="No saved lists at this time", values=('', '', '', ''))
                return

            for packing_list in saved_lists.values():
                progress_text = f"{packing_list.packed_items}/{packing_list.total_items} ({packing_list.packing_progress:.1f}%)"
                self.tree.insert('', 'end', text=packing_list.trip_name,
                                 values=(packing_list.destination_type,
                                         f"{packing_list.duration} days",
                                         packing_list.weather,
                                         progress_text))

        except Exception as e:
            messagebox.showerror("Loading error", f"An error occurred while loading the manifest: {str(e)}", parent=self.root)

    def load_selected_list(self, event=None):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Incorrect selection", "Please select the list to load!", parent=self.root)
            return

        selected_item = selection[0]
        list_name = self.tree.item(selected_item, "text")

        if list_name == "No saved lists at this time":
            return

        try:
            saved_lists = self.controller.load_all_lists()
            if list_name in saved_lists:
                # load main menu
                self.parent_gui.load_saved_list(saved_lists[list_name])
                self.close_window()
            else:
                messagebox.showerror("Error", "The specified list cannot be found!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Loading error", f"An error occurred while loading the manifest: {str(e)}", parent=self.root)

    def delete_selected_list(self):
        """delete selected list"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Incorrect selection", "Please select the list to delete!", parent=self.root)
            return

        selected_item = selection[0]
        list_name = self.tree.item(selected_item, "text")

        if list_name == "No saved lists at this time":
            return

        # check delete
        confirm = messagebox.askyesno("Confirm deletion", f"Are you sure you want to delete the list '{list_name}' ?\nThis action cannot be undone!", parent=self.root)
        if confirm:
            try:
                success = self.controller.delete_list(list_name)
                if success:
                    messagebox.showinfo("Delete successful", f"List '{list_name}' deleted successfully!", parent=self.root)
                    self.load_saved_lists()  # load saved list again
                else:
                    messagebox.showerror("Delete failed", "The list does not exist or deletion failed!", parent=self.root)
            except Exception as e:
                messagebox.showerror("Delete Error", f"An error occurred while deleting the list: {str(e)}", parent=self.root)

    def close_window(self):
        """close window"""
        self.root.destroy()


class PackingListViewer:
    """list viewer"""

    def __init__(self, root, packing_list: PackingList):
        self.root = root
        self.packing_list = packing_list