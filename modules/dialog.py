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
E.append(["Nie znaleziono pliku konfiguracyjnego (config.cfg).\nPrzywróć plik. (E01x0001)", True]) #0
E.append(["Błąd pliku konfiguracyjnego (config.cfg).\nNiepoprawna ilość wierszy w pliku\nPrzywróć plik. (E01x0011)", True]) #1
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 1\nPrzywróć plik. (E01x0021)", True]) #2
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 2\nPrzywróć plik. (E01x0022)", True]) #3
E.append(["Nie znaleziono pliku składowego (readme.txt)\nPrzywróć plik. (E03x0011)", False]) #4
E.append(["Nie znaleziono pliku formatu (format.fmt).\nPrzywróć plik (E02x0000)", True]) #5
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie uczniów.\nIlość znaczników klasy w formacie uczniów nie jest równa 1 (E02x0102)", False]) #6
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie uczniów.\nIlość znaczników oddziału w formacie uczniów nie jest równa 1 (E02x0103)", False]) #7
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie uczniów.\nIlość znaczników nazwiska w formacie uczniów nie jest równa 1 (E02x0104)", False]) #8
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie uczniów.\nIlość znaczników imienia w formacie uczniów nie jest równa 1 (E02x0105)", False]) #9
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie uczniów.\nIlość znaczników loginu w formacie uczniów nie jest równa 1 (E02x0106)", False]) #10
E.append(["Błąd pliku formatu (format.fmt).\nPusty wiersz w formacie uczniów (E02x0101).", False]) #11
E.append(["Błąd pliku formatu (format.fmt).\nPusty wiersz w formacie nauczycieli (E02x0111).", False]) #12
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie nauczycieli.\nIlość znaczników nazwiska w formacie nauczycieli nie jest równa 1 (E02x0112)", False]) #13
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie nauczycieli.\nIlość znaczników imienia w formacie nauczycieli nie jest równa 1 (E02x0113)", False]) #14
E.append(["Błąd pliku formatu (format.fmt).\nNie poprawne dane w formacie nauczycieli.\nIlość znaczników loginu w formacie nauczycieli nie jest równa 1 (E02x0114)", False]) #15
E.append(["Błąd pliku formatu (format.fmt).\nNiedozwolone znaki w formacie. (E02x0120).", False]) #16
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 4\nPrzywróć plik. (E01x0023)", True]) #17
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 6\nPrzywróć plik. (E01x0024)", True]) #18
E.append(["Bład pliku konfiguracyjnego (config.cfg).\nNiepoprawne dane w wierszu 7\nPrzywróć plik. (E01x0025)", True]) #19
E.append(["Nieznany błąd podczas ładowania pliku konfiguracyjnego (config.cfg). (E01x0000)", True]) #20
E.append(["Nieznany błąd podczas ładowania pliku formatu (format.fmt)). (E02x0000)", True]) #21
E.append(["Nieznany błąd podczas ładowania pliku składowego (readme.txt) (E03x0011)", False]) #22



I = [] # Informacje
I.append(["Pomyślnie zapisano!\nDla niektórych zmian może być wymagane ponowne uruchomienie programu", False]) #0 (I0001)



A = [] # Zapytania
A.append("Czy na pewno chcesz rozpocząć generowanie?") #0 (A0001)
A.append("Czy chcesz zapisać ustawienia?") #1 (A0002)







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
def ask(AskIndex):
    if TKmsb.askokcancel('Pytanie', A[AskIndex]):
        return True
    else:
        return False
