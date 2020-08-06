"""
# GeneratorCSV
# Wersja 4.0: UC 1
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Główny skrypt uruchamiający
#
"""








# ----------------------------------------- # Definicja kodów dialogowych # ------------------------------------------ #

E000x00 = "Brak głównego pliku składowego programu ('main.py').\nPrzywróć plik. (E000x00)"








# ---------------------------------------- # Import bibliotek zewnętrznych # ----------------------------------------- #

import os as OS
import sys as SS








# ----------------------------------------- # Uruchomienie głównego modułu # ----------------------------------------- #

try:
    fck = open("components\main.py")
except:
    print('Nieoczekiwany wyjatek - nie mozna wygenerowac okna dialogowego bledu\n\nBŁĄD KRYTYCZNY!\n%s') % E000x00
    wait = input('Naciśnij ENTER aby zakończyć')
    SS.exit(0)
else:
    OS.system("components\main.py")
