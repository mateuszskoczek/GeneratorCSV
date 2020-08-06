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








# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

# Biblioteki zewnętrzne
import sys as SS



# Moduły składowe programu
try:
    import dialog as MDdlg
except ModuleNotFoundError:
    print('Nie znaleziono modułu programu (dialog.py)\nNie można załadować programu\nKod błędu: E00x0001')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)








# --------------------------------------------------- # Funkcje # ---------------------------------------------------- #

# Wewnętrzna funkcja sprawdzająca błędy pliku konfiguracyjnego
def CheckConfig(settings):
    # Ilość wierszy
    try:
        if len(settings) != 2:
            error = int('x')
    except ValueError:
        MDdlg.err(1)

    # Linia 1 (0/1)
    try:
        check = int(settings[0])
        if 0 > check > 1:
            error = int('x')
    except ValueError:
        MDdlg.err(2)
    # Linia 2 (utf-8)

    DostepneKodowanieWyjsciowe = ['utf-8']
    try:
        if settings[1] not in DostepneKodowanieWyjsciowe:
            error = int('x')
    except ValueError:
        MDdlg.err(3)



# Odczytywanie ustawień z pliku konfiguracyjnego
def read():
    try:
        check = open('.\config.cfg')
    except FileNotFoundError:
        MDdlg.err(0)
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
        MDdlg.err(0)
    else:
        SettingsToSave = []
        SettingsToSave.append('Ciemny motyw(0/1): ' + str(settings[0]) + '\n')
        SettingsToSave.append('Kodowanie wyjsciowe: ' + str(settings[1]))
        with open('.\config.cfg', 'w') as cfg:
            for x in SettingsToSave:
                cfg.write(x)
            MDdlg.inf(0)