"""
# GeneratorCSV
# Wersja 4.0 Experimental
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Moduł zarządzający plikiem konfiguracyjnym
#
"""








# ----------------------------------------- # Definicja kodów dialogowych # ------------------------------------------ #

E000x01 = "Brak modułu wywołującego okna dialogowe ('dialog.py').\nPrzywróć plik. (E000x01)"
E001x01 = ["Brak pliku konfiguracyjnego ('config.cfg').\nPrzywróć plik. (E001x01)", True]
E002x00 = ["Bład pliku konfiguracyjnego ('config.cfg').\nNiepoprawna ilość wierszy w pliku\nPrzywróć plik. (E002x00)", True]
E002x01 = ["Bład pliku konfiguracyjnego ('config.cfg').\nNiepoprawne dane w wierszu 1\nPrzywróć plik. (E002x01)", True]
E002x02 = ["Bład pliku konfiguracyjnego ('config.cfg').\nNiepoprawne dane w wierszu 2\nPrzywróć plik. (E002x02)", True]

I001 = ["Pomyślnie zapisano!\nDla niektórych zmian może być wymagane ponowne uruchomienie programu", False]









# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

# Biblioteki zewnętrzne
import sys as SS

# Moduły składowe programu
try:
    import dialog as MDdlg
except ModuleNotFoundError:
    print('Nieoczekiwany wyjatek - nie mozna wygenerowac okna dialogowego bledu\n\nBŁĄD KRYTYCZNY!\n%s') %E000x01
    wait = input('Naciśnij ENTER aby zakończyć')
    SS.exit(0)








# --------------------------------------------------- # Funkcje # ---------------------------------------------------- #

# Wewnętrzna funkcja sprawdzająca błędy pliku konfiguracyjnego
def CheckConfig(settings):
    # Ilość wierszy
    try:
        if len(settings) != 2:
            error = int('x')
    except ValueError:
        MDdlg.Err(E002x00)

    # Linia 1 (0/1)
    try:
        check = int(settings[0])
        if 0 > check > 1:
            error = int('x')
    except ValueError:
        MDdlg.Err(E002x01)

    # Linia 2 (utf-8)
    DostepneKodowanieWyjsciowe = ['utf-8']
    try:
        if settings[1] not in DostepneKodowanieWyjsciowe:
            error = int('x')
    except ValueError:
        MDdlg.Err(E002x02)



# Odczytywanie ustawień z pliku konfiguracyjnego
def read():
    try:
        check = open('.\config.cfg')
    except FileNotFoundError:
        MDdlg.Err(E001x01)
    else:
        with open('.\config.cfg', 'r') as cfg:
            config = cfg.read().split('\n')
            settings = []
            for x in config:
                settings.append(x.split(': ')[1])
            CheckConfig(settings)
            return settings



# Zapis ustawień do pliku konfiguracyjnego
def edit(settings):
    CheckConfig(settings)
    try:
        check = open('.\config.cfg')
    except FileNotFoundError:
        MDdlg.Err(E001x01)
    else:
        SettingsToSave = []
        SettingsToSave.append('Ciemny motyw(0/1): ' + str(settings[0]) + '\n')
        SettingsToSave.append('Kodowanie wyjsciowe: ' + str(settings[1]))
        with open('.\config.cfg', 'w') as cfg:
            for x in SettingsToSave:
                cfg.write(x)
            MDdlg.Inf(I001)