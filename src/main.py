import tkinter as tk
from tkinter import ttk
from gui.budgetgui import BudgetMenu

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("✈ Travel Planner Assistant")
        self.root.geometry("400x400")
        self.root.configure(bg="#121212")

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=10,
                        width=25,
                        background="#1f1f1f",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#333333")],
                  foreground=[("active", "white")])

        style.configure("TLabel",
                        font=("Segoe UI", 16, "bold"),
                        background="#121212",
                        foreground="white")

        # Title
        title = ttk.Label(root, text="✈ Travel Planner Assistant")
        title.pack(pady=20)

        # Buttons (all equal width)
        self.btn_trip = ttk.Button(root, text="Module 1")
        self.btn_trip.pack(pady=10)

        self.btn_dest = ttk.Button(root, text="Module 2")
        self.btn_dest.pack(pady=10)

        self.btn_budget = ttk.Button(root, text="💰 Budget Estimator", command=self.open_budget_menu)
        self.btn_budget.pack(pady=10)

        self.btn_exit = ttk.Button(root, text="Exit", command=root.quit)
        self.btn_exit.pack(pady=20)

    def open_budget_menu(self):
        win = tk.Toplevel(self.root)
        BudgetMenu(win)


if __name__ == "__main__":
    root = tk.Tk()
    enable_fullscreen(root)
    app = MainMenu(root)
    root.mainloop()
