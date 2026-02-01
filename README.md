# 🛒 System Zarządzania Zamówieniami i Magazynem E-commerce
# 📝 Opis Projektu
Ten projekt stanowi implementację Backendu (API) oraz frontendu dla systemu zarządzania zamówieniami, klientami i magazynem, wykorzystując relacyjną bazę danych SQLite. Jest to aplikacja typu thick client (lub API dla lokalnej aplikacji GUI), której głównym celem jest zapewnienie bezpiecznej i transakcyjnej obsługi procesów biznesowych (np. tworzenie zamówień i obsługa zapasów).
⚙️ Architektura
Baza Danych: SQLite
Język i Logika: Python
Backend / API: Flask
Frontend: tkinter
Dokumentacja API: Flasgger (automatycznie generowana specyfikacja OpenAPI)
# 🚀 Uruchomienie Projektu
Aby uruchomić serwer API, wykonaj poniższe kroki.
# 1. Klonowanie Repozytorium (jeśli dotyczy)
Jeśli używasz Git:
Bashgit clone [ADRES_TWOJEGO_REPOSITORIUM]
cd [NAZWA_KATALOGU_PROJEKTU]
# 2. Konfiguracja Środowiska Wirtualnego
Zaleca się użycie wirtualnego środowiska (.venv) dla izolacji zależności:
Bash
# Tworzenie środowiska
python -m venv .venv

# Aktywacja środowiska
# Windows (PowerShell):
.venv\Scripts\Activate
# macOS / Linux (Bash):
source .venv/bin/activate
# 3. Instalacja Zależności
Zainstaluj wszystkie wymagane biblioteki Pythona (Flask, Flasgger, itp.):
Bash
pip install flask flasgger flask-cors
# Opcjonalnie: jeśli masz plik requirements.txt:
# pip install -r requirements.txt
# 4. Uruchomienie pełnej aplikacji
W celu zainicjowania bazy danych (utworzenie pliku .db), zapełnienia bazy danymi i uruchomienia GUI odpal plik main.py
Bash
python ./main.py
# 5. Inicjalizacja Bazy Danych
Jeśli chcesz uruchamiać pliki pojedynczo, uruchom skrypt, który utworzy plik sklep.db i zdefiniuje w nim wszystkie niezbędne tabele:
Bash
python ./database_init.py
(Ten skrypt powinien być uruchamiany tylko raz, chyba że chcesz zresetować całą bazę.)
# 6. Uruchomienie Serwera API
Uruchom serwer Flask. Domyślnie serwer będzie dostępny pod adresem http://127.0.0.1:5000/.
Bash
python api.py
# 💡 Użycie API i Dokumentacja
Po uruchomieniu serwera, możesz uzyskać dostęp do API za pomocą narzędzi takich jak Postman, curl, lub bezpośrednio z frontendu.
# 📄 Dokumentacja Swagger UI
Pełna, interaktywna dokumentacja wszystkich punktów końcowych (endpointów) API jest dostępna automatycznie dzięki bibliotece Flasgger:
# ➡️ Adres Dokumentacji: http://127.0.0.1:5000/apidocs/
# 🔑 Kluczowe Endpointy
Endpoint Metoda Opis
-/api/health - GET - Sprawdzenie, czy serwer działa poprawnie.
-/api/customers - POST - Dodanie nowego klienta.
-/api/products - GET - Pobranie listy wszystkich produktów.
-/api/products/{id}/stock - GET - Pobranie aktualnego stanu magazynowego.
/api/orders/transaction - POST - Najważniejsza transakcja: Tworzenie zamówienia wraz ze sprawdzeniem zapasów.
# 📂 Kluczowe komponenty aplikacji (Logika i Serwer)
main.py – (Warstwa Startowa): Odpala całą funkcjonalność aplikacji: tworzy bazę danych, zapełnia ją losowymi danymi i uruchamia GUI.
backend.py – (Warstwa Logiki Biznesowej/Danych): Zawiera wszystkie funkcje Pythona do interakcji z bazą (add_customer, create_order_transaction, itp.).
api.py – (Warstwa API / Endpointy): Definiuje wszystkie trasy Flask i zawiera logikę walidacji/wywołań.
api_client.py – (Warstwa Komunikacji): Ułatwia komunikację między front i backendem.
# 🖥️ Interfejs Użytkownika (Frontend)
gui_app.py – (Warstwa Prezentacji): Główny plik frontendu. Tworzy okno i inicjuje wszystkie funkcje opisane w views.py.
views.py – (Warstwa Prezentacji): Kod frontendu. Znajdują się tu wszystkie widoki i ich szata graficzna.
# 🗄️ Baza Danych i Inicjalizacja
database_init.py – (Warstwa Konfiguracyjna): Inicjalizacja: Skrypt do tworzenia schematu bazy danych (tabel).
seed_data.py – (Warstwa Danych): Zapełnia bazę losowymi danymi.
db (np. sklep.db) – (Warstwa Danych): Główny plik bazy danych SQLite.
🛠️ Pliki Pomocnicze i Deployment
main.spec – (Warstwa Budowania): Plik utworzony przy pakowaniu pliku main.py do .exe przy użyciu pyinstallera.
shopp.ico – (Zasoby): Ikona pliku .exe.
test_backend.py – (Warstwa Testowa): Funkcje do testowania backendu, pozostałość po poprzednim etapie projektu.
.venv/ – (Środowisko): Wirtualne środowisko Pythona.
🛑 Wyłączanie Serwera
Aby zatrzymać działanie serwera API, naciśnij Ctrl + C w oknie terminala.
