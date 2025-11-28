🛒 System Zarządzania Zamówieniami i Magazynem E-commerce
📝 Opis Projektu
Ten projekt stanowi implementację Backendu (API) dla systemu zarządzania zamówieniami, klientami i magazynem, wykorzystując relacyjną bazę danych SQLite. Jest to aplikacja typu thick client (lub API dla lokalnej aplikacji GUI), której głównym celem jest zapewnienie bezpiecznej i transakcyjnej obsługi procesów biznesowych (np. tworzenie zamówień i obsługa zapasów).
⚙️ Architektura
Baza Danych: SQLite
Język i Logika: Python
Backend / API: Flask
Dokumentacja API: Flasgger (automatycznie generowana specyfikacja OpenAPI)
🚀 Uruchomienie Projektu
Aby uruchomić serwer API, wykonaj poniższe kroki.
1. Klonowanie Repozytorium (jeśli dotyczy)
Jeśli używasz Git:
Bashgit clone [ADRES_TWOJEGO_REPOSITORIUM]
cd [NAZWA_KATALOGU_PROJEKTU]
2. Konfiguracja Środowiska Wirtualnego
Zaleca się użycie wirtualnego środowiska (.venv) dla izolacji zależności:
Bash
# Tworzenie środowiska
python -m venv .venv

# Aktywacja środowiska
# Windows (PowerShell):
.venv\Scripts\Activate
# macOS / Linux (Bash):
source .venv/bin/activate
3. Instalacja Zależności
Zainstaluj wszystkie wymagane biblioteki Pythona (Flask, Flasgger, itp.):
Bash
pip install flask flasgger flask-cors
# Opcjonalnie: jeśli masz plik requirements.txt:
# pip install -r requirements.txt
4. Inicjalizacja Bazy Danych
Uruchom skrypt, który utworzy plik sklep.db i zdefiniuje w nim wszystkie niezbędne tabele:
Bash
python database_init.py
(Ten skrypt powinien być uruchamiany tylko raz, chyba że chcesz zresetować całą bazę.)
5. Uruchomienie Serwera APIUruchom serwer Flask. Domyślnie serwer będzie dostępny pod adresem http://127.0.0.1:5000/.
Bash
python api.py
💡 Użycie API i Dokumentacja
Po uruchomieniu serwera, możesz uzyskać dostęp do API za pomocą narzędzi takich jak Postman, curl, lub bezpośrednio z Twojego frontendu (np. GUI Tkinter).
📄 Dokumentacja Swagger UI
Pełna, interaktywna dokumentacja wszystkich punktów końcowych (endpointów) API jest dostępna automatycznie dzięki bibliotece Flasgger:
➡️ Adres Dokumentacji: http://127.0.0.1:5000/apidocs/
🔑 Kluczowe Endpointy
Endpoint Metoda Opis
-/api/health - GET - Sprawdzenie, czy serwer działa poprawnie.
-/api/customers - POST - Dodanie nowego klienta.
-/api/products - GET - Pobranie listy wszystkich produktów.
-/api/products/{id}/stock - GET - Pobranie aktualnego stanu magazynowego.
/api/orders/transaction - POST - Najważniejsza transakcja: Tworzenie zamówienia wraz ze sprawdzeniem zapasów.
🧪 Struktura Plików
Plik/Katalog Rola
-api.py - Warstwa API (Endpointy): Definiuje wszystkie trasy Flask i zawiera logikę walidacji/wywołań.
-backend.py - Warstwa Logiki Biznesowej/Danych: Zawiera wszystkie funkcje Pythona do interakcji z bazą (add_customer, create_order_transaction, itp.).
-database_init.py - Inicjalizacja: Skrypt do tworzenia schematu bazy danych (tabel).sklep.
-db - Główny plik bazy danych SQLite.
-.venv/ - Wirtualne środowisko Pythona.
🛑 Wyłączanie Serwera
Aby zatrzymać działanie serwera API, naciśnij Ctrl + C w oknie terminala.