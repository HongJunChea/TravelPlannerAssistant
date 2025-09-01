import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.controllers.budgetcontroller import BudgetController

def apply_gradient(widget, color1="#0f0f0f", color2="#2a2a2a"):
    """Paint a vertical gradient background on a canvas that resizes with window."""
    canvas = tk.Canvas(widget, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def _draw_gradient(event=None):
        canvas.delete("gradient")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        limit = height
        (r1, g1, b1) = widget.winfo_rgb(color1)
        (r2, g2, b2) = widget.winfo_rgb(color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr >> 8:02x}{ng >> 8:02x}{nb >> 8:02x}"
            canvas.create_line(0, i, width, i, tags=("gradient",), fill=color)

        canvas.lower("gradient")

    canvas.bind("<Configure>", _draw_gradient)
    return canvas


class BudgetGUI:
    def __init__(self, root, trip_name, controller: BudgetController):
        self.root = root
        self.trip_name = trip_name
        self.controller = controller

        self.root.title(f"Budget Plan - {self.trip_name}")
        self.root.geometry("750x600")  # slightly smaller for balance

        # === Gradient Background ===
        bg_canvas = apply_gradient(self.root, "#0f0f0f", "#2a2a2a")

        # === Main container with grid ===
        container = tk.Frame(bg_canvas, bg="#121212", bd=0)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=0)   # inputs + buttons (fixed)
        container.grid_rowconfigure(1, weight=1)   # display box (flex)
        container.grid_rowconfigure(2, weight=0)   # footer (fixed)
        container.grid_columnconfigure(0, weight=1)

        # === Card: Inputs ===
        input_card = tk.Frame(container, bg="#1c1c1c", bd=0)
        input_card.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        ttk.Label(input_card, text="Trip Name:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.trip_entry = ttk.Entry(input_card, width=25)
        self.trip_entry.insert(0, trip_name)
        self.trip_entry.grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(input_card, text="Total Budget:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.total_entry = ttk.Entry(input_card, width=25)
        self.total_entry.insert(0, str(self.controller.get_trip(trip_name).total_budget))
        self.total_entry.grid(row=1, column=1, padx=8, pady=6)

        ttk.Label(input_card, text="Category:").grid(row=2, column=0, sticky="e", padx=8, pady=6)
        self.cat_entry = ttk.Entry(input_card, width=25)
        self.cat_entry.grid(row=2, column=1, padx=8, pady=6)

        ttk.Label(input_card, text="Amount:").grid(row=3, column=0, sticky="e", padx=8, pady=6)
        self.amount_entry = ttk.Entry(input_card, width=25)
        self.amount_entry.grid(row=3, column=1, padx=8, pady=6)

        # Category Actions
        category_card = tk.Frame(container, bg="#1c1c1c", bd=0)
        category_card.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        for i in range(3):
            category_card.grid_columnconfigure(i, weight=1)

        ttk.Button(category_card, text="➕ Add Category", command=self.add_category) \
            .grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(category_card, text="✏️ Edit Category", command=self.edit_category) \
            .grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(category_card, text="🗑️ Delete Category", command=self.delete_category) \
            .grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Trip Actions
        trip_card = tk.Frame(container, bg="#1c1c1c", bd=0)
        trip_card.grid(row=4, column=0, sticky="ew", padx=20, pady=10)

        for i in range(2):
            trip_card.grid_columnconfigure(i, weight=1)

        ttk.Button(trip_card, text="💾 Save Budget", command=self.save_budget) \
            .grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(trip_card, text="🗑️ Delete Trip", command=self.delete_trip) \
            .grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Display
        display_card = tk.Frame(container, bg="#1c1c1c", bd=0)
        display_card.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.display = tk.Text(display_card, bg="#1f1f1f", fg="white", insertbackground="white",
                               relief="flat", wrap="word")
        self.display.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer Buttons
        footer = tk.Frame(container, bg="#121212")
        footer.grid(row=2, column=0, pady=10)

        ttk.Button(footer, text="🔄 Refresh View", command=self.view_budgets).grid(row=0, column=0, padx=10)
        ttk.Button(footer, text="⬅️ Go Back", command=self.go_back).grid(row=0, column=1, padx=10)

        self.view_budgets()

    def add_category(self):
        category = self.cat_entry.get().strip()
        try:
            amount = float(self.amount_entry.get())
            self.controller.add_category(self.trip_name, category, amount)
            self.view_budgets()
            messagebox.showinfo("Added", f"Category '{category}' added with RM{amount:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def edit_category(self):
        budget = self.controller.get_trip(self.trip_name)
        categories = list(budget.categories.keys())

        if not categories:
            messagebox.showinfo("No Categories", "There are no categories to edit.")
            return

        # Create pop-up dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("✏️ Edit Category")
        dialog.geometry("300x300")
        dialog.configure(bg="#2b2b2b")

        ttk.Label(dialog, text="Choose Category:", background="#2b2b2b", foreground="white").pack(pady=(15, 5))
        cat_var = tk.StringVar(value=categories[0])
        combo = ttk.Combobox(dialog, textvariable=cat_var, values=categories, state="readonly")
        combo.pack(pady=5)

        ttk.Label(dialog, text="New Amount (RM):", background="#2b2b2b", foreground="white").pack(pady=(15, 5))
        amount_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=amount_var)
        entry.pack(pady=5)

        def save():
            try:
                amt = float(amount_var.get())
                self.controller.edit_category(self.trip_name, cat_var.get(), amt)
                self.view_budgets()
                dialog.destroy()
                messagebox.showinfo("Updated", f"Category '{cat_var.get()}' updated to RM{amt:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        ttk.Button(dialog, text="💾 Save Changes", style="Modern.TButton", command=save).pack(pady=15, fill="x", padx=20)
        ttk.Button(dialog, text="❌ Cancel", style="Exit.TButton", command=dialog.destroy).pack(pady=(0, 15), fill="x", padx=20)

    def delete_trip(self):
        confirm = messagebox.askyesno("Confirm Delete", f"Delete trip '{self.trip_name}'?")
        if confirm:
            try:
                self.controller.delete_trip(self.trip_name)
                self.root.destroy()
                messagebox.showinfo("Deleted", f"Trip '{self.trip_name}' deleted!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def delete_category(self):
        budget = self.controller.get_trip(self.trip_name)
        categories = list(budget.categories.keys())

        if not categories:
            messagebox.showinfo("No Categories", "There are no categories to delete.")
            return

        # Create pop-up dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("🗑 Delete Category")
        dialog.geometry("300x300")
        dialog.configure(bg="#2b2b2b")

        ttk.Label(dialog, text="Choose Category to Delete:", background="#2b2b2b", foreground="white").pack(
            pady=(20, 5))
        cat_var = tk.StringVar(value=categories[0])
        combo = ttk.Combobox(dialog, textvariable=cat_var, values=categories, state="readonly")
        combo.pack(pady=5)

        def confirm_delete():
            category = cat_var.get()
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{category}'?"):
                self.controller.delete_category(self.trip_name, category)
                self.view_budgets()
                dialog.destroy()
                messagebox.showinfo("Deleted", f"Category '{category}' has been removed.")

        ttk.Button(dialog, text="🗑 Delete", style="Exit.TButton", command=confirm_delete).pack(pady=15, fill="x", padx=20)
        ttk.Button(dialog, text="❌ Cancel", style="Exit.TButton", command=dialog.destroy).pack(pady=(0, 15), fill="x", padx=20)

    def save_budget(self):
        try:
            total = float(self.total_entry.get())
            self.controller.update_total(self.trip_name, total)
            messagebox.showinfo("Saved", "Budget saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Total budget must be a number!")

    def view_budgets(self):
        self.display.delete("1.0", tk.END)
        budget = self.controller.get_trip(self.trip_name)

        self.display.insert(tk.END, f"🏖️ Trip: {budget.trip_name}\n")
        self.display.insert(tk.END, f"   💰 Total Budget: RM{budget.total_budget:.2f}\n")
        self.display.insert(tk.END, f"   📊 Allocated: RM{budget.allocated:.2f}\n")
        self.display.insert(tk.END, f"   💵 Remaining: RM{budget.remaining:.2f}\n")
        self.display.insert(tk.END, "   📂 Categories:\n")

        if budget.categories:
            for category, amount in budget.categories.items():
                self.display.insert(tk.END, f"      - {category}: RM{amount:.2f}\n")
        else:
            self.display.insert(tk.END, "      (No categories)\n")

    def go_back(self):
        self.root.destroy()

# === Budget Menu ===
class BudgetMenu:
    def __init__(self, root, controller: BudgetController):
        self.root = root
        self.controller = controller
        self.root.title("💼 Budget Plans")
        self.root.configure(bg="#121212")
        self.root.geometry("700x600")

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", background="#121212", foreground="white")

        # Title
        title = ttk.Label(root, text="💼 Manage Budget Plans", font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)

        # Listbox
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

        style = ttk.Style()
        style.configure("White.TButton", background="white", foreground="black")
        ttk.Button(btn_frame, text="➕ Add New Plan", command=self.add_plan, style="White.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="✏️ Open Plan", command=self.open_plan, style="White.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="🗑 Delete Plan", command=self.delete_plan, style="White.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="⬅️ Back to Menu", command=self.go_back, style="White.TButton").grid(row=0, column=3, padx=5)

        self.refresh_list()

    def go_back(self):
        self.root.destroy()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for trip_name in self.controller.get_trips():
            self.listbox.insert(tk.END, trip_name)

    def add_plan(self):
        trip_name = simpledialog.askstring("New Plan", "Enter trip name:", parent=self.root)
        if not trip_name:
            return
        try:
            self.controller.add_trip(trip_name)
            self.refresh_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def open_plan(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a plan to open.")
            return
        trip_name = self.listbox.get(selection[0])
        win = tk.Toplevel(self.root)
        BudgetGUI(win, trip_name, self.controller)

    def delete_plan(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a plan to delete.")
            return
        trip_name = self.listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Delete plan '{trip_name}'?")
        if confirm:
            try:
                self.controller.delete_trip(trip_name)
                self.refresh_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
