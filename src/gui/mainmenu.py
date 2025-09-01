import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.ItineraryGUI import ItineraryMenu
from src.gui.budgetgui import BudgetMenu
from src.gui.packageGui import PackingListGUI
from src.controllers.budgetcontroller import BudgetController

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✈ Travel Planner Assistant")
        self.root.geometry("750x500")
        self.root.configure(bg="#121212")

        # === Gradient Background (auto-resizes) ===
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.bg_canvas.pack(fill="both", expand=True)
        # store colors and redraw on resize
        self.grad_top = "#0f2027"
        self.grad_bottom = "#2c5364"
        self.bg_canvas.bind("<Configure>", lambda e: self.draw_gradient())
        self.draw_gradient()  # initial paint

        # === ttk Style ===
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#2b2b2b")
        style.configure("Card.TFrame", background="#2b2b2b", relief="flat")

        style.configure("TLabel",
                        font=("Segoe UI", 12),
                        background="#2b2b2b",
                        foreground="white")
        style.configure("Header.TLabel",
                        font=("Segoe UI", 20, "bold"),
                        background="#2b2b2b",
                        foreground="white")

        style.configure("Modern.TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=12,
                        relief="flat",
                        background="#3b3b3b",
                        foreground="white")
        style.map("Modern.TButton",
                  background=[("active", "#505050")],
                  foreground=[("active", "white")])

        style.configure("Exit.TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=12,
                        relief="flat",
                        background="#a93232",
                        foreground="white")
        style.map("Exit.TButton",
                  background=[("active", "#e74c3c")],
                  foreground=[("active", "white")])

        # === Main Card ===
        card = ttk.Frame(self.bg_canvas, style="Card.TFrame", padding=30)
        # keep centered even when the window resizes
        card.place(relx=0.5, rely=0.45, anchor="center")

        title = ttk.Label(card, text="✈ Travel Planner Assistant", style="Header.TLabel")
        title.pack(pady=(0, 10))
        tk.Frame(card, bg="#00bcd4", height=2, width=280).pack(pady=(0, 20))

        btn_width = 30
        ttk.Button(card, text="🗓 Itinerary Builder", style="Modern.TButton",
                   command=self.open_itinerary_menu, width=btn_width) \
            .pack(pady=6, fill="x", padx=10)

        ttk.Button(card, text="📦 Packing List Generator", style="Modern.TButton",
                   command=self.open_packing_menu, width=btn_width) \
            .pack(pady=6, fill="x", padx=10)

        ttk.Button(card, text="💰 Budget Estimator", style="Modern.TButton",
                   command=self.open_budget_menu, width=btn_width) \
            .pack(pady=6, fill="x", padx=10)

        ttk.Button(card, text="❌ Exit", style="Exit.TButton",
                   command=root.quit, width=btn_width) \
            .pack(pady=(15, 5), fill="x", padx=10)

        footer = ttk.Label(self.bg_canvas, text="© 2025 Travel Planner Assistant",
                           background="#2b2b2b", foreground="#aaa", font=("Segoe UI", 9))
        footer.place(relx=0.5, rely=0.95, anchor="center")

    def draw_gradient(self):
        """Draw a vertical gradient that always fills the canvas."""
        c = self.bg_canvas
        c.delete("gradient")  # clear previous
        width = max(1, c.winfo_width())
        height = max(1, c.winfo_height())

        # hex -> rgb
        r1, g1, b1 = int(self.grad_top[1:3], 16), int(self.grad_top[3:5], 16), int(self.grad_top[5:7], 16)
        r2, g2, b2 = int(self.grad_bottom[1:3], 16), int(self.grad_bottom[3:5], 16), int(self.grad_bottom[5:7], 16)

        for i in range(height):
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            c.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}", tags="gradient")

    # === Sub-Menus ===
    def open_itinerary_menu(self):
        win = tk.Toplevel(self.root)
        win.configure(bg="#121212")
        ItineraryMenu(win)

    def open_budget_menu(self):
        win = tk.Toplevel(self.root)
        controller = BudgetController()
        win.configure(bg="#121212")
        BudgetMenu(win, controller)

    def open_packing_menu(self):
        try:
            win = tk.Toplevel(self.root)
            win.configure(bg="#121212")
            PackingListGUI(win)
        except ImportError as e:
            messagebox.showerror("Module Not Found", f"Packing list not found:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error when opening packing list:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
