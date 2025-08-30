import tkinter as tk
from tkinter import messagebox
from src.gui.budgetgui import BudgetMenu
from src.gui.packageGui import PackingListGUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✈ Travel Planner Assistant")
        self.root.geometry("600x450")
        self.root.minsize(500, 400)

        # Gradient canvas background
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient("#0f2027", "#203a43", "#2c5364")

        # Title
        title = tk.Label(
            self.canvas,
            text="✈ Travel Planner Assistant",
            font=("Segoe UI", 22, "bold"),
            bg="#0f2027", fg="white"
        )
        title.place(relx=0.5, rely=0.12, anchor="center")

        # Accent line under title
        self.canvas.create_line(150, 90, 450, 90, fill="#4ecdc4", width=2)

        # Menu card
        card = tk.Frame(self.canvas, bg="#1e1e1e")
        card.place(relx=0.5, rely=0.55, anchor="center", width=400, height=280)
        card.configure(highlightbackground="#333333", highlightthickness=2, bd=0)

        # Buttons inside card
        self.create_button(card, "🗂  Module 1", self.not_implemented)
        self.create_button(card, "💼  Packing List Generator", self.open_packing_menu)
        self.create_button(card, "💰  Budget Estimator", self.open_budget_menu)
        self.create_button(card, "🚪  Exit", root.quit)

        # Footer
        footer = tk.Label(
            self.canvas,
            text="© 2025 Travel Planner Assistant",
            font=("Segoe UI", 9),
            bg="#0f2027", fg="gray"
        )
        footer.place(relx=0.5, rely=0.95, anchor="center")

    # Draw vertical gradient
    def draw_gradient(self, *colors):
        width, height = 600, 450
        steps = height // (len(colors) - 1)
        for i in range(len(colors)-1):
            (r1, g1, b1) = self.root.winfo_rgb(colors[i])
            (r2, g2, b2) = self.root.winfo_rgb(colors[i+1])
            r_ratio = (r2 - r1) / steps
            g_ratio = (g2 - g1) / steps
            b_ratio = (b2 - b1) / steps
            for j in range(steps):
                nr = int(r1 + (r_ratio * j)) >> 8
                ng = int(g1 + (g_ratio * j)) >> 8
                nb = int(b1 + (b_ratio * j)) >> 8
                color = f"#{nr:02x}{ng:02x}{nb:02x}"
                y = i*steps + j
                self.canvas.create_line(0, y, width, y, fill=color)

    # Card-style button with hover effect
    def create_button(self, parent, text, command):
        btn = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 12, "bold"),
            bg="#2b2b2b", fg="white",
            padx=12, pady=12,
            cursor="hand2"
        )
        btn.pack(pady=10, fill="x", padx=40)

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#3a3a3a"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#2b2b2b"))
        btn.bind("<Button-1>", lambda e: command())

    # Menu actions
    def open_budget_menu(self):
        win = tk.Toplevel(self.root)
        BudgetMenu(win)

    def open_packing_menu(self):
        try:
            win = tk.Toplevel(self.root)
            PackingListGUI(win)
        except ImportError as e:
            messagebox.showerror("Module Not Found", f"Packing list not found:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error when open packing list:\n{str(e)}")

    def not_implemented(self):
        messagebox.showinfo("Info", "This module is not implemented yet.")

