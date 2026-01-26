import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from api_client import APIClient
from datetime import datetime

class CustomersView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.API = APIClient()
        self.setupUI()
        self.refresh_list()
    
    def setupUI(self):
        header = ttk.Label(self, text = "Zarządzanie Klientami", font = ('Arial', 16, 'bold'))
        header.pack(pady=10)

        list_frame = ttk.LabelFrame(self, text = "Lista Kilentów", padding = 10)
        list_frame.pack(fill = 'both', expand = True, padx = 10, pady = 5)

        columns = ('ID', 'Imię i Nazwisko', 'Email', 'Telefon')
        self.tree = ttk.Treeview(list_frame, columns = columns, show = 'headings', height = 10)

        for col in columns:
            self.tree.heading(col, text = col)
            self.tree.column(col, width = 150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient = 'vertical', command = self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady = 10)

        ttk.Button(btn_frame, text = "Odśwież", command = self.refresh_list).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Dodaj Klienta", command = self.add_customer_dialog).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Anonimizuj Klienta", command = self.delete_customer).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Usuń Całkowicie", command = self.delete_customer_completely).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Edytuj Dane", command = self.update_customer_dialog).pack(side = 'left', padx = 5)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        customers = self.API.get_customers()
        for c in customers:
            self.tree.insert('', 'end', values = (c['id'], c['name'], c['email'], c.get('phone', 'N/A')))
        
    def add_customer_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Dodaj klienta")
        dialog.geometry("400x250")

        ttk.Label(dialog, text = "Imię:").grid(row = 0, column = 0, padx = 10, pady = 5, sticky='w')
        name_entry = ttk.Entry(dialog, width = 30)
        name_entry.grid(row = 0, column = 1, padx = 10, pady = 5)


        ttk.Label(dialog, text = "Email:").grid(row = 1, column = 0, padx = 10, pady = 5, sticky='w')
        email_entry = ttk.Entry(dialog, width = 30)
        email_entry.grid(row = 1, column = 1, padx = 10, pady = 5)


        ttk.Label(dialog, text = "Telefon:").grid(row = 2, column = 0, padx = 10, pady = 5, sticky='w')
        phone_entry = ttk.Entry(dialog, width = 30)
        phone_entry.grid(row = 2, column = 1, padx = 10, pady = 5)


        ttk.Label(dialog, text = "Adres:").grid(row = 3, column = 0, padx = 10, pady = 5, sticky='w')
        address_entry = ttk.Entry(dialog, width = 30)
        address_entry.grid(row = 3, column = 1, padx = 10, pady = 5)

        def save():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            
            try:
                self.API.add_customer(name, email, phone, address)
                messagebox.showinfo("Sukces", "Klient został dodany")
                dialog.destroy()
                self.refresh_list()
            except ValueError as ve:
                messagebox.showerror("Błąd walidacji", str(ve))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać klienta: {str(e)}")
            
        ttk.Button(dialog, text = "Zapisz", command = save).grid(row = 4, column = 0, columnspan = 2, pady = 20)
    
    def delete_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz klienta do usunięcia:")
            return

        item = self.tree.item(selected[0])
        c_id = item['values'][0]

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz anonimizować klienta?"):
            try:
                self.API.anonymize_customer(c_id)
                messagebox.showinfo("Sukces", "Klient został zanonimizowany")
                self.refresh_list()
            except ValueError as ve:
                messagebox.showerror("Błąd", str(ve))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się anonimizować klienta: {str(e)}")

    def delete_customer_completely(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz klienta do usunięcia")
            return

        item = self.tree.item(selected[0])
        c_id = item['values'][0]

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz całkowicie usunąć klienta? (Tylko jeśli nie ma zamówień)"):
            try:
                self.API.delete_customer(c_id)
                messagebox.showinfo("Sukces", "Klient został usunięty")
                self.refresh_list()
            except ValueError as ve:
                messagebox.showerror("Błąd", str(ve))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się usunąć klienta: {str(e)}")

    def update_customer_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz klienta do edycji")
            return
        item = self.tree.item(selected[0])
        c_id = item['values'][0]
        dialog = tk.Toplevel(self)
        dialog.title("Edytuj dane klienta")
        dialog.geometry("400x250")
        ttk.Label(dialog, text = "Imię:").grid(row = 0, column = 0, padx = 10, pady = 5, sticky='w')
        name_entry = ttk.Entry(dialog, width = 30)
        name_entry.grid(row = 0, column = 1, padx = 10, pady = 5)
        name_entry.insert(0, item['values'][1])
        ttk.Label(dialog, text = "Email:").grid(row = 1, column = 0, padx = 10, pady = 5, sticky='w')
        email_entry = ttk.Entry(dialog, width = 30)
        email_entry.grid(row = 1, column = 1, padx = 10, pady = 5)
        email_entry.insert(0, item['values'][2])
        ttk.Label(dialog, text = "Telefon:").grid(row = 2, column = 0, padx = 10, pady = 5, sticky='w')
        phone_entry = ttk.Entry(dialog, width = 30)
        phone_entry.grid(row = 2, column = 1, padx = 10, pady = 5)
        phone_entry.insert(0, item['values'][3])
        ttk.Label(dialog, text = "Adres:").grid(row = 3, column = 0, padx = 10, pady = 5, sticky='w')
        address_entry = ttk.Entry(dialog, width = 30)
        address_entry.grid(row = 3, column = 1, padx = 10, pady = 5)

        def save():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            try:
                self.API.update_customer_info(c_id, name, email, phone, address)
                messagebox.showinfo("Sukces", "Dane klienta zostały zaktualizowane")
                dialog.destroy()
                self.refresh_list()
            except ValueError as ve:
                messagebox.showerror("Błąd walidacji", str(ve))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zaktualizować danych klienta: {str(e)}")
        ttk.Button(dialog, text = "Zapisz", command = save).grid(row = 4, column = 0, columnspan = 2, pady = 20)

class ProductsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.API = APIClient()
        self.edit_entry = None
        self.setupUI()
        self.refresh_list()

    def setupUI(self):
        header = ttk.Label(self, text = "Zarządzanie Produktami", font = ('Arial', 16, 'bold'))
        header.pack(pady = 10)

        list_frame = ttk.LabelFrame(self, text = "Lista Produktów", padding = 10)
        list_frame.pack(fill = 'both', expand = True, padx = 10, pady = 5)

        columns = ('ID', 'Nazwa', 'Opis', 'Cena', 'Stan')
        self.tree = ttk.Treeview(list_frame, columns = columns, show = 'headings', height = 10)

        widths = [50, 150, 200, 80, 80]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text = col)
            self.tree.column(col, width = width)
        
        scrollbar = ttk.Scrollbar(list_frame, orient = 'vertical', command = self.tree.yview)
        self.tree.configure(yscrollcommand = scrollbar.set)

        self.tree.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')
        
        self.tree.bind('<Double-1>', self.on_double_click)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady = 10)

        ttk.Button(btn_frame, text = "Odśwież", command = self.refresh_list).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Dodaj Produkt", command = self.add_product_dialog).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Ustaw Cenę", command = self.set_price_dialog).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Ruch Magazynowy", command = self.add_movement_dialog).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Pokaż Ruchy Magazynowe", command = self.list_inventory_movements).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Historia Cen", command = self.get_price_history_dialog).pack(side = 'left', padx = 5)

    def on_double_click(self, event):
        # Zamknij poprzedni edytor jeśli istnieje
        if self.edit_entry:
            self.edit_entry.destroy()
            self.edit_entry = None

        # Znajdź klikniętą komórkę
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            return

        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        
        if not item:
            return

        col_index = int(column[1:]) - 1  # #1 -> 0, #2 -> 1, etc.
        columns = ('ID', 'Nazwa', 'Opis', 'Cena', 'Stan')
        col_name = columns[col_index]

        # Tylko Nazwa i Opis są edytowalne (Cena przez "Ustaw Cenę", Stan przez "Ruch Magazynowy")
        if col_name not in ('Nazwa', 'Opis'):
            return

        # Pobierz pozycję i wymiary komórki
        bbox = self.tree.bbox(item, column)
        if not bbox:
            return

        x, y, width, height = bbox
        current_value = self.tree.item(item)['values'][col_index]

        # Stwórz pole edycji
        self.edit_entry = tk.Entry(self.tree, width=width//8)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, current_value if current_value != 'N/A' else '')
        self.edit_entry.select_range(0, tk.END)
        self.edit_entry.focus()

        # Zapisz informacje o edytowanej komórce
        self.edit_item = item
        self.edit_column = col_name
        self.edit_product_id = self.tree.item(item)['values'][0]

        # Obsługa zapisania (Enter) i anulowania (Escape)
        self.edit_entry.bind('<Return>', self.save_edit)
        self.edit_entry.bind('<Escape>', self.cancel_edit)
        self.edit_entry.bind('<FocusOut>', self.save_edit)

    def save_edit(self, event=None):
        if not self.edit_entry:
            return

        new_value = self.edit_entry.get().strip()
        
        if new_value:
            try:
                self.API.update_product(self.edit_product_id, self.edit_column.lower(), new_value)
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Błąd", f"Nie udało się zapisać: {str(e)}")

        self.edit_entry.destroy()
        self.edit_entry = None
        self.refresh_list()

    def cancel_edit(self, event=None):
        if self.edit_entry:
            self.edit_entry.destroy()
            self.edit_entry = None

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.API.get_products()
        for p in products:
            try:
                price = self.API.get_product_price(p['id'])
                price_display = f"{price:.2f}" if price is not None else 'N/A'
                stock = self.API.get_current_stock(p['id']) or 0
            except:
                price_display = 'N/A'
                stock = 0
            self.tree.insert('', 'end', values = (p['id'], p['name'], p.get('description', 'N/A'), price_display, stock))
        
    def add_product_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Dodaj produkt")
        dialog.geometry("400x200")

        ttk.Label(dialog, text = "Nazwa:").grid(row = 0, column = 0, padx = 10, pady = 5, sticky='w')
        name_entry = ttk.Entry(dialog, width = 30)
        name_entry.grid(row = 0, column = 1, padx = 10, pady = 5)

        ttk.Label(dialog, text = "Opis:").grid(row = 1, column = 0, padx = 10, pady = 5, sticky='w')
        desc_entry = ttk.Entry(dialog, width = 30)
        desc_entry.grid(row = 1, column = 1, padx = 10, pady = 5)

        def save():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()

            if not name or not description:
                messagebox.showerror("Błąd", "Nazwa i opis są wymagane")
                return
                
            try:
                self.API.add_product(name, description)
                messagebox.showinfo("Sukces", "Produkt został dodany")
                dialog.destroy()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać produktu: {str(e)}")
                
        ttk.Button(dialog, text = "Zapisz", command = save).grid(row = 2, column = 1, pady = 20)
        ttk.Button(dialog, text = "Anuluj", command = dialog.destroy).grid(row = 2, column = 0, padx = 20, pady = 20)
        
    def set_price_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz produkt do ustawienia ceny")
            return

        item = self.tree.item(selected[0])
        p_id = item['values'][0]
 
        dialog = tk.Toplevel(self)
        dialog.title("Ustaw cenę produktu")
        dialog.geometry("300x150")

        ttk.Label(dialog, text = "Nowa cena:").grid(row = 0, column = 0, padx = 10, pady = 5, sticky='w')
        price_entry = ttk.Entry(dialog, width = 20)
        price_entry.grid(row = 0, column = 1, padx = 10, pady = 5)

        def save():
            try:
                price = float(price_entry.get())
                self.API.update_product_price(p_id, price)
                messagebox.showinfo("Sukces", "Cena została ustawiona")
                dialog.destroy()
                self.refresh_list()
            except ValueError as ve:
                messagebox.showerror("Błąd", str(ve))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się ustawić ceny: {str(e)}")     
        ttk.Button(dialog, text = "Zapisz", command = save).grid(row = 1, column = 1, padx = 0, pady = 20, sticky = 'w')
        ttk.Button(dialog, text = "Anuluj", command = dialog.destroy).grid(row = 1, column = 0, padx = 0, pady = 20, sticky = 'w')

    def add_movement_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz produkt do dodania ruchu magazynowego:")
            return
        item = self.tree.item(selected[0])
        p_id = item['values'][0]

        dialog = tk.Toplevel(self)
        dialog.title("Dodaj ruch magazynowy")
        dialog.geometry("350x250")

        ttk.Label(dialog, text = f"ID produktu: {p_id}").pack(pady = 10)
        ttk.Label(dialog, text = "Typ ruchu:").pack()
        movement_type = ttk.Combobox(dialog, values = ['dostawa', 'wydanie', 'korekta'], state = 'readonly')
        movement_type.current(0)
        movement_type.pack(pady = 5)

        ttk.Label(dialog, text = "Ilość (ujemna dla rozchodu):").pack()
        quantity_entry = ttk.Entry(dialog)
        quantity_entry.pack(pady = 5)

        def save():
            try:
                quantity = int(quantity_entry.get())
                m_type = movement_type.get()
                self.API.add_inventory_movement(p_id, m_type, quantity)
                messagebox.showinfo("Sukces", "Ruch magazynowy został dodany")
                dialog.destroy()
                self.refresh_list()
            except ValueError as ve:
                messagebox.showerror("Błąd", str(ve))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać ruchu magazynowego: {str(e)}")

        ttk.Button(dialog, text = "Zapisz", command = save).pack(pady = 10)
        ttk.Button(dialog, text = "Anuluj", command = dialog.destroy).pack()

    def list_inventory_movements(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz produkt do wyświetlenia ruchów magazynowych")
            return

        item = self.tree.item(selected[0])
        p_id = item['values'][0]

        movements = self.API.list_inventory_movements(p_id)
        if not movements:
            messagebox.showinfo("Informacja", "Brak ruchów magazynowych dla tego produktu")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Ruchy magazynowe")
        dialog.geometry("500x300")

        tree_frame = ttk.Frame(dialog)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(10, 0))

        tree = ttk.Treeview(tree_frame, columns=('ID', 'Typ', 'Ilość', 'Data'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Typ', text='Typ')
        tree.heading('Ilość', text='Ilość')
        tree.heading('Data', text='Data')

        for m in movements:
            tree.insert('', 'end', values=(m['movement_id'], m['movement_type'], m['quantity_change'], m['movement_date']))

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        ttk.Button(dialog, text="Zamknij", command=dialog.destroy).pack(pady=10)
    
    def get_price_history_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz produkt do wyświetlenia historii cen")
            return

        item = self.tree.item(selected[0])
        p_id = item['values'][0]

        history = self.API.get_price_history(p_id)
        if not history:
            messagebox.showinfo("Informacja", "Brak historii cen dla tego produktu")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Historia cen")
        dialog.geometry("400x300")

        tree_frame = ttk.Frame(dialog)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(10, 0))

        tree = ttk.Treeview(tree_frame, columns=('Cena', 'Data rozpoczęcia'), show='headings')
        tree.heading('Cena', text='Cena')
        tree.heading('Data rozpoczęcia', text='Data rozpoczęcia')

        for h in history:
            tree.insert('', 'end', values=(f"{h['price']:.2f}", h['start_date']))

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        ttk.Button(dialog, text="Zamknij", command=dialog.destroy).pack(pady=10)

class OrdersView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.API = APIClient()
        self.setupUI()
        self.refresh_list()

    def setupUI(self):
        header = ttk.Label(self, text = "Zarządzanie Zamówieniami", font = ('Arial', 16, 'bold'))
        header.pack(pady = 10)

        list_frame = ttk.LabelFrame(self, text = "Lista Zamówień", padding = 10)
        list_frame.pack(fill = 'both', expand = True, padx = 10, pady = 5)

        columns = ('ID', 'Klient ID', 'Klient', 'Data', 'Status')
        self.tree = ttk.Treeview(list_frame, columns = columns, show = 'headings', height = 10)

        widths = [50, 80, 150, 150, 100]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text = col)
            self.tree.column(col, width = width)
        
        scrollbar = ttk.Scrollbar(list_frame, orient = 'vertical', command = self.tree.yview)
        self.tree.configure(yscrollcommand = scrollbar.set)

        self.tree.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady = 10)

        ttk.Button(btn_frame, text = "Odśwież", command = self.refresh_list).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Nowe Zamówienie", command = self.create_order_dialog).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Dodaj Produkt", command = self.add_order_item_dialog).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Szczegóły", command = self.show_order_details).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Usuń Zamówienie", command = self.delete_order).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Aktualizuj Status", command = self.update_order_status).pack(side = 'left', padx = 5)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        orders = self.API.get_orders()
        for o in orders:
            self.tree.insert('', 'end', values = (o['order_id'], o['customer_id'], o['customer_name'], o['order_date'], o['status']))

    def create_order_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Nowe zamówienie")
        dialog.geometry("500x450")
        
        # Lista produktów do dodania
        products_to_add = []

        # Klient i status
        ttk.Label(dialog, text = "ID Klienta:").grid(row = 0, column = 0, padx = 10, pady = 5, sticky='w')
        customer_entry = ttk.Entry(dialog, width = 20)
        customer_entry.grid(row = 0, column = 1, padx = 10, pady = 5, sticky='w')

        ttk.Label(dialog, text = "Status:").grid(row = 1, column = 0, padx = 10, pady = 5, sticky='w')
        status_combo = ttk.Combobox(dialog, values = ['nowe', 'w trakcie', 'wysłane', 'dostarczone', 'anulowane'], state = 'readonly', width = 17)
        status_combo.current(0)
        status_combo.grid(row = 1, column = 1, padx = 10, pady = 5, sticky='w')

        # Sekcja dodawania produktów
        ttk.Separator(dialog, orient='horizontal').grid(row = 2, column = 0, columnspan = 3, sticky = 'ew', pady = 10)
        ttk.Label(dialog, text = "Dodaj produkty:", font = ('Arial', 10, 'bold')).grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 5, sticky='w')

        ttk.Label(dialog, text = "ID Produktu:").grid(row = 4, column = 0, padx = 10, pady = 5, sticky='w')
        product_entry = ttk.Entry(dialog, width = 20)
        product_entry.grid(row = 4, column = 1, padx = 10, pady = 5, sticky='w')

        ttk.Label(dialog, text = "Ilość:").grid(row = 5, column = 0, padx = 10, pady = 5, sticky='w')
        quantity_entry = ttk.Entry(dialog, width = 20)
        quantity_entry.grid(row = 5, column = 1, padx = 10, pady = 5, sticky='w')

        # Lista dodanych produktów
        products_frame = ttk.LabelFrame(dialog, text = "Produkty w zamówieniu", padding = 5)
        products_frame.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = 'nsew')

        products_tree = ttk.Treeview(products_frame, columns = ('ID', 'Ilość', 'Cena'), show = 'headings', height = 6)
        products_tree.heading('ID', text = 'ID Produktu')
        products_tree.heading('Ilość', text = 'Ilość')
        products_tree.heading('Cena', text = 'Cena jedn.')
        products_tree.column('ID', width = 100)
        products_tree.column('Ilość', width = 100)
        products_tree.column('Cena', width = 100)
        products_tree.pack(fill = 'both', expand = True)

        def add_product_to_list():
            try:
                product_id = int(product_entry.get())
                quantity = int(quantity_entry.get())
                
                if quantity <= 0:
                    messagebox.showerror("Błąd", "Ilość musi być większa od zera")
                    return
                
                # Pobierz cenę produktu
                price = self.API.get_product_price(product_id)
                if price is None:
                    messagebox.showerror("Błąd", "Produkt nie ma ustawionej ceny")
                    return
                
                # Sprawdź stan magazynowy
                stock = self.API.get_current_stock(product_id)
                if stock < quantity:
                    messagebox.showerror("Błąd", f"Niewystarczający stan magazynowy. Dostępne: {stock}")
                    return
                
                # Dodaj do listy
                products_to_add.append([product_id, quantity, price])
                products_tree.insert('', 'end', values = (product_id, quantity, f"{price:.2f}"))
                
                # Wyczyść pola
                product_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                
            except ValueError:
                messagebox.showerror("Błąd", "ID produktu i ilość muszą być liczbami")

        ttk.Button(dialog, text = "Dodaj do listy", command = add_product_to_list).grid(row = 4, column = 2, padx = 5, pady = 5)

        def save_order():
            try:
                raw_id = customer_entry.get() # .strip() usuwa przypadkowe spacje
                print(f"Raw customer ID: '{raw_id}'")
                if not raw_id:
                    messagebox.showerror("Błąd", "Wpisz ID klienta!")
                    return
                customer_id = int(raw_id)
                print(customer_id)
                status = status_combo.get()
                
                if not products_to_add:
                    messagebox.showerror("Błąd", "Dodaj przynajmniej jeden produkt do zamówienia")
                    return
                
                order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"DEBUG: customer_id = {customer_id} (typ: {type(customer_id)})")
                result = self.API.create_full_order(customer_id, status, order_date, products_to_add)

                
                if result:
                    messagebox.showinfo("Sukces", f"Zamówienie #{result} zostało utworzone")
                    dialog.destroy()
                    self.refresh_list()
                else:
                    messagebox.showerror("Błąd", "Nie udało się utworzyć zamówienia")
                    
            except ValueError as e:
                print(f"Log błędu: {e}") 
                messagebox.showerror("Błąd", f"Problem z danymi: {e}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się utworzyć zamówienia: {str(e)}")

        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row = 7, column = 0, columnspan = 3, pady = 10)
        ttk.Button(btn_frame, text = "Zapisz zamówienie", command = save_order).pack(side = 'left', padx = 5)
        ttk.Button(btn_frame, text = "Anuluj", command = dialog.destroy).pack(side = 'left', padx = 5)

    def add_order_item_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz zamówienie")
            return

        item = self.tree.item(selected[0])
        order_id = item['values'][0]

        dialog = tk.Toplevel(self)
        dialog.title("Dodaj produkt do zamówienia")
        dialog.geometry("400x200")

        ttk.Label(dialog, text = f"Zamówienie ID: {order_id}").grid(row = 0, column = 0, columnspan = 2, pady = 10)

        ttk.Label(dialog, text = "ID Produktu:").grid(row = 1, column = 0, padx = 10, pady = 5, sticky='w')
        product_entry = ttk.Entry(dialog, width = 30)
        product_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky='w')

        ttk.Label(dialog, text = "Ilość:").grid(row = 2, column = 0, padx = 10, pady = 5, sticky='w')
        quantity_entry = ttk.Entry(dialog, width = 30)
        quantity_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky='w')

        def save():
            try:
                product_id = int(product_entry.get())
                quantity = int(quantity_entry.get())
                
                price = self.API.get_product_price(product_id)
                if price is None:
                    messagebox.showerror("Błąd", "Produkt nie ma ustawionej ceny")
                    return
                
                self.API.add_order_item(order_id, product_id, quantity, price)
                messagebox.showinfo("Sukces", f"Dodano produkt do zamówienia (cena: {price:.2f} zł)")
                dialog.destroy()
                self.refresh_list()
            except ValueError:
                messagebox.showerror("Błąd", "ID produktu i ilość muszą być liczbami")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać produktu: {str(e)}")
                
        ttk.Button(dialog, text = "Zapisz", command = save).grid(row = 3, column = 0, columnspan = 2, pady = 20)

    def delete_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz zamówienie do usunięcia")
            return

        item = self.tree.item(selected[0])
        order_id = item['values'][0]

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć zamówienie?"):
            try:
                self.API.delete_order(order_id)
                messagebox.showinfo("Sukces", "Zamówienie zostało usunięte")
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się usunąć zamówienia: {str(e)}")

    def show_order_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz zamówienie")
            return

        item = self.tree.item(selected[0])
        order_id = item['values'][0]

        dialog = tk.Toplevel(self)
        dialog.title(f"Szczegóły zamówienia #{order_id}")
        dialog.geometry("600x400")

        ttk.Label(dialog, text = f"Zamówienie ID: {order_id}", font = ('Arial', 14, 'bold')).pack(pady = 10)

        details_frame = ttk.LabelFrame(dialog, text = "Produkty w zamówieniu", padding = 10)
        details_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)

        columns = ('Produkt ID', 'Nazwa', 'Ilość', 'Cena jedn.', 'Suma')
        tree = ttk.Treeview(details_frame, columns = columns, show = 'headings', height = 10)

        widths = [80, 200, 80, 100, 100]
        for col, width in zip(columns, widths):
            tree.heading(col, text = col)
            tree.column(col, width = width)

        scrollbar = ttk.Scrollbar(details_frame, orient = 'vertical', command = tree.yview)
        tree.configure(yscrollcommand = scrollbar.set)

        tree.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')

        try:
            details = self.API.get_order_details(order_id)
            total = 0
            for detail in details:
                unit_price = f"{detail['unit_price']:.2f}"
                total_price = f"{detail['total_price']:.2f}"
                tree.insert('', 'end', values = (
                    detail['product_id'],
                    detail['product_name'],
                    detail['quantity'],
                    unit_price,
                    total_price
                ))
                total += detail['total_price']
            
            ttk.Label(dialog, text = f"Suma całkowita: {total:.2f} zł", font = ('Arial', 12, 'bold')).pack(pady = 10)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać szczegółów: {str(e)}")

    def update_order_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz zamówienie do aktualizacji")
            return
        item = self.tree.item(selected[0])
        order_id = item['values'][0]

        dialog = tk.Toplevel(self)
        dialog.title(f"Aktualizuj status zamówienia {order_id}")
        dialog.geometry("300x150")

        ttk.Label(dialog, text = f"Zamówienie nr: {order_id}").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(dialog, text = "Nowy status:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        status_combo = ttk.Combobox(dialog, values = ['w trakcie', 'wysłane', 'dostarczone', 'anulowane', 'nowe'], state = 'readonly')
        status_combo.current(0)
        status_combo.grid(row=1, column=1, padx=10, pady=5)
        def save():
            try:
                new_status = status_combo.get()
                self.API.update_order_status(order_id, new_status)
                messagebox.showinfo("Sukces", "Status zamówienia został zaktualizowany")
                dialog.destroy()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zaktualizować statusu: {str(e)}")
        ttk.Button(dialog, text = "Zapisz", command = save).grid(row=2, column=0, columnspan=2, pady=20)

class ReportsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.API = APIClient()
        self.setupUI()
    
    def setupUI(self):
        header = ttk.Label(self, text = "Raporty", font = ('Arial', 16, 'bold'))
        header.pack(pady = 10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady = 10)

        ttk.Button(btn_frame, text = "Najlepiej sprzedające się produkty", command = self.show_best_selling, width = 30).pack(pady = 5)
        ttk.Button(btn_frame, text = "Historia klienta", command = self.show_customer_history, width = 30).pack(pady = 5)

        result_frame = ttk.LabelFrame(self, text = "Wyniki", padding = 10)
        result_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)

        self.result_text = scrolledtext.ScrolledText(result_frame, width = 80, height = 20, wrap = tk.WORD)
        self.result_text.pack(fill = 'both', expand = True)

    def show_best_selling(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Najlepiej sprzedające się produkty:\n\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")

        try:
            products = self.API.get_best_selling_products(10)
            if not products:
                self.result_text.insert(tk.END, "Brak danych do wyświetlenia.\n")
                return
            for i, p in enumerate(products, 1):
                self.result_text.insert(tk.END, f"{i}. {p['product_name']} - Sprzedane ilości: {p['total_sold_quantity']}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Błąd podczas pobierania danych: {str(e)}\n")
    
    def show_customer_history(self):
        dialog = tk.Toplevel(self)
        dialog.title("Historia klienta")
        dialog.geometry("300x150")

        ttk.Label(dialog, text = "ID klienta:").pack(pady = 20)
        customer_entry = ttk.Entry(dialog)
        customer_entry.pack(pady = 5)

        def show_history():
            try:
                c_id = int(customer_entry.get())
                history = self.API.get_customer_history(c_id)

                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Historia klienta ID: {c_id}\n\n")
                self.result_text.insert(tk.END, "=" * 60 + "\n\n")

                if not history:
                    self.result_text.insert(tk.END, "Brak zamówień dla tego klienta.\n")
                else:
                    for record in history:
                        self.result_text.insert(tk.END, 
                            f"Zamówienie: {record['order_id']} - {record['order_date']}\n"
                            f"  Produkt: {record['product_name']}\n"
                            f"  Ilość: {record['quantity']}, Cena jedn.: {record['unit_price']} zł\n"
                            f"  Status: {record['status']}\n\n")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowe ID klienta")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas pobierania historii: {str(e)}")
                
        ttk.Button(dialog, text = "Pokaż historię", command = show_history).pack(pady = 10)
