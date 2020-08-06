"""
# Generator CSV
# Wersja 4.0 Experimental
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Główny plik programu
#
"""








# -------------------------------------------- # Informacje o programie # -------------------------------------------- #

Nazwa = 'Generator CSV'
Wersja = '4.0 Experimental'
LataPracy = '2019'
Autorzy = 'Mateusz Skoczek'








# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

# Biblioteki zewnętrzne
import os as OS
import sys as SS



# Moduły składowe programu
try:
    from modules import dialog as MDdlg
except ModuleNotFoundError:
    print('Wystąpił krytyczny błąd!')
    print('Nie znaleziono jednego z modułów programu (dialog.py). Nie można załadować programu')
    print('Kod błędu: E00x0011')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)
except Exception as exc:
    print('Wystąpił krytyczny błąd!')
    print('Nieznany błąd podczas ładowania jednego z modułów programu (dialog.py). Nie można załadować programu.')
    print('Treść błędu: ' + exc)
    print('Kod błędu: E00x0010')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)

try:
    from modules import load_config as MDlcg
except ModuleNotFoundError:
    print('Wystąpił krytyczny błąd!')
    print('Nie znaleziono jednego z modułów programu (load_config.py). Nie można załadować programu')
    print('Kod błędu: E00x0021')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)
except Exception as exc:
    print('Wystąpił krytyczny błąd!')
    print('Nieznany błąd podczas ładowania jednego z modułów programu (load_config.py). Nie można załadować programu.')
    print('Treść błędu: ' + exc)
    print('Kod błędu: E00x0020')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)

try:
    from modules import load_format as MDlfm
except ModuleNotFoundError:
    print('Wystąpił krytyczny błąd!')
    print('Nie znaleziono jednego z modułów programu (load_format.py). Nie można załadować programu')
    print('Kod błędu: E00x0031')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)
except Exception as exc:
    print('Wystąpił krytyczny błąd!')
    print('Nieznany błąd podczas ładowania jednego z modułów programu (load_format.py). Nie można załadować programu.')
    print('Treść błędu: ' + exc)
    print('Kod błędu: E00x0030')
    wait = input('Naciśnij ENTER aby wyjść')
    SS.exit(0)


# Biblioteki zewnętrzne interfejsu graficznego
import tkinter as TK

from tkinter import filedialog as TKfld
from tkinter import ttk as TKttk









# ------------------------------------- # Uruchomienie interfejsu graficznego # -------------------------------------- #

# Zmienne globalne środowiska graficznego
if int(MDlcg.read()[0]) == 1:
    CiemnyMotyw = True
else:
    CiemnyMotyw = False
SzerokoscOpisu = 17
SzerokoscOpisu2 = 30
SzerokoscOpisu3 = 10
SzerokoscPola = 122
SzerokoscPola2 = 107
SzerokoscPola3 = 130



# Zmienne motywu
if CiemnyMotyw:
    ZmienneMotywu = ['#1F1F1F', '#191919', '#B8B8B8', '#FFFFFF', '#404040', '#FFFFFF', '#1F1F1F', 1]
else:
    ZmienneMotywu = ['#F0F0F0', '#D4D4D4', '#000000', '#000000', '#A6A6A6', '#000000', '#FFFFFF', 2]

M_tlo = ZmienneMotywu[0]
M_tytultlo = ZmienneMotywu[1]
M_tytultext = ZmienneMotywu[2]
M_text = ZmienneMotywu[3]
M_przycisktlo = ZmienneMotywu[4]
M_przycisktext = ZmienneMotywu[5]
M_entrytlo = ZmienneMotywu[6]
M_framewielkosc = ZmienneMotywu[7]



