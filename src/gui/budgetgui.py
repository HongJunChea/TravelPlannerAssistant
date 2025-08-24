import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.modules.budget import Budget
from src.utils.file import load_budgets, save_budgets

class BudgetGUI:
    def __init__(self, root, trip_name, budgets):
        self.root = root
        self.trip_name = trip_name
        self.budgets = budgets  # dict[str, Budget]

        self.root.title(f"Budget Plan - {self.trip_name}")
        enable_fullscreen(self.root)
        self.root.configure(bg="#121212")

        # ttk dark styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        relief="flat", background="#1f1f1f", foreground="white")
        style.map("TButton", background=[("active", "#333333")], foreground=[("active", "white")])
        style.configure("TLabel", font=("Segoe UI", 11), background="#121212", foreground="white")
        style.configure("TEntry", fieldbackground="#1f1f1f", foreground="white", insertcolor="white")

        # Inputs frame
        frame = tk.Frame(root, bg="#121212")
        frame.pack(pady=10)

        ttk.Label(frame, text="Trip Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.trip_entry = ttk.Entry(frame, width=25)
        self.trip_entry.insert(0, trip_name)
        self.trip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Total Budget:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.total_entry = ttk.Entry(frame, width=25)
        self.total_entry.insert(0, str(self.budgets[trip_name].total_budget))
        self.total_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Category:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.cat_entry = ttk.Entry(frame, width=25)
        self.cat_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame, width=25)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(frame, text="➕ Add Category", command=self.add_category).grid(row=4, column=0, pady=10)
        ttk.Button(frame, text="✏️ Edit Category", command=self.edit_category).grid(row=4, column=1, pady=10)
        ttk.Button(frame, text="🗑️ Delete Trip", command=self.delete_trip).grid(row=5, column=0, pady=10)
        ttk.Button(frame, text="🗑️ Delete Category", command=self.delete_category).grid(row=5, column=1, pady=10)
        ttk.Button(frame, text="💾 Save Budget", command=self.save_budget).grid(row=6, column=0, columnspan=2, pady=10)

        # Display
        self.display = tk.Text(root, height=15, width=70,
                               bg="#1f1f1f", fg="white", insertbackground="white",
                               relief="flat", wrap="word")
        self.display.pack(pady=10)

        ttk.Button(root, text="🔄 Refresh View", command=self.view_budgets).pack(pady=5)

        ttk.Button(root, text="⬅️ Go Back", command=self.go_back).pack(pady=10)

        self.view_budgets()

    # methods
    def add_category(self):
        category = self.cat_entry.get().strip()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        budget = self.budgets[self.trip_name]
        budget.categories[category] = amount
        self.view_budgets()
        messagebox.showinfo("Added", f"Category '{category}' added with RM{amount:.2f}")

    def edit_category(self):
        category = self.cat_entry.get().strip()
        try:
            new_amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "New amount must be a number!")
            return

        budget = self.budgets[self.trip_name]
        if category not in budget.categories:
            messagebox.showerror("Error", f"Category '{category}' not found!")
            return

        budget.categories[category] = new_amount
        self.view_budgets()
        messagebox.showinfo("Updated", f"Category '{category}' updated!")

    def delete_trip(self):
        confirm = messagebox.askyesno("Confirm Delete", f"Delete trip '{self.trip_name}'?")
        if confirm:
            del self.budgets[self.trip_name]
            save_budgets(self.budgets)
            self.root.destroy()
            messagebox.showinfo("Deleted", f"Trip '{self.trip_name}' deleted!")

    def delete_category(self):
        category = self.cat_entry.get().strip()
        budget = self.budgets[self.trip_name]
        if category not in budget.categories:
            messagebox.showerror("Error", f"Category '{category}' not found!")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{category}' from trip '{self.trip_name}'?")
        if confirm:
            del budget.categories[category]
            self.view_budgets()
            messagebox.showinfo("Deleted", f"Category '{category}' removed.")

    def save_budget(self):
        try:
            total = float(self.total_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Total budget must be a number!")
            return

        self.budgets[self.trip_name].total_budget = total
        save_budgets(self.budgets)
        messagebox.showinfo("Saved", "Budget saved successfully!")

    def view_budgets(self):
        self.display.delete("1.0", tk.END)
        budget = self.budgets[self.trip_name]

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

# budget menu
class BudgetMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("💼 Budget Plans")
        enable_fullscreen(self.root)
        self.root.configure(bg="#121212")

        self.budgets = load_budgets()  # dict[str, Budget]

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

        ttk.Button(btn_frame, text="➕ Add New Plan", command=self.add_plan).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="✏️ Open Plan", command=self.open_plan).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="🗑 Delete Plan", command=self.delete_plan).grid(row=0, column=2, padx=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for trip_name in self.budgets.keys():
            self.listbox.insert(tk.END, trip_name)

    def add_plan(self):
        trip_name = simpledialog.askstring("New Plan", "Enter trip name:", parent=self.root)
        if not trip_name:
            return
        if trip_name in self.budgets:
            messagebox.showerror("Error", f"A plan named '{trip_name}' already exists.")
            return

        self.budgets[trip_name] = Budget(trip_name=trip_name, total_budget=0, categories={})
        save_budgets(self.budgets)
        self.refresh_list()

    def open_plan(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a plan to open.")
            return
        trip_name = self.listbox.get(selection[0])
        win = tk.Toplevel(self.root)
        BudgetGUI(win, trip_name, self.budgets)

    def delete_plan(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a plan to delete.")
            return
        trip_name = self.listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Delete plan '{trip_name}'?")
        if confirm:
            del self.budgets[trip_name]
            save_budgets(self.budgets)
            self.refresh_list()
