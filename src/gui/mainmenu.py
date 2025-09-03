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

        # Gradient Background
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.bind("<Configure>", self.redraw_gradient)

        # ttk Style
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#2b2b2b", relief="flat")
        style.configure("Header.TLabel",
                        font=("Segoe UI", 20, "bold"),
                        background="#2b2b2b",
                        foreground="white")
        style.configure("TLabel",
                        font=("Segoe UI", 12),
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

        # Main Card
        card = ttk.Frame(self.bg_canvas, style="Card.TFrame", padding=30)
        card.place(relx=0.5, rely=0.45, anchor="center")

        # Title + underline
        title = ttk.Label(card, text="✈ Travel Planner Assistant", style="Header.TLabel")
        title.pack(pady=(0, 10))
        tk.Frame(card, bg="#00bcd4", height=2, width=280).pack(pady=(0, 20))

        # Buttons
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

        # Footer
        footer = ttk.Label(self.bg_canvas, text="© 2025 Travel Planner Assistant",
                           background="#2b2b2b", foreground="#aaa", font=("Segoe UI", 9))
        footer.place(relx=0.5, rely=0.95, anchor="center")

    # Gradient Drawer
    def draw_gradient(self, width, height, color1="#0f2027", color2="#2c5364"):
        self.bg_canvas.delete("gradient")
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        for i in range(height):
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            self.bg_canvas.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}", tags=("gradient",))

    def redraw_gradient(self, event):
        self.draw_gradient(event.width, event.height)

    # Sub-Menus
    def open_itinerary_menu(self):
        self.root.destroy()
        new_root = tk.Tk()
        new_root.configure(bg="#121212")
        ItineraryMenu(new_root)
        new_root.mainloop()

    def open_budget_menu(self):
        self.root.destroy()
        new_root = tk.Tk()
        new_root.configure(bg="#121212")
        controller = BudgetController()
        BudgetMenu(new_root, controller)
        new_root.mainloop()

    def open_packing_menu(self):
        try:
            self.root.destroy()
            new_root = tk.Tk()
            new_root.configure(bg="#121212")
            PackingListGUI(new_root)
            new_root.mainloop()
        except ImportError as e:
            messagebox.showerror("Module Not Found", f"Packing list not found:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error when opening packing list:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
