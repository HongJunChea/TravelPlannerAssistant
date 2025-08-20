import tkinter as tk
from tkinter import ttk, messagebox
from src.modules.budget import Budget
from src.utils.file import load_budgets, save_budgets


class BudgetGUI:
    def __init__(self, root, trip_name, budgets):
        self.root = root
        self.trip_name = trip_name
        self.budgets = budgets

        self.root.title(f"Budget Plan - {self.trip_name}")
        self.root.geometry("650x550")
        self.root.configure(bg="#121212")  # dark mode base

        # ttk dark styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 11),
                        padding=6,
                        relief="flat",
                        background="#1f1f1f",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#333333")],
                  foreground=[("active", "white")])

        style.configure("TLabel", font=("Segoe UI", 11),
                        background="#121212",
                        foreground="white")
        style.configure("TEntry",
                        fieldbackground="#1f1f1f",
                        foreground="white",
                        insertcolor="white")  # white cursor in entry

        # Data
        self.budgets = load_budgets()

        # Title
        title = ttk.Label(root, text="✈ Travel Budget Estimator",
                          font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)

        # Trip + Category input frame
        frame = tk.Frame(root, bg="#121212")
        frame.pack(pady=10)

        ttk.Label(frame, text="Trip Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.trip_entry = ttk.Entry(frame, width=25)
        self.trip_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Total Budget:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.total_entry = ttk.Entry(frame, width=25)
        self.total_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Category:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.cat_entry = ttk.Entry(frame, width=25)
        self.cat_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame, width=25)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons row
        ttk.Button(frame, text="➕ New Budget", command=self.add_budget).grid(row=4, column=0, pady=10)
        ttk.Button(frame, text="✏️ Edit Category", command=self.edit_budget).grid(row=4, column=1, pady=10)
        ttk.Button(frame, text="🗑️ Delete Trip", command=self.delete_budget).grid(row=5, column=0, pady=10)
        ttk.Button(frame, text="🗑️ Delete Category", command=self.delete_category).grid(row=5, column=1, pady=10)
        ttk.Button(frame, text="💾 Save Budgets", command=self.save_budget).grid(row=6, column=0, columnspan=2, pady=10)

        # Display area
        self.display = tk.Text(root, height=15, width=70,
                               bg="#1f1f1f", fg="white", insertbackground="white",
                               relief="flat", wrap="word")
        self.display.pack(pady=10)

        ttk.Button(root, text="🔄 Refresh View", command=self.view_budgets).pack(pady=5)

        self.view_budgets()

    # --- Controller Methods ---

    def add_budget(self):
        trip_name = self.trip_entry.get().strip()
        try:
            total_budget = float(self.total_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Total budget must be a number!")
            return

        category = self.cat_entry.get().strip()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        # Create or load budget
        if trip_name not in self.budgets:
            budget = Budget(trip_name, total_budget)
        else:
            data = self.budgets[trip_name]
            budget = Budget(trip_name, data["total_budget"])
            budget.categories = data["categories"]

        budget.add_category(category, amount)
        self.budgets[trip_name] = {
            "total_budget": budget.total_budget,
            "categories": budget.categories
        }

        self.view_budgets()
        self.cat_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def edit_budget(self):
        trip_name = self.trip_entry.get().strip()
        category = self.cat_entry.get().strip()
        try:
            new_amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "New amount must be a number!")
            return

        if trip_name not in self.budgets:
            messagebox.showerror("Error", "Trip not found!")
            return

        data = self.budgets[trip_name]
        if category not in data["categories"]:
            messagebox.showerror("Error", f"Category '{category}' not found!")
            return

        data["categories"][category] = new_amount
        self.budgets[trip_name] = data
        self.view_budgets()
        messagebox.showinfo("Updated", f"Category '{category}' updated!")

    def delete_budget(self):
        trip_name = self.trip_entry.get().strip()
        if not trip_name or trip_name not in self.budgets:
            messagebox.showerror("Error", "Enter a valid trip name to delete!")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete trip '{trip_name}'?")
        if not confirm:
            return

        del self.budgets[trip_name]
        self.view_budgets()
        self.trip_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)
        messagebox.showinfo("Deleted", f"Trip '{trip_name}' deleted!")

    def delete_category(self):
        trip_name = self.trip_entry.get().strip()
        category = self.cat_entry.get().strip()

        if not trip_name or trip_name not in self.budgets:
            messagebox.showerror("Error", "Enter a valid trip name first!")
            return

        if not category:
            messagebox.showerror("Error", "Enter a category name to delete!")
            return

        budget_data = self.budgets[trip_name]
        if category not in budget_data["categories"]:
            messagebox.showerror("Error", f"Category '{category}' not found in {trip_name}.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{category}' from trip '{trip_name}'?")
        if not confirm:
            return

        del budget_data["categories"][category]
        self.budgets[trip_name] = budget_data

        self.view_budgets()
        self.cat_entry.delete(0, tk.END)
        messagebox.showinfo("Deleted", f"Category '{category}' removed from trip '{trip_name}'.")

    def save_budget(self):
        save_budgets(self.budgets)
        messagebox.showinfo("Saved", "Budgets saved successfully!")

    def view_budgets(self):
        self.display.delete("1.0", tk.END)
        if not self.budgets:
            self.display.insert(tk.END, "No budget plans available.\n")
            return
        for trip, data in self.budgets.items():
            self.display.insert(tk.END, f"\n🌍 Trip: {trip}\n")
            self.display.insert(tk.END, f"   💰 Total Budget: RM{data['total_budget']:.2f}\n")
            self.display.insert(tk.END, "   📂 Categories:\n")
            for cat, amt in data['categories'].items():
                self.display.insert(tk.END, f"      - {cat}: RM{amt:.2f}\n")
            # show remaining balance
            allocated = sum(data['categories'].values())
            remaining = data['total_budget'] - allocated
            self.display.insert(tk.END, f"   📊 Allocated: RM{allocated:.2f}\n")
            self.display.insert(tk.END, f"   🔑 Remaining: RM{remaining:.2f}\n")
