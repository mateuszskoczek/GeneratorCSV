"""
# GeneratorCSV
# Wersja 4.0 Experimental
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Główny skrypt uruchamiający
#
"""








# ----------------------------------------- # Uruchomienie głównego modułu # ----------------------------------------- #

try:
    fck = open("components/main.py")
except:
    print('Nie znaleziono głównego modułu programu (main.py)\nNie można załadować programu\nKod błędu: E00x0000')
    wait = input('Naciśnij ENTER aby wyjść')
else:
    import os
    os.system("components\main.py")