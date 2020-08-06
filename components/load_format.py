"""
# GeneratorCSV
# Wersja 4.0 Experimental
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Moduł zarządzający plikiem formatu
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