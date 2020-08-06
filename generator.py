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








# ------------ # Import bibliotek zewnętrznych i modułów oraz inicjacja funkcji zapisywania crashlogów # ------------- #

# Funkcja zapisująca crashlogi
def crash(ErrorCode):
    import sys as SS
    import time as TM
    d = TM.localtime()
    name = 'crashlogs/crash_' + str(d[2]) + str(d[1]) + str(d[0]) + str(d[3]) + str(d[4]) + str(d[5]) + '.txt'
    with open(name, 'w') as crash:
        crash.write('Critical error!\n' + ErrorCode)
        SS.exit(0)

# Błędy
E000x00 = "Brak głównego pliku składowego programu ('main.py'). Przywróć plik. (E000x00)"








# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

import os as OS









# ----------------------------------------- # Uruchomienie głównego modułu # ----------------------------------------- #

try:
    fck = open("components/main.py")
except:
    crash(E000x00)
else:
    OS.system("components\main.py")