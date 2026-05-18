## Wstęp

Celem zadania jest wdrożenie aplikacji webowych opartych na frameworkach Flask oraz FastAPI. Aplikacje zostały 
uruchomione z wykorzystaniem serwera ASGI Uvicorn oraz serwera NGINX pełniącego rolę reverse proxy.
Rozwiązanie zostało przygotowane do testów wydajnościowych przy użyciu narzędzia k6 oraz wdrożone na serwerze VPS.

## Zadanie 1
### Aplikacja Flask

Aplikacja Flask implementuje prosty serwis webowy umożliwiający przesyłanie danych użytkownika przy użyciu formularzy 
HTML. Aplikacja składa się ze strony głównej oraz dwóch oddzielnych formularzy odpowiedzialnych za synchroniczne i 
asynchroniczne przetwarzanie danych. Strona główna wyświetla ekran powitalny oraz przyciski nawigacyjne przekierowujące 
użytkownika do formularza synchronicznego lub asynchronicznego. Interfejs użytkownika został przygotowany z 
wykorzystaniem szablonów HTML renderowanych przez silnik Jinja2 oraz plików CSS odpowiedzialnych za wygląd aplikacji.

Formularz synchroniczny służy do pobierania imienia i nazwiska użytkownika. Po przesłaniu formularza metodą POST 
aplikacja przeprowadza walidację danych wejściowych, sprawdzając między innymi poprawność długości danych oraz dozwolone 
znaki. Po poprawnej walidacji dane są zapisywane bezpośrednio do bazy danych przy użyciu biblioteki SQLAlchemy w ramach 
tego samego cyklu żądanie–odpowiedź. Następnie zapisane dane są ponownie pobierane z bazy danych i wyświetlane 
użytkownikowi.

Formularz asynchroniczny został zaimplementowany w osobnym widoku i służy do pobierania nazwy użytkownika oraz numeru 
telefonu. Również w tym przypadku wykonywana jest walidacja danych wejściowych. W przeciwieństwie do formularza 
synchronicznego zapis danych nie odbywa się bezpośrednio podczas obsługi żądania HTTP. Operacja zapisu zostaje 
przekazana do kolejki zadań Celery, która przetwarza zadanie asynchronicznie poza głównym wątkiem aplikacji.

Do obsługi kolejki zadań wykorzystano Redis pełniący rolę brokera wiadomości oraz backendu wyników Celery. 
Po przesłaniu formularza użytkownik zostaje przekierowany do endpointu statusowego umożliwiającego sprawdzenie 
aktualnego stanu zadania asynchronicznego. W zależności od statusu zadania aplikacja wyświetla informacje takie 
jak `PENDING`, `RETRY`, `FAILURE` lub `SUCCESS`. Po poprawnym zakończeniu zadania zapisane dane są pobierane z 
bazy danych i prezentowane użytkownikowi.

Komunikacja z bazą danych została zrealizowana przy użyciu ORM SQLAlchemy. Dane synchroniczne oraz asynchroniczne 
przechowywane są w oddzielnych tabelach bazy danych. Parametry połączenia z bazą danych są pobierane z pliku `.env` 
przy użyciu zmiennych środowiskowych.

Aplikacja Flask została dodatkowo przystosowana do pracy w środowisku ASGI. Oryginalna aplikacja WSGI została opakowana 
przy użyciu `WsgiToAsgi`, co umożliwia jej uruchomienie na serwerze Uvicorn. Podczas wdrożenia aplikacja działa za 
serwerem NGINX pełniącym rolę reverse proxy przekazującego żądania HTTP do aplikacji backendowej.

## Zadanie 2

### Aplikacja FastAPI

Aplikacja FastAPI implementuje serwis webowy umożliwiający synchroniczne oraz asynchroniczne przetwarzanie danych 
użytkownika przy użyciu formularzy HTML. Struktura aplikacji została oparta na routerach FastAPI oraz szablonach 
Jinja2 odpowiedzialnych za generowanie widoków HTML. 

Strona główna aplikacji wyświetla ekran powitalny oraz przyciski umożliwiające przejście do formularza synchronicznego 
lub asynchronicznego. Aplikacja wykorzystuje również statyczne pliki CSS odpowiedzialne za wygląd interfejsu użytkownika. 
Formularz synchroniczny służy do pobierania imienia i nazwiska użytkownika. Dane przesyłane metodą POST są walidowane 
pod względem poprawności długości oraz dozwolonych znaków. Po poprawnej walidacji dane są zapisywane bezpośrednio do 
bazy danych przy użyciu SQLAlchemy w ramach obsługi bieżącego żądania HTTP. Następnie zapisane dane są pobierane z bazy
danych i wyświetlane użytkownikowi. 
Formularz asynchroniczny został przygotowany w osobnym widoku i służy do pobierania nazwy użytkownika oraz numeru
telefonu. Po przeprowadzeniu walidacji danych aplikacja nie zapisuje danych bezpośrednio do bazy danych. Operacja zapisu 
zostaje przekazana do kolejki zadań Celery działającej asynchronicznie. Do komunikacji pomiędzy aplikacją a workerem Celery 
wykorzystano Redis pełniący rolę brokera wiadomości oraz backendu wyników. 

Po utworzeniu zadania użytkownik zostaje przekierowany do endpointu statusowego umożliwiającego monitorowanie aktualnego 
stanu zadania asynchronicznego. W zależności od statusu aplikacja wyświetla informacje takie jak `PENDING`, `RETRY`, 
`FAILURE` lub `SUCCESS`. Po poprawnym zakończeniu zadania zapisane dane są pobierane z bazy danych i prezentowane 
użytkownikowi. Aplikacja wykorzystuje SQLAlchemy ORM do komunikacji z bazą danych PostgreSQL. Dane synchroniczne oraz 
asynchroniczne są przechowywane w oddzielnych tabelach bazy danych. Parametry połączenia z bazą danych pobierane są ze 
zmiennych środowiskowych zdefiniowanych w pliku `.env`. 

FastAPI jest frameworkiem natywnie opartym o ASGI, dlatego aplikacja może zostać bezpośrednio uruchomiona przy użyciu 
serwera Uvicorn bez konieczności dodatkowego opakowywania aplikacji. Wdrożenie aplikacji zostało przygotowane 
z wykorzystaniem serwera NGINX pełniącego rolę reverse proxy przekazującego żądania HTTP do aplikacji backendowej. 