"""
# GeneratorCSV
# Wersja 4.0 Experimental
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Moduł wywołujący okna dialogowe
#
"""








# ----------------------------------------------- # Kody dialogowe # ------------------------------------------------- #

E = [] # Błędy
E.append(["Nie znaleziono pliku konfiguracyjnego (config.cfg).\nPrzywróć plik. (E01x0000)", True]) #0
E.append(["Błąd pliku konfiguracyjnego (config.cfg).\nNiepoprawna ilość wierszy w pliku\nPrzywróć plik. (E01x0001)", True]) #1
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 1\nPrzywróć plik. (E01x0011)", True]) #2
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 2\nPrzywróć plik. (E01x0012)", True]) #3
E.append(["Nie znaleziono pliku składowego (instruction.txt)\nPrzywróć plik. (E03x0010)", False]) #4



I = [] # Informacje
I.append(["Pomyślnie zapisano!\nDla niektórych zmian może być wymagane ponowne uruchomienie programu", False]) #0 (I0001)



A = [] # Zapytania








# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

# Biblioteki zewnętrzne
import sys as SS



# Biblioteki zewnętrzne interfejsu graficznego
from tkinter import messagebox as TKmsb








# --------------------------------------------------- # Funkcje # ---------------------------------------------------- #

# Okno dialogowe błędu
def err(ErrorIndex):
    Message = 'Wystąpił błąd!\n' + E[ErrorIndex][0]
    TKmsb.showerror('Błąd', Message)
    if E[ErrorIndex][1]:
        SS.exit(0)



# Okno dialogowe informacyjne
def inf(InfoIndex):
    TKmsb.showinfo('Informacja', I[InfoIndex][0])
    if I[InfoIndex][1]:
        SS.exit(0)



# Okno dialogowe zapytania
def Ask(AskIndex):
    if TKmsb.askokcancel('Pytanie', A[AskIndex]):
        return True
    else:
        return False
