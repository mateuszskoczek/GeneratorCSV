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





# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

# Biblioteki zewnętrzne
import sys as SS

# Biblioteki zewnętrzne interfejsu graficznego
from tkinter import messagebox as TKmsb








# --------------------------------------------------- # Funkcje # ---------------------------------------------------- #

# Okno dialogowe błędu
def Err(KodBledu):
    Message = 'Wystąpił błąd!\n' + KodBledu[0]
    TKmsb.showerror('Błąd', Message)
    if KodBledu[1]:
        SS.exit(0)



# Okno dialogowe informacyjne
def Inf(KodInformacji):
    TKmsb.showinfo('Informacja', KodInformacji[0])
    if KodInformacji[1]:
        SS.exit(0)



# Okno dialogowe zapytania
def Ask(KodZapytania):
    if TKmsb.askokcancel('Pytanie', KodZapytania):
        return True
    else:
        return False
