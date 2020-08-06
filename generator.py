# GeneratorCSV
# Wersja 3.0.1
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew










## Defincja błędów ##############################################################################

# E001 - Brak pliku składowego
E001x00 = "Brak pliku formatu 'moduly.py'.\nPrzywróć plik. (E001x00)"
E001x01 = "Brak pliku formatu 'format.py'.\nPrzywróć plik. (E001x01)"
E001x02 = "Brak pliku konfiguracyjnego 'config.cfg'.\nPrzywróć plik. (E001x02)"
E001x03 = "Brak pliku 'instrukcja.txt'.\nPrzywróć plik. (E001x03)"

# E002 - Błąd pliku składowego
E002x02 = "Nieokreślony błąd pliku konfiguracyjnego 'config.cfg'.\nPrzywróć domyślny plik lub popraw ustawienia. (E002x02)"
E002x021 = "Błąd pliku konfiguracyjnego 'config.cfg'.\nPodane kodowanie nie jest obsługiwane\nPrzywróć domyślny plik lub popraw ustawienia. (E002x021)"

# E003 - Błąd lokalizacji plików I/O
E003x01 = "Nie podano lokalizacji plików do importu. (E003x01)"
E003x02 = "Nie podano lokalizacji zapisu wygenerowanych plików. (E003x02)"
E003x111 = "Plik podany w sciezce 1 nie istnieje (E003x111)"
E003x112 = "Plik podany w sciezce 2 nie istnieje (E003x112)"
E003x113 = "Plik podany w sciezce 3 nie istnieje (E003x113)"
E003x114 = "Plik podany w sciezce 4 nie istnieje (E003x114)"

#_______________________________________________________________________________________________#










## Import bibliotek zewnętrznych ################################################################

import tkinter as tk
import codecs as cd
import os
import time as tm
import sys as ss

# Definicja składowych biblioteki interfejsu graficznego
from tkinter import filedialog as TKfld
from tkinter import messagebox as TKmsb

#_______________________________________________________________________________________________#










## Weryfikacja istnienia plików składowych programu #############################################

try:
    x = open('moduly.py')
except FileNotFoundError:
    Message = 'Wystąpił błąd!\n' + E001x00
    tk.showerror('Błąd', Message)
    ss.exit(0)

try:
    x = open('format.py')
except FileNotFoundError:
    Message = 'Wystąpił błąd!\n' + E001x01
    tk.showerror('Błąd', Message)
    ss.exit(0)

#_______________________________________________________________________________________________#










## Import modułów programu ######################################################################

# Import modułów składowych programu
from moduly import ErrorDialog as MDerr
from moduly import FileCheck as MDfck
from moduly import PolishLetterRemover as MDplr
from moduly import ClassTagCreator as MDctc

# Import skryptu przetwarzającego dane
import format as ft

#_______________________________________________________________________________________________#











## Weryfikacja istnienia plików składowych ######################################################

MDfck('format.py', E001x01)
MDfck('config.cfg', E001x02)
MDfck('instrukcja.txt', E001x03)

#_______________________________________________________________________________________________#











## Wczytywanie pliku konfiguracyjnego ###########################################################

try:
    with open('config.cfg', 'r') as config:
        config = config.read().split('\n')
        Kodowanie = str(config[0].strip('Kodowanie: '))
        TypyKodowania = ['utf-8', 'cp1252', 'iso-8859-1']
        if Kodowanie not in TypyKodowania:
            MDerr(E002x021)
except:
    MDerr(E002x02)

#_______________________________________________________________________________________________#











## Inicjacja skryptu przetwarzającego dane ######################################################

def Main():
    if TKmsb.askokcancel('Ostrzeżenie', "Czy na pewno chcesz rozpocząć generowanie?\nProgram utworzy w podanej lokalizacji pliki 'email.csv' i 'office.csv'.\nJeżeli w podanej lokalizacji istnieją pliki o takich nazwach zostaną one nadpisane."):
        sciezka1 = Pole1.get()
        sciezka1_puste = True
        sciezka2 = Pole2.get()
        sciezka2_puste = True
        sciezka3 = Pole3.get()
        sciezka3_puste = True
        sciezka4 = Pole3.get()
        sciezka4_puste = True
        sciezkaExport = PoleExport.get()
        sciezkaExport_puste = True

        if sciezka1 != '':
            sciezka1_puste = False
        if sciezka2 != '':
            sciezka2_puste = False
        if sciezka3 != '':
            sciezka3_puste = False
        if sciezka4 != '':
            sciezka4_puste = False
        if sciezkaExport != '':
            sciezkaExport_puste = False

        if sciezka1_puste and sciezka2_puste and sciezka3_puste and sciezka4_puste:
            MDerr(E003x01)
        if sciezkaExport_puste:
            MDerr(E003x02)

        KontenerDanych = []
        if not sciezka1_puste:
            try:
                x = open(sciezka1)
            except FileNotFoundError:
                MDerr(E003x111)
            else:
                with open(sciezka1, 'r') as plik1:
                    KontenerDanych += ft.przetworz(plik1.read())
        if not sciezka2_puste:
            try:
                x = open(sciezka2)
            except FileNotFoundError:
                MDerr(E003x112)
            else:
                with open(sciezka2, 'r') as plik2:
                    KontenerDanych += ft.przetworz(plik2.read())
        if not sciezka3_puste:
            try:
                x = open(sciezka3)
            except FileNotFoundError:
                MDerr(E003x113)
            else:
                with open(sciezka3, 'r') as plik3:
                    KontenerDanych += ft.przetworz(plik3.read())
        if not sciezka4_puste:
            try:
                x = open(sciezka4)
            except FileNotFoundError:
                MDerr(E003x114)
            else:
                with open(sciezka4, 'r') as plik4:
                    KontenerDanych += ft.przetworz(plik4.read())

        KontenerEmail = []
        KontenerOffice = []
        for osoba in KontenerDanych:
            if osoba[-1]:
                Klasa = osoba[0]
                Imie = osoba[2]
                Inicjaly = Imie[0]
                Nazwisko = ''
                NazwiskoDoEmaila = ''
                for x in osoba[1]:
                    Nazwisko += x + ' '
                    NazwiskoDoEmaila += ('.' + x)
                    Inicjaly += x[0]
                Nazwisko = Nazwisko[:-1]
                ZnacznikKlasy = MDctc(Klasa)
                Login = osoba[3]
                Adres = MDplr(Imie).lower() + MDplr(NazwiskoDoEmaila).lower() + ZnacznikKlasy + '@losobolew.pl'
                Email = Adres + ',' + Login + ':' + MDplr(Inicjaly) + ',500'
                Office = Adres + ',' + Imie + ',' + Nazwisko + ',' + Imie + ' ' + Nazwisko + ',uczeń,' + Klasa + ',,,,,,,,,Rzeczypospolita Polska'
                KontenerEmail.append(Email)
                KontenerOffice.append(Office)
            else:
                Imie = osoba[1]
                Inicjaly = Imie[0]
                Nazwisko = ''
                NazwiskoDoEmaila = ''
                for x in osoba[0]:
                    Nazwisko += x + ' '
                    NazwiskoDoEmaila += ('.' + x)
                    Inicjaly += x[0]
                Nazwisko = Nazwisko[:-1]
                Login = osoba[2]
                Adres = MDplr(Imie).lower() + MDplr(NazwiskoDoEmaila).lower() + '@losobolew.pl'
                Email = Adres + ',' + Login + ':' + MDplr(Inicjaly) + ',500'
                Office = Adres + ',' + Imie + ',' + Nazwisko + ',' + Imie + ' ' + Nazwisko + ',nauczyciel,,,,,,,,,,Rzeczpospolita Polska'
                KontenerEmail.append(Email)
                KontenerOffice.append(Office)
        sciezkaEmail = sciezkaExport + '/email.csv'
        sciezkaOffice = sciezkaExport + '/office.csv'
        with cd.open(sciezkaEmail, 'w', Kodowanie) as plikEmail:
            for x in KontenerEmail:
                plikEmail.writelines(x + '\n')
            plikEmail.close()
        with cd.open(sciezkaOffice, 'w', Kodowanie) as plikOffice:
            for x in KontenerOffice:
                plikOffice.writelines(x + '\n')
            plikOffice.close()
        TKmsb.showinfo('Zakończono', 'Operacja zakończona pomyślnie')
        ss.exit(0)
    else:
        ss.exit(0)


#_______________________________________________________________________________________________#











## Inicjacja okna ###############################################################################

# Zmienne globalne środowiska graficznego
SzerokoscOpisu = 17
SzerokoscPola = 91
TytulProgramu = 'GeneratorCSV'
Autorzy = 'Mateusz Skoczek'
Wersja = '3.0.1'
Lata = '2019'

# Tworzenie okna
OknoGlowne = tk.Tk()
OknoGlowne.title(TytulProgramu)
OknoGlowne.resizable(width = False, height = False)

# Nazwa programu
Tytul = tk.Label(OknoGlowne, text = TytulProgramu, font = ('Segoe UI Semilight', 20), borderwidth = 7, justify = 'center', bg = 'Gainsboro', width = 47)
Tytul.grid(row = 0)


# Tworzenie frame dla ścieżek plików do importu
Ramka1 = tk.LabelFrame(OknoGlowne, text = 'Pliki do importu zawierające dane')
Ramka1.grid(row = 1)

# Ścieżka pliku do importu 1
wiersz1 = 0
text1 = tk.StringVar()
OpisPola1 = tk.Label(Ramka1, text = 'Plik z danymi (1)', justify = 'left', width = SzerokoscOpisu)
OpisPola1.grid(row = wiersz1, column = 0)
Pole1 = tk.Entry(Ramka1, textvariable = text1, width = SzerokoscPola)
Pole1.grid(row = wiersz1, column = 1)
def Browse1_Dialog():
    Browse1.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
    Pole1.delete(0, 'end')
    Pole1.insert(0, Browse1.filename)
Browse1 = tk.Button(Ramka1, text = '...', command = Browse1_Dialog, background = 'silver', relief = 'flat')
Browse1.grid(row = wiersz1, column = 2, padx = 5, pady = 3)

# Ścieżka pliku do importu 2
wiersz2 = 1
text2 = tk.StringVar()
OpisPola2 = tk.Label(Ramka1, text = 'Plik z danymi (2)', justify = 'left', width = SzerokoscOpisu)
OpisPola2.grid(row = wiersz2, column = 0)
Pole2 = tk.Entry(Ramka1, textvariable = text2, width = SzerokoscPola)
Pole2.grid(row = wiersz2, column = 1)
def Browse2_Dialog():
    Browse2.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
    Pole2.delete(0, 'end')
    Pole2.insert(0, Browse2.filename)
Browse2 = tk.Button(Ramka1, text = '...', command = Browse2_Dialog, background = 'silver', relief = 'flat')
Browse2.grid(row = wiersz2, column = 2, padx = 5, pady = 3)

# Ścieżka pliku do importu 3
wiersz3 = 2
text3 = tk.StringVar()
OpisPola3 = tk.Label(Ramka1, text = 'Plik z danymi (3)', justify = 'left', width = SzerokoscOpisu)
OpisPola3.grid(row = wiersz3, column = 0)
Pole3 = tk.Entry(Ramka1, textvariable = text3, width = SzerokoscPola)
Pole3.grid(row = wiersz3, column = 1)
def Browse3_Dialog():
    Browse3.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
    Pole3.delete(0, 'end')
    Pole3.insert(0, Browse3.filename)
Browse3 = tk.Button(Ramka1, text = '...', command = Browse3_Dialog, background = 'silver', relief = 'flat')
Browse3.grid(row = wiersz3, column = 2, padx = 5, pady = 3)

# Ścieżka pliku do importu 4
wiersz4 = 3
text4 = tk.StringVar()
OpisPola4 = tk.Label(Ramka1, text = 'Plik z danymi (4)', justify = 'left', width = SzerokoscOpisu)
OpisPola4.grid(row = wiersz4, column = 0)
Pole4 = tk.Entry(Ramka1, textvariable = text4, width = SzerokoscPola)
Pole4.grid(row = wiersz4, column = 1)
def Browse4_Dialog():
    Browse4.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
    Pole4.delete(0, 'end')
    Pole4.insert(0, Browse4.filename)
Browse4 = tk.Button(Ramka1, text = '...', command = Browse4_Dialog, background = 'silver', relief = 'flat')
Browse4.grid(row = wiersz4, column = 2, padx = 5, pady = 3)


# Tworzenie frame dla plików export
Ramka2 = tk.LabelFrame(OknoGlowne, text = 'Ustawienia eksportu')
Ramka2.grid(row = 2)

# Ścieżka folderu do zapisu wygenerowanych plików
text4 = tk.StringVar()
OpisPolaExport = tk.Label(Ramka2, text = 'Lokalizacja', justify = 'left', width = SzerokoscOpisu)
OpisPolaExport.grid(row = 0, column = 0)
PoleExport = tk.Entry(Ramka2, textvariable = text4, width = SzerokoscPola)
PoleExport.grid(row = 0, column = 1)
def BrowseExport_Dialog():
    BrowseExport.filename = TKfld.askdirectory()
    PoleExport.delete(0, 'end')
    PoleExport.insert(0, BrowseExport.filename)
BrowseExport = tk.Button(Ramka2, text = '...', command = BrowseExport_Dialog, background = 'silver', relief = 'flat')
BrowseExport.grid(row = 0, column = 2, padx = 5, pady = 3)


# Przycisk START
Przycisk = tk.Button(OknoGlowne, text = 'START', justify = 'center', width = 50, command = Main, relief = 'flat', background = 'silver')
Przycisk.grid(row = 3, pady = 15)


# Pasek dolny
PasekDolny = tk.LabelFrame(OknoGlowne, bd = 0, background = 'Gainsboro')
PasekDolny.grid(row = 4)
info = TytulProgramu + ' ' + Wersja + ' | © ' + Autorzy + ' '+ Lata + ' dla ZSP Sobolew'
InfoLabel = tk.Label(PasekDolny, text = info, justify = 'left', width = 93, anchor = 'w', background = 'Gainsboro')
InfoLabel.grid(row= 0, column = 0)
def InfoOpen():
    try:
        x = open('instrukcja.txt')
    except FileNotFoundError:
        MDerr(E001x03)
    else:
        os.system("notepad instrukcja.txt")
Przycisk = tk.Button(PasekDolny, text = 'Instrukcja', justify = 'center', foreground = 'blue', relief = 'flat', command = InfoOpen, background = 'Gainsboro')
Przycisk.grid(row = 0, column = 1)


tk.mainloop()

#_______________________________________________________________________________________________#
