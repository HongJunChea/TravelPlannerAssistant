import tkinter as tk
from tkinter import ttk
from src.gui.budgetgui import BudgetGUI


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner Assistant")
        self.root.geometry("500x350")
        self.root.configure(bg="#121212")  # dark background

        # ttk styling (dark mode)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 12),
                        padding=8,
                        relief="flat",
                        background="#1f1f1f",   # button background
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#333333")],
                  foreground=[("active", "white")])

        style.configure("TLabel", font=("Segoe UI", 12), background="#121212", foreground="white")

        # Title
        title = ttk.Label(root, text="✈ Travel Planner Assistant", font=("Segoe UI", 18, "bold"))
        title.pack(pady=20)

        # Buttons (Modules)
        ttk.Button(root, text="Budget Estimator", command=self.open_budget).pack(pady=10)
        ttk.Button(root, text="Trip Planner", state="disabled").pack(pady=10)
        ttk.Button(root, text="Destination Guide", state="disabled").pack(pady=10)
        ttk.Button(root, text="Exit", command=root.quit).pack(pady=20)

    def open_budget(self):
        budget_window = tk.Toplevel(self.root)
        budget_window.configure(bg="#121212")  # dark background for a new window
        BudgetGUI(budget_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()