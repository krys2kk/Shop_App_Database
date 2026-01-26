import tkinter as tk
from tkinter import ttk
import database_init
from views import CustomersView, ProductsView, OrdersView, ReportsView

class ShopManagementApp(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.root.title("System Zarządzania Sklepem")
        self.root.geometry("900x600")

        database_init.init_db()

        self.setupUI()

    def setupUI(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        title = ttk.Label(header_frame, text="System Zarządzania Sklepem", font=("Helvetica", 18, 'bold'))
        title.pack()

        subtitle = ttk.Label(header_frame, text="Baza Danych - Projekt 2025/26", font=("Helvetica", 12))
        subtitle.pack()

        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.customers_view = CustomersView(self.notebook)
        self.notebook.add(self.customers_view, text="Klienci")
        
        self.products_view = ProductsView(self.notebook)
        self.notebook.add(self.products_view, text="Produkty")
        
        self.orders_view = OrdersView(self.notebook)
        self.notebook.add(self.orders_view, text="Zamówienia")
        
        self.reports_view = ReportsView(self.notebook)
        self.notebook.add(self.reports_view, text="Raporty")

        footer = ttk.Label(self.root, text="v1.0 | Etap 4: Frontend", font=("Helvetica", 10), foreground="gray")
        footer.pack(side='bottom', pady=5)

def main():
    root = tk.Tk()
    app = ShopManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