# Okno główne
class Main(TK.Tk):
    def __init__(self):
        # Ustawienia okna
        TK.Tk.__init__(self)
        self.title(Nazwa + " " + Wersja)
        self.resizable(width = False, height = False)
        self.configure(bg = M_tlo)


        # Tytuł
        Tytul = TK.Label(self)
        Tytul.config(text = Nazwa)
        Tytul.config(width = 41)
        Tytul.config(bg = M_tytultlo)
        Tytul.config(fg = M_tytultext)
        Tytul.config(font = ('Segoe UI Semilight', 30))
        Tytul.grid(row = 0)


        # Frame1 - Pliki z danymi
        Ramka1 = TK.LabelFrame(self)
        Ramka1.config(text=' Pliki tekstowe zawierające dane (wymagany przynajmniej jeden) ')
        Ramka1.config(borderwidth = M_framewielkosc)
        Ramka1.config(bg = M_tlo)
        Ramka1.config(fg = M_text)
        Ramka1.grid(row = 1)


        # Ścieżka pliku txt nr 1
        wiersz = 1
        text1 = TK.StringVar()

        Pole1Label = TK.Label(Ramka1)
        Pole1Label.config(text = 'Plik z danymi (1)')
        Pole1Label.config(width = SzerokoscOpisu)
        Pole1Label.config(bg = M_tlo)
        Pole1Label.config(fg = M_text)
        Pole1Label.grid(row = wiersz, column = 0)

        Pole1 = TK.Entry(Ramka1)
        Pole1.config(textvariable = text1)
        Pole1.config(width = SzerokoscPola)
        Pole1.config(bg = M_entrytlo)
        Pole1.config(fg = M_text)
        Pole1.grid(row = wiersz, column = 1)

        def Pole1BrowseDialog():
            Pole1Browse.filename = TKfld.askopenfilename(initialdir = "C:/", title = "Wybierz plik tekstowy z danymi", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
            Pole1.delete(0, 'end')
            Pole1.insert(0, Pole1Browse.filename)

        Pole1Browse = TK.Button(Ramka1)
        Pole1Browse.config(text = '...')
        Pole1Browse.config(command = Pole1BrowseDialog)
        Pole1Browse.config(bg = M_przycisktlo)
        Pole1Browse.config(fg = M_przycisktext)
        Pole1Browse.config(relief = 'flat')
        Pole1Browse.config(activebackground = M_przycisktlo)
        Pole1Browse.grid(row = wiersz, column = 2, padx=5, pady=3)


        # Ścieżka pliku txt nr 2
        wiersz = 2
        text2 = TK.StringVar()

        Pole2Label = TK.Label(Ramka1)
        Pole2Label.config(text = 'Plik z danymi (2)')
        Pole2Label.config(width = SzerokoscOpisu)
        Pole2Label.config(bg = M_tlo)
        Pole2Label.config(fg = M_text)
        Pole2Label.grid(row = wiersz, column = 0)

        Pole2 = TK.Entry(Ramka1)
        Pole2.config(textvariable = text2)
        Pole2.config(width = SzerokoscPola)
        Pole2.config(bg = M_entrytlo)
        Pole2.config(fg = M_text)
        Pole2.grid(row = wiersz, column = 1)

        def Pole2BrowseDialog():
            Pole2Browse.filename = TKfld.askopenfilename(initialdir = "C:/", title = "Wybierz plik tekstowy z danymi", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
            Pole2.delete(0, 'end')
            Pole2.insert(0, Pole2Browse.filename)

        Pole2Browse = TK.Button(Ramka1)
        Pole2Browse.config(text = '...')
        Pole2Browse.config(command = Pole2BrowseDialog)
        Pole2Browse.config(bg = M_przycisktlo)
        Pole2Browse.config(fg = M_przycisktext)
        Pole2Browse.config(relief = 'flat')
        Pole2Browse.config(activebackground = M_przycisktlo)
        Pole2Browse.grid(row = wiersz, column = 2, padx = 5, pady = 3)

        # Ścieżka pliku txt nr 3
        wiersz = 3
        text3 = TK.StringVar()

        Pole3Label = TK.Label(Ramka1)
        Pole3Label.config(text = 'Plik z danymi (3)')
        Pole3Label.config(width = SzerokoscOpisu)
        Pole3Label.config(bg = M_tlo)
        Pole3Label.config(fg = M_text)
        Pole3Label.grid(row = wiersz, column = 0)

        Pole3 = TK.Entry(Ramka1)
        Pole3.config(textvariable = text3)
        Pole3.config(width = SzerokoscPola)
        Pole3.config(bg = M_entrytlo)
        Pole3.config(fg = M_text)
        Pole3.grid(row = wiersz, column = 1)

        def Pole3BrowseDialog():
            Pole3Browse.filename = TKfld.askopenfilename(initialdir = "C:/", title = "Wybierz plik tekstowy z danymi", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
            Pole3.delete(0, 'end')
            Pole3.insert(0, Pole3Browse.filename)

        Pole3Browse = TK.Button(Ramka1)
        Pole3Browse.config(text = '...')
        Pole3Browse.config(command = Pole3BrowseDialog)
        Pole3Browse.config(bg = M_przycisktlo)
        Pole3Browse.config(fg = M_przycisktext)
        Pole3Browse.config(relief = 'flat')
        Pole3Browse.config(activebackground = M_przycisktlo)
        Pole3Browse.grid(row = wiersz, column = 2, padx = 5, pady = 3)


        # Frame2 - Dołącz pliki .csv
        Ramka2 = TK.LabelFrame(self)
        Ramka2.config(text = ' Dołącz pliki .csv (opcjonalne) ')
        Ramka2.config(borderwidth = M_framewielkosc)
        Ramka2.config(bg = M_tlo)
        Ramka2.config(fg = M_text)
        Ramka2.grid(row = 2)


        # Sciezka do konta.csv
        wiersz = 1
        textKonta = TK.StringVar()

        PoleKontaLabel = TK.Label(Ramka2)
        PoleKontaLabel.config(text = 'Ściezka do pliku .csv dla poczty')
        PoleKontaLabel.config(width = SzerokoscOpisu2)
        PoleKontaLabel.config(bg = M_tlo)
        PoleKontaLabel.config(fg = M_text)
        PoleKontaLabel.grid(row = wiersz, column = 0)

        PoleKonta = TK.Entry(Ramka2)
        PoleKonta.config(textvariable = textKonta)
        PoleKonta.config(width = SzerokoscPola2)
        PoleKonta.config(bg = M_entrytlo)
        PoleKonta.config(fg = M_text)
        PoleKonta.grid(row = wiersz, column = 1)

        def PoleKontaBrowseDialog():
            PoleKontaBrowse.filename = TKfld.askopenfilename(initialdir="C:/", title="Wybierz plik .csv dla poczty", filetypes=(("Pliki csv", "*.csv"), ("Wszystkie pliki", "*.*")))
            PoleKonta.delete(0, 'end')
            PoleKonta.insert(0, PoleKontaBrowse.filename)

        PoleKontaBrowse = TK.Button(Ramka2)
        PoleKontaBrowse.config(text = '...')
        PoleKontaBrowse.config(command = PoleKontaBrowseDialog)
        PoleKontaBrowse.config(bg = M_przycisktlo)
        PoleKontaBrowse.config(fg = M_przycisktext)
        PoleKontaBrowse.config(relief = 'flat')
        PoleKontaBrowse.config(activebackground = M_przycisktlo)
        PoleKontaBrowse.grid(row = wiersz, column = 2, padx = 5, pady = 3)


        # Sciezka do office.csv
        wiersz = 2
        textOffice = TK.StringVar()

        PoleOfficeLabel = TK.Label(Ramka2)
        PoleOfficeLabel.config(text = 'Ściezka do pliku .csv dla office365')
        PoleOfficeLabel.config(width = SzerokoscOpisu2)
        PoleOfficeLabel.config(bg = M_tlo)
        PoleOfficeLabel.config(fg = M_text)
        PoleOfficeLabel.grid(row = wiersz, column = 0)

        PoleOffice = TK.Entry(Ramka2)
        PoleOffice.config(textvariable = textOffice)
        PoleOffice.config(width = SzerokoscPola2)
        PoleOffice.config(bg = M_entrytlo)
        PoleOffice.config(fg = M_text)
        PoleOffice.grid(row = wiersz, column = 1)

        def PoleOfficeBrowseDialog():
            PoleOfficeBrowse.filename = TKfld.askopenfilename(initialdir = "C:/", title = "Wybierz plik .csv dla poczty", filetypes = (("Pliki csv", "*.csv"), ("Wszystkie pliki", "*.*")))
            PoleOffice.delete(0, 'end')
            PoleOffice.insert(0, PoleOfficeBrowse.filename)

        PoleOfficeBrowse = TK.Button(Ramka2)
        PoleOfficeBrowse.config(text = '...')
        PoleOfficeBrowse.config(command = PoleKontaBrowseDialog)
        PoleOfficeBrowse.config(bg = M_przycisktlo)
        PoleOfficeBrowse.config(fg = M_przycisktext)
        PoleOfficeBrowse.config(relief = 'flat')
        PoleOfficeBrowse.config(activebackground = M_przycisktlo)
        PoleOfficeBrowse.grid(row = wiersz, column = 2, padx = 5, pady = 3)


        # Frame3 - Eksport
        Ramka3 = TK.LabelFrame(self)
        Ramka3.config(text=' Eksport ')
        Ramka3.config(borderwidth = M_framewielkosc)
        Ramka3.config(bg = M_tlo)
        Ramka3.config(fg = M_text)
        Ramka3.grid(row = 3)


        # Sciezka do pliku poczty
        wiersz = 1
        textKontaEksport = TK.StringVar()

        PoleKontaEksportLabel = TK.Label(Ramka3)
        PoleKontaEksportLabel.config(text = 'Poczta')
        PoleKontaEksportLabel.config(width = SzerokoscOpisu3)
        PoleKontaEksportLabel.config(bg = M_tlo)
        PoleKontaEksportLabel.config(fg = M_text)
        PoleKontaEksportLabel.grid(row = wiersz, column = 0)

        PoleKontaEksport = TK.Entry(Ramka3)
        PoleKontaEksport.config(textvariable = textKontaEksport)
        PoleKontaEksport.config(width = SzerokoscPola3)
        PoleKontaEksport.config(bg = M_entrytlo)
        PoleKontaEksport.config(fg = M_text)
        PoleKontaEksport.grid(row = wiersz, column = 1)

        def PoleKontaEksportBrowseDialog():
            PoleKontaEksportBrowse.filename = TKfld.saveasfilename(initialdir = "C:/", title = "Zapisz", filetypes = (("Pliki csv", "*.csv"), ("Wszystkie pliki", "*.*")))
            PoleKontaEksport.delete(0, 'end')
            PoleKontaEksport.insert(0, PoleKontaEksportBrowse.filename)

        PoleKontaEksportBrowse = TK.Button(Ramka3)
        PoleKontaEksportBrowse.config(text = '...')
        PoleKontaEksportBrowse.config(command = PoleKontaEksportBrowseDialog)
        PoleKontaEksportBrowse.config(bg = M_przycisktlo)
        PoleKontaEksportBrowse.config(fg = M_przycisktext)
        PoleKontaEksportBrowse.config(relief = 'flat')
        PoleKontaEksportBrowse.config(activebackground = M_przycisktlo)
        PoleKontaEksportBrowse.grid(row = wiersz, column = 2, padx = 5, pady = 3)

        # Sciezka do pliku office
        wiersz = 2
        textOfficeEksport = TK.StringVar()

        PoleOfficeEksportLabel = TK.Label(Ramka3)
        PoleOfficeEksportLabel.config(text = 'Office')
        PoleOfficeEksportLabel.config(width = SzerokoscOpisu3)
        PoleOfficeEksportLabel.config(bg = M_tlo)
        PoleOfficeEksportLabel.config(fg = M_text)
        PoleOfficeEksportLabel.grid(row = wiersz, column = 0)

        PoleOfficeEksport = TK.Entry(Ramka3)
        PoleOfficeEksport.config(textvariable = textOfficeEksport)
        PoleOfficeEksport.config(width = SzerokoscPola3)
        PoleOfficeEksport.config(bg = M_entrytlo)
        PoleOfficeEksport.config(fg = M_text)
        PoleOfficeEksport.grid(row = wiersz, column = 1)

        def PoleOfficeEksportBrowseDialog():
            PoleOfficeEksportBrowse.filename = TKfld.saveasfilename(initialdir = "C:/", title = "Zapisz", filetypes = (("Pliki csv", "*.csv"), ("Wszystkie pliki", "*.*")))
            PoleOfficeEksport.delete(0, 'end')
            PoleOfficeEksport.insert(0, PoleOfficeEksportBrowse.filename)

        PoleOfficeEksportBrowse = TK.Button(Ramka3)
        PoleOfficeEksportBrowse.config(text = '...')
        PoleOfficeEksportBrowse.config(command = PoleOfficeEksportBrowseDialog)
        PoleOfficeEksportBrowse.config(bg = M_przycisktlo)
        PoleOfficeEksportBrowse.config(fg = M_przycisktext)
        PoleOfficeEksportBrowse.config(relief = 'flat')
        PoleOfficeEksportBrowse.config(activebackground = M_przycisktlo)
        PoleOfficeEksportBrowse.grid(row = wiersz, column = 2, padx = 5, pady = 3)

        # Przycisk START
        def PathPreprocess():
            pass

        PrzyciskSTART = TK.Button(self)
        PrzyciskSTART.config(text = 'START')
        PrzyciskSTART.config(command = PathPreprocess)
        PrzyciskSTART.config(width = 50)
        PrzyciskSTART.config(bg = M_przycisktlo)
        PrzyciskSTART.config(fg = M_przycisktext)
        PrzyciskSTART.config(relief = 'flat')
        PrzyciskSTART.config(activebackground = M_przycisktlo)
        PrzyciskSTART.grid(row = 4, pady = 15)

        # Pasek dolny
        PasekDolny = TK.LabelFrame(self)
        PasekDolny.config(bd = 0)
        PasekDolny.config(bg = M_tytultlo)
        PasekDolny.config(fg = M_tytultext)
        PasekDolny.grid(row=5)

        InfoLabel = TK.Label(PasekDolny)
        InfoLabel.config(text = Nazwa + ' ' + Wersja + ' | © ' + Autorzy + ' ' + LataPracy + ' dla ZSP Sobolew')
        InfoLabel.config(width = 107)
        InfoLabel.config(justify = 'left')
        InfoLabel.config(anchor='w')
        InfoLabel.config(bg = M_tytultlo)
        InfoLabel.config(fg = M_tytultext)
        InfoLabel.grid(row = 0, column = 0)

        def InfoOpen():
            try:
                x = open('.\instruction.txt')
            except FileNotFoundError:
                MDdlg.err(4)
            else:
                OS.system("notepad .\instruction.txt")

        PrzyciskINFO = TK.Button(PasekDolny)
        PrzyciskINFO.config(text = 'Instrukcja')
        PrzyciskINFO.config(command = InfoOpen)
        PrzyciskINFO.config(bg = M_przycisktlo)
        PrzyciskINFO.config(fg = M_przycisktext)
        PrzyciskINFO.config(relief = 'flat')
        PrzyciskINFO.config(activebackground = M_przycisktlo)
        PrzyciskINFO.grid(row = 0, column = 1, padx = 5, pady = 5)

        PrzyciskUSTAWIENIA = TK.Button(PasekDolny)
        PrzyciskUSTAWIENIA.config(text = 'Ustawienia')
        PrzyciskUSTAWIENIA.config(command = self.settingsButton)
        PrzyciskUSTAWIENIA.config(bg = M_przycisktlo)
        PrzyciskUSTAWIENIA.config(fg = M_przycisktext)
        PrzyciskUSTAWIENIA.config(relief = 'flat')
        PrzyciskUSTAWIENIA.grid(row = 0, column = 2, padx = 5, pady = 5)

    def settingsButton(self):
        self.child = Settings(self)

    def run(self):
        self.mainloop()

# Okno ustawień
class Settings(TK.Toplevel):
    def __init__(self, parent):
        # Ustawienia okna
        TK.Toplevel.__init__(self, parent)
        self.title('Ustawienia')
        self.resizable(width = False, height = False)
        self.configure(bg = M_tlo)

        liczbawierszy = 0

        # Tytuł
        Tytul = TK.Label(self)
        Tytul.config(text = 'Ustawienia')
        Tytul.config(width = 40)
        Tytul.config(bg = M_tytultlo)
        Tytul.config(fg = M_tytultext)
        Tytul.config(font = ('Segoe UI Semilight', 20))
        Tytul.grid(row = 0)


        # Frame1 - Motyw
        liczbawierszy += 1
        Ramka1 = TK.LabelFrame(self)
        Ramka1.config(text = ' Motyw programu ')
        Ramka1.config(bg = M_tlo)
        Ramka1.config(fg = M_text)
        Ramka1.config(borderwidth = M_framewielkosc)
        Ramka1.grid(row = 1, pady = 5)


        if int(MDlcg.read()[0]) == 1:
            Motyw_list_set = 1
        else:
            Motyw_list_set = 0
        Motyw_list = TKttk.Combobox(Ramka1)
        Motyw_list.config(textvariable = TK.StringVar())
        Motyw_list.config(state = 'readonly')
        Motyw_list.config(width = 93)
        Motyw_list.grid(row = 0, pady = 5, padx = 5)
        Motyw_list['values'] = ('Jasny', 'Ciemny')
        Motyw_list.current(Motyw_list_set)


        # Frame2 - Kodowanie
        liczbawierszy += 1
        Ramka2 = TK.LabelFrame(self)
        Ramka2.config(text = ' Kodowanie wyjściowe ')
        Ramka2.config(bg = M_tlo)
        Ramka2.config(fg = M_text)
        Ramka2.config(borderwidth = M_framewielkosc)
        Ramka2.grid(row = 2, pady = 5)

        Code_list = TKttk.Combobox(Ramka2)
        Code_list.config(textvariable = TK.StringVar())
        Code_list.config(state = 'readonly')
        Code_list.config(width = 93)
        Code_list.grid(row = 0, pady = 5, padx = 5)
        Code_list['values'] = ('utf-8')
        Code_list.set(MDlcg.read()[1])


        # Frame3 - Format plików wejściowych
        SzerokoscPolaWej = 35
        WysokoscPolaWej = 8

        liczbawierszy += 1
        Ramka3 = TK.LabelFrame(self)
        Ramka3.config(text = ' Format plików wejściowych ')
        Ramka3.config(bg = M_tlo)
        Ramka3.config(fg = M_text)
        Ramka3.config(borderwidth = M_framewielkosc)
        Ramka3.grid(row = 3, pady = 5)

        UczniowieLabel = TK.Label(Ramka3)
        UczniowieLabel.config(text = 'Uczniowie')
        UczniowieLabel.config(justify = 'center')
        UczniowieLabel.config(bg = M_tlo)
        UczniowieLabel.config(fg = M_text)
        UczniowieLabel.grid(row = 0, column = 0)

        uczfmt = MDlfm.read()[0]
        uczfmt = '\n'.join(uczfmt)
        UczniowieFormat = TK.Text(Ramka3)
        UczniowieFormat.config(width = SzerokoscPolaWej)
        UczniowieFormat.config(height = WysokoscPolaWej)
        UczniowieFormat.config(bg = M_entrytlo)
        UczniowieFormat.config(fg = M_text)
        UczniowieFormat.grid(row = 1, column = 0, padx = 5, pady = 5)
        UczniowieFormat.insert(TK.END, uczfmt)

        NauczycieleLabel = TK.Label(Ramka3)
        NauczycieleLabel.config(text = 'Nauczyciele')
        NauczycieleLabel.config(justify = 'center')
        NauczycieleLabel.config(bg = M_tlo)
        NauczycieleLabel.config(fg = M_text)
        NauczycieleLabel.grid(row = 0, column = 1)

        nczfmt = MDlfm.read()[1]
        nczfmt = '\n'.join(nczfmt)
        NauczycieleFormat = TK.Text(Ramka3)
        NauczycieleFormat.config(width = SzerokoscPolaWej)
        NauczycieleFormat.config(height = WysokoscPolaWej)
        NauczycieleFormat.config(bg = M_entrytlo)
        NauczycieleFormat.config(fg = M_text)
        NauczycieleFormat.grid(row = 1, column = 1, padx = 5, pady = 5)
        NauczycieleFormat.insert(TK.END, nczfmt)

        OpisFmt = TK.LabelFrame(Ramka3)
        OpisFmt.config(bg=M_tlo)
        OpisFmt.config(fg=M_text)
        OpisFmt.config(borderwidth=0)
        OpisFmt.grid(row=2, pady=5, columnspan=4)

        Opis1 = TK.Label(OpisFmt)
        Opis1.config(text='Dozwolone znaki:')
        Opis1.config(bg=M_tlo)
        Opis1.config(fg=M_text)
        Opis1.grid(row=0, columnspan=7)

        Opis2_1 = TK.Label(OpisFmt)
        Opis2_1.config(text='K - Klasa')
        Opis2_1.config(bg=M_tlo)
        Opis2_1.config(fg=M_text)
        Opis2_1.grid(row=1, column=0)

        Opis2_2 = TK.Label(OpisFmt)
        Opis2_2.config(text='O - Oddzial')
        Opis2_2.config(bg=M_tlo)
        Opis2_2.config(fg=M_text)
        Opis2_2.grid(row=1, column=1)

        Opis2_3 = TK.Label(OpisFmt)
        Opis2_3.config(text='N - Nazwisko')
        Opis2_3.config(bg=M_tlo)
        Opis2_3.config(fg=M_text)
        Opis2_3.grid(row=1, column=2)

        Opis2_4 = TK.Label(OpisFmt)
        Opis2_4.config(text='I - Imię')
        Opis2_4.config(bg=M_tlo)
        Opis2_4.config(fg=M_text)
        Opis2_4.grid(row=1, column=3)

        Opis2_5 = TK.Label(OpisFmt)
        Opis2_5.config(text='L - Login')
        Opis2_5.config(bg=M_tlo)
        Opis2_5.config(fg=M_text)
        Opis2_5.grid(row=1, column=4)

        Opis2_6 = TK.Label(OpisFmt)
        Opis2_6.config(text = 'X - Dane nieznaczące')
        Opis2_6.config(bg = M_tlo)
        Opis2_6.config(fg = M_text)
        Opis2_6.grid(row = 1, column = 5)

        Opis2_6 = TK.Label(OpisFmt)
        Opis2_6.config(text='Q - Pusta linia')
        Opis2_6.config(bg=M_tlo)
        Opis2_6.config(fg=M_text)
        Opis2_6.grid(row=1, column=6)

        Opis3 = TK.Label(OpisFmt)
        Opis3.config(text='Pozostałe znaki oprócz cyfr i pozostałych liter')
        Opis3.config(bg=M_tlo)
        Opis3.config(fg=M_text)
        Opis3.grid(row=2, columnspan = 7)


        # Frame4 - Stałe
        liczbawierszy += 1
        Ramka4 = TK.LabelFrame(self)
        Ramka4.config(text = ' Ustawienia generowania ')
        Ramka4.config(bg = M_tlo)
        Ramka4.config(fg = M_text)
        Ramka4.config(borderwidth = M_framewielkosc)
        Ramka4.grid(row = 4, pady = 5)


        # Długość liceum i branżowej
        RamkaDl = TK.LabelFrame(Ramka4)
        RamkaDl.config(bg = M_tlo)
        RamkaDl.config(fg = M_text)
        RamkaDl.config(borderwidth = 0)
        RamkaDl.grid(row = 0, pady = 5, columnspan = 2)

        DlLicLabel = TK.Label(RamkaDl)
        DlLicLabel.config(text = 'Lata nauki w liceum')
        DlLicLabel.config(width = SzerokoscOpisu + 5)
        DlLicLabel.config(bg = M_tlo)
        DlLicLabel.config(fg = M_text)
        DlLicLabel.grid(row = 0, column = 0)

        DlLicValue = TK.IntVar()
        DlLicPole = TK.Spinbox(RamkaDl)
        DlLicPole.config(textvariable = DlLicValue)
        DlLicPole.config(from_ = 1, to = 10)
        DlLicPole.config(width = 18)
        DlLicPole.config(bg = M_entrytlo)
        DlLicPole.config(fg = M_text)
        DlLicPole.grid(row = 0, column = 1, padx = 5, pady = 5)
        DlLicPole.delete(0, 'end')
        DlLicPole.insert(0, int(MDlcg.read()[5]))

        DlBrLabel = TK.Label(RamkaDl)
        DlBrLabel.config(text='Lata nauki w branżowej')
        DlBrLabel.config(width = SzerokoscOpisu + 5)
        DlBrLabel.config(bg = M_tlo)
        DlBrLabel.config(fg = M_text)
        DlBrLabel.grid(row = 0, column = 2)

        DlBrValue = TK.IntVar()
        DlBrPole = TK.Spinbox(RamkaDl)
        DlBrPole.config(textvariable = DlBrValue)
        DlBrPole.config(from_ = 1, to=10)
        DlBrPole.config(width = 18)
        DlBrPole.config(bg = M_entrytlo)
        DlBrPole.config(fg = M_text)
        DlBrPole.grid(row = 0, column = 3, padx = 5, pady = 5)
        DlBrPole.delete(0, 'end')
        DlBrPole.insert(0, int(MDlcg.read()[6]))


        # Domena

        DomenaLabel = TK.Label(Ramka4)
        DomenaLabel.config(text = 'Domena')
        DomenaLabel.config(width = SzerokoscOpisu + 5)
        DomenaLabel.config(bg = M_tlo)
        DomenaLabel.config(fg = M_text)
        DomenaLabel.grid(row = 2, column = 0)

        text1 = TK.StringVar()
        PoleDomena = TK.Entry(Ramka4)
        PoleDomena.config(textvariable = text1)
        PoleDomena.config(width = 69)
        PoleDomena.config(bg = M_entrytlo)
        PoleDomena.config(fg = M_text)
        PoleDomena.grid(row = 2, column = 1, padx = 5, pady = 5)
        PoleDomena.insert(0, MDlcg.read()[2])


        # Quota

        QuotaLabel = TK.Label(Ramka4)
        QuotaLabel.config(text = 'Quota (MB)')
        QuotaLabel.config(width = SzerokoscOpisu)
        QuotaLabel.config(bg = M_tlo)
        QuotaLabel.config(fg = M_text)
        QuotaLabel.grid(row = 3, column = 0)

        value2 = TK.IntVar()
        PoleQuota = TK.Spinbox(Ramka4)
        PoleQuota.config(textvariable = value2)
        PoleQuota.config(from_ = 1, to = 100000)
        PoleQuota.config(width = 67)
        PoleQuota.config(bg = M_entrytlo)
        PoleQuota.config(fg = M_text)
        PoleQuota.grid(row = 3, column = 1, padx = 5, pady = 5)
        PoleQuota.delete(0, 'end')
        PoleQuota.insert(0, int(MDlcg.read()[3]))


        # Kraj

        KrajLabel = TK.Label(Ramka4)
        KrajLabel.config(text = 'Kraj')
        KrajLabel.config(width = SzerokoscOpisu + 5)
        KrajLabel.config(bg = M_tlo)
        KrajLabel.config(fg = M_text)
        KrajLabel.grid(row = 4, column = 0)

        KrajValue = TK.StringVar()
        KrajPole = TK.Entry(Ramka4)
        KrajPole.config(textvariable = KrajValue)
        KrajPole.config(width = 69)
        KrajPole.config(bg = M_entrytlo)
        KrajPole.config(fg = M_text)
        KrajPole.grid(row = 4, column = 1, padx = 5, pady = 5)
        KrajPole.insert(0, MDlcg.read()[4])


        # Przycisk ZAPISZ
        def save():
            if MDdlg.ask(1):
                motyw = Motyw_list.get()
                if motyw == 'Jasny':
                    motyw = '0'
                else:
                    motyw = '1'
                kodowanie = Code_list.get()
                uczniowiefmt = UczniowieFormat.get('1.0', 'end')
                nauczycielefmt = NauczycieleFormat.get('1.0', 'end')
                liclata = DlLicPole.get()
                brlata = DlBrPole.get()
                domena = PoleDomena.get()
                quota = PoleQuota.get()
                kraj = KrajPole.get()
                SettingsToSave = [motyw, kodowanie, domena, quota, kraj, liclata, brlata]
                FormatToSave = [uczniowiefmt, nauczycielefmt]
                if MDlfm.edit(FormatToSave):
                    MDlcg.edit(SettingsToSave)
                    MDdlg.inf(0)
                    self.destroy()
                else:
                    pass
        PrzyciskZAPISZ = TK.Button(self)
        PrzyciskZAPISZ.config(text = 'ZAPISZ')
        PrzyciskZAPISZ.config(command = save)
        PrzyciskZAPISZ.config(width = 50)
        PrzyciskZAPISZ.config(bg = M_przycisktlo)
        PrzyciskZAPISZ.config(fg = M_przycisktext)
        PrzyciskZAPISZ.config(relief = 'flat')
        PrzyciskZAPISZ.config(activebackground = M_przycisktlo)
        PrzyciskZAPISZ.grid(row = liczbawierszy + 1, pady = 15)



# Inicjacja okna głównego
OknoGlowne = Main()
OknoGlowne.run()