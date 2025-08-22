import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.utils.file import load_budgets, save_budgets
from src.gui.budgetgui import BudgetGUI


class BudgetMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("💼 Budget Plans")
        self.root.geometry("500x400")
        self.root.configure(bg="#121212")

        self.budgets = load_budgets()

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 11),
                        padding=6,
                        background="#1f1f1f",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#333333")],
                  foreground=[("active", "white")])
        style.configure("TLabel", background="#121212", foreground="white")

        # Title
        title = ttk.Label(root, text="💼 Manage Budget Plans", font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)

        # Listbox for budget plans
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

        # Load listbox
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
        self.budgets[trip_name] = {"total_budget": 0, "categories": {}}
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
