import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.ItineraryGUI import ItineraryMenu
from src.gui.budgetgui import BudgetMenu
from src.gui.packageGui import PackingListGUI, PackingListViewer

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✈ Travel Planner Assistant")
        self.root.geometry("400x400")
        self.root.configure(bg="#121212")

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6,
                        relief="flat", background="#1f1f1f", foreground="white")

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
        ttk.Button(root, text="Itinerary Builder", command=self.open_itinerary_menu).pack(pady=10, fill="x", padx=40)
        ttk.Button(root, text="Packing List Generator", command=self.open_packing_menu).pack(pady=10, fill="x", padx=40)
        ttk.Button(root, text="💰 Budget Estimator", command=self.open_budget_menu).pack(pady=10, fill="x", padx=40)
        ttk.Button(root, text="Exit", command=root.quit).pack(pady=20, fill="x", padx=40)

    def open_itinerary_menu(self):
        win = tk.Toplevel(self.root)
        ItineraryMenu(win)

    def open_budget_menu(self):
        win = tk.Toplevel(self.root)
        BudgetMenu(win)

    def open_packing_menu(self):
        try:
            win = tk.Toplevel(self.root)
            PackingListGUI(win)
        except ImportError as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Module Not Found", f"Packing list not found:\n{str(e)}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Error when open packing list:\n{str(e)}")

    def not_implemented(self):
        messagebox.showinfo("Info", "This module is not implemented yet.")