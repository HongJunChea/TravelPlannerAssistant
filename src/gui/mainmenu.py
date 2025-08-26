import tkinter as tk
from tkinter import ttk
from src.gui.budgetgui import BudgetGUI


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

        # Buttons
        ttk.Button(root, text="Module 1", command=self.not_implemented).pack(pady=10)
        ttk.Button(root, text="Packing List Generator", command=self.not_implemented).pack(pady=10)
        ttk.Button(root, text="💰 Budget Estimator", command=self.open_budget_menu).pack(pady=10)
        ttk.Button(root, text="Exit", command=root.quit).pack(pady=20)

    def open_budget_menu(self):
        win = tk.Toplevel(self.root)
        BudgetGUI(win)

    def not_implemented(self):
        tk.messagebox.showinfo("Info", "This module is not implemented yet.")


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MainApp(root)
#     root.mainloop()