import sys
import os
from database_init import init_db
from seed_data import seed_database as seed_all
from gui_app import main as run_gui_app

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sklep.db')

def start_app():
    print(f"[DEBUG] Szukam bazy w: {DB_FILE}")
    if not os.path.exists(DB_FILE):
        print("Inicjalizacja bazy danych...")
        init_db(DB_FILE)

        print("Zapełnianie bazy danych...")
        seed_all(DB_FILE)
    else:
        print("Baza danych już istnieje. Pomijanie inicjalizacji.")
    print("Uruchamianie GUI...")
    run_gui_app()

if __name__ == "__main__":
    start_app()