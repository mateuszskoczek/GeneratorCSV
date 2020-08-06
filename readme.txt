Program tworzy pliki .csv potrzebne do stworzenia kont uczniów i nauczycieli na szkolnej poczcie i Office 365.
Obecnie program obsługuje tylko 4 pliki z danymi. Program tworzy pliki 'email.csv' do eksportu dla szkolnej poczty oraz 'office.csv' do eksportu dla kont office.
Obecna wersja: 3.0
Autorzy: Mateusz Skoczek
dla ZSP Sobolew
luty 2019 - grudzień 2019





Format domyślny plików z danymi:

Legenda:
X - Dane nieznaczące
Q - Pusta linia

Uczniowie:
# <Klasa> <Nazwisko>, <Imie> <X> <Login do librusa> <X>
# <Q>

# Przykład:
# 1a BS Nowak, Adam <NieznaczaceDane> 1234567u <NieznaczaceDane>
#

Nauczyciele:
# <Nazwisko>, <Imie> <X> <Login do Librusa> <X>
# <Q>

# Przykład:
# Nowak, Adam <NieznaczaceDane> 1234567 <NieznaczaceDane>
#

Format można edytować w pliku 'format.py'. Więcej info na dole.





Format domyślny pliku 'office.csv':
Uczniowie:
# <email>,<imie>,<nazwisko>,<imie nazwisko>,uczeń,<klasa>,,,,,,,,,Rzeczpospolita Polska

# Przykład:
# adam.nowak@losobolew.pl,Adam,Nowak,Adam Nowak,uczeń,1a BS,,,,,,,,,Rzeczpospolita Polska

Nauczyciele:
# <email>,<imie>,<nazwisko>,<imie nazwisko>,nauczyciel,,,,,,,,,,Rzeczpospolita Polska

# Przykład:
# adam.nowak@losobolew.pl,Adam,Nowak,Adam Nowak,nauczyciel,,,,,,,,,,Rzeczpospolita Polska





Format domyślny pliku 'email.csv':
Uczniowie:
# <email>,<haslo>,500
|
v
# <imie>.<nazwisko><znacznikklasy:rokukonczeniaszkoly + literaklasy/bs>@losobolew.pl,<loginlibrusa>:<inicjaly>,500

# Przykład:
# adam.nowak2021bs@losobolew.pl,1234567u,500

Nauczyciele:
# <email>,<haslo>,500
|
v
# <imie>.<nazwisko>@losobolew.pl,<loginlibrusa>:<inicjaly>,500

# Przykład:
# adam.nowak@losobolew.pl,1234567,500





Dalsze pojęcia:
błąd programu - błąd programu objawiający się komunikatem
krytyczny błąd programu - nieoczekiwany błąd programu nieobjawiający się komunikatem





Pliki:

changelog.txt
Informacje o zmianach w poszczególnych wersjach programu.

generator.py
Główny plik programu. Jakiekolwiek naruszenie jego zawartości może spowodować krytyczny błąd programu.

instrukcja.txt
Plik z instrukcją użytkowania. Usunięcie tego pliku spowoduje błąd programu.

config.cfg
Plik zawiera ukryte ustawienia programu. Można go edytować, ale należy robić to z rozwagą. Usunięcie go spowoduje błąd programu.
1: Obsługiwane kodowania: 'utf-8', 'cp1252', 'iso-8859-1'

moduly.py
Plik zawierający moduły niezbędne do działania programu. Usunięcie pliku spowoduje błąd programu. Naruszenie jego zawartości może spowodować krytyczny błąd programu.

format.py
Plik ten jest skryptem przetwarzającym dane. W razie zmiany formatu pliku z danymi należy go edytować, lecz nie powinna tego robić osoba początkująca, gdyż błędny kod może spowodować krytyczny błąd programu lub niepożądane wyniki. Usunięcie pliku spowoduje błąd programu.