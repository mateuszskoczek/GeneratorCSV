"""
# GeneratorCSV
# Wersja 4.0 Experimental
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Główny plik składowy programu
#
"""





# -------------------------------------------- # Informacje o programie # -------------------------------------------- #

Nazwa = 'GeneratorCSV'
Wersja = '4.0 Experimental'








# ----------------------------------------- # Definicja kodów dialogowych # ------------------------------------------ #

E000x01 = "Brak modułu wywołującego okna dialogowe ('dialog.py').\nPrzywróć plik. (E000x01)"
E000x02 = ["Brak modułu zarządzającego plikiem konfiguracyjnym ('load_config.py').\nPrzywróć plik. (E000x02)", True]
E001x01 = ["Brak pliku formatu 'format.py'.\nPrzywróć plik. (E001x01)", True]
E001x02 = ["Brak pliku instrukcji ('instruction.txt').\nPrzywróć plik. (E001x02)", False]
E003x01 = ["Nie podano lokalizacji plików do importu. (E003x01)", False]
E003x02 = ["Nie podano lokalizacji zapisu wygenerowanych plików. (E003x02)", False]

E003x111 = ["Plik podany w sciezce 1 nie istnieje (E003x111)", False]
E003x112 = ["Plik podany w sciezce 2 nie istnieje (E003x112)", False]
E003x113 = ["Plik podany w sciezce 3 nie istnieje (E003x113)", False]
E003x114 = ["Plik podany w sciezce 4 nie istnieje (E003x114)", False]

A001 = "Czy na pewno chcesz rozpocząć generowanie?\nProgram utworzy w podanej lokalizacji pliki 'email.csv' i 'office.csv'.\nJeżeli w podanej lokalizacji istnieją pliki o takich nazwach zostaną one nadpisane."








# ----------------------------------- # Import bibliotek zewnętrznych i modułów # ------------------------------------ #

# Biblioteki zewnętrzne
import os as OS
import sys as SS



# Moduły składowe programu
try:
    import dialog as MDdlg
except ModuleNotFoundError:
    print('Nieoczekiwany wyjatek - nie mozna wygenerowac okna dialogowego bledu\n\nBŁĄD KRYTYCZNY!\n%s') %E000x01
    wait = input('Naciśnij ENTER aby zakończyć')
    SS.exit(0)

try:
    import load_config as MDlcg
except ModuleNotFoundError:
    MDdlg.Err(E000x02)

try:
    import format as MDfmt
except ModuleNotFoundError:
    MDdlg.Err(E000x02)

try:
    import processing as MDprc
except ModuleNotFoundError:
    MDdlg.Err(E000x02)


# Biblioteki zewnętrzne interfejsu graficznego
from tkinter import filedialog as TKfld
from tkinter import ttk as TKttk
import tkinter as TK









# ------------------------------------- # Uruchomienie interfejsu graficznego # -------------------------------------- #

# Zmienne globalne środowiska graficznego
if int(MDlcg.read()[0]) == 1:
    CiemnyMotyw = True
else:
    CiemnyMotyw = False
SzerokoscOpisu = 17
SzerokoscPola = 122



# Kolorystyka okna
if CiemnyMotyw:
    PaletaBarw = ['#1F1F1F', '#191919', '#B8B8B8', '#FFFFFF', '#404040', '#FFFFFF', '#1F1F1F', 1]
else:
    PaletaBarw = ['#F0F0F0', '#D4D4D4', '#000000', '#000000', '#A6A6A6', '#000000', '#FFFFFF', 2]

B_tlo = PaletaBarw[0]
B_tytultlo = PaletaBarw[1]
B_tytultext = PaletaBarw[2]
B_text = PaletaBarw[3]
B_przycisktlo = PaletaBarw[4]
B_przycisktext = PaletaBarw[5]
B_entrytlo = PaletaBarw[6]
B_framewielkosc = PaletaBarw[7]




def settings():
    # Tworzenie okna ustawień
    SettingsWindow = TK.Tk()
    SettingsWindow.title('Ustawienia programu')
    SettingsWindow.resizable(width = False, height = False)
    SettingsWindow.configure(background = B_tlo)


    # Tytul
    Tytul = TK.Label(SettingsWindow)
    Tytul.config(text = 'Ustawienia')
    Tytul.config(width = 20)
    Tytul.config(bg = B_tytultlo, fg = B_tytultext)
    Tytul.config(font = ('Segoe UI Semilight', 20))
    Tytul.grid(row = 0)


    # Frame1 - Motyw
    Ramka1 = TK.LabelFrame(SettingsWindow)
    Ramka1.config(text = ' Motyw programu ')
    Ramka1.config(bg = B_tlo, fg = B_text)
    Ramka1.config(borderwidth = B_framewielkosc)
    Ramka1.grid(row = 1, pady = 5)

    Motyw_var = TK.StringVar()
    if int(MDlcg.read()[0]) == 1:
        Motyw_var.set('Ciemny')
        Motyw_index = 1
    else:
        Motyw_var.set('Jasny')
        Motyw_index = 0

    Motyw_list = TKttk.Combobox(Ramka1)
    Motyw_list.config(textvariable = Motyw_var, state = 'readonly')
    Motyw_list.config(width = 43)
    Motyw_list.grid(row = 0, pady = 5, padx = 5)
    Motyw_list['values'] = ('Jasny', 'Ciemny')
    Motyw_list.current(Motyw_index)


    # Frame2 - Kodowanie
    Ramka2 = TK.LabelFrame(SettingsWindow)
    Ramka2.config(text = ' Kodowanie wyjściowe ')
    Ramka2.config(bg = B_tlo, fg = B_text)
    Ramka2.config(borderwidth = B_framewielkosc)
    Ramka2.grid(row = 2, pady = 5)

    Code_var = TK.StringVar()
    Code_var.set(MDlcg.read()[1])

    Code_list = TKttk.Combobox(Ramka2)
    Code_list.config(textvariable = Code_var, state = 'readonly')
    Code_list.config(width = 43)
    Code_list.grid(row = 0, pady = 5, padx = 5)
    Code_list['values'] = ('utf-8')
    Code_list.set(MDlcg.read()[1])


    # Przycisk ZAPISZ
    def zapis():
        X1 = Motyw_list.get()
        if X1 == 'Jasny':
            X1 = '0'
        else:
            X1 = '1'
        X2 = Code_list.get()
        ToSave = [X1, X2]
        MDlcg.edit(ToSave)
        SettingsWindow.destroy()
    PrzyciskZAPISZ = TK.Button(SettingsWindow)
    PrzyciskZAPISZ.config(text = 'ZAPISZ')
    PrzyciskZAPISZ.config(command = zapis)
    PrzyciskZAPISZ.config(width = 40)
    PrzyciskZAPISZ.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat', activebackground = B_przycisktlo)
    PrzyciskZAPISZ.grid(row = 3, pady = 8)


    SettingsWindow.mainloop()




def main():
    # Tworzenie okna głównego
    MainWindow = TK.Tk()
    MainWindow.title(Nazwa + ' ' + Wersja)
    MainWindow.resizable(width = False, height = False)
    MainWindow.configure(background = B_tlo)


    # Tytul
    Tytul = TK.Label(MainWindow)
    Tytul.config(text = Nazwa)
    Tytul.config(width = 41)
    Tytul.config(bg = B_tytultlo, fg = B_tytultext)
    Tytul.config(font = ('Segoe UI Semilight', 30))
    Tytul.grid(row = 0)


    # Frame1 - Import
    Ramka1 = TK.LabelFrame(MainWindow)
    Ramka1.config(text = ' Pliki do importu zawierające dane ')
    Ramka1.config(bg = B_tlo, fg = B_text)
    Ramka1.config(borderwidth = B_framewielkosc)
    Ramka1.grid(row = 1)


    # Ścieżka pliku do importu 1
    wiersz = 1
    text1 = TK.StringVar()

    OpisPola1 = TK.Label(Ramka1)
    OpisPola1.config(text = 'Plik z danymi (1)')
    OpisPola1.config(width = SzerokoscOpisu)
    OpisPola1.config(bg = B_tlo, fg = B_text)
    OpisPola1.grid(row = wiersz, column = 0)

    Pole1 = TK.Entry(Ramka1)
    Pole1.config(textvariable = text1)
    Pole1.config(width = SzerokoscPola)
    Pole1.config(bg = B_entrytlo, fg = B_text)
    Pole1.grid(row = wiersz, column = 1)

    def Browse1_Dialog():
        Browse1.filename = TKfld.askopenfilename(initialdir = "/", title = "Wybierz plik do importu", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole1.delete(0, 'end')
        Pole1.insert(0, Browse1.filename)

    Browse1 = TK.Button(Ramka1)
    Browse1.config(text = '...')
    Browse1.config(command = Browse1_Dialog)
    Browse1.config(bg = B_przycisktlo, fg = B_przycisktext, relief='flat', activebackground = B_przycisktlo)
    Browse1.grid(row = wiersz, column = 2, padx=5, pady=3)


    # Ścieżka pliku do importu 2
    wiersz = 2
    text2 = TK.StringVar()

    OpisPola2 = TK.Label(Ramka1)
    OpisPola2.config(text = 'Plik z danymi (2)')
    OpisPola2.config(width = SzerokoscOpisu)
    OpisPola2.config(bg = B_tlo, fg = B_text)
    OpisPola2.grid(row = wiersz, column = 0)

    Pole2 = TK.Entry(Ramka1)
    Pole2.config(textvariable = text2)
    Pole2.config(width = SzerokoscPola)
    Pole2.config(bg = B_entrytlo, fg = B_text)
    Pole2.grid(row = wiersz, column = 1)

    def Browse2_Dialog():
        Browse2.filename = TKfld.askopenfilename(initialdir = "/", title = "Wybierz plik do importu", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole2.delete(0, 'end')
        Pole2.insert(0, Browse2.filename)

    Browse2 = TK.Button(Ramka1)
    Browse2.config(text = '...')
    Browse2.config(command = Browse1_Dialog)
    Browse2.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat', activebackground = B_przycisktlo)
    Browse2.grid(row = wiersz, column = 2, padx = 5, pady = 3)


    # Ścieżka pliku do importu 3
    wiersz = 3
    text3 = TK.StringVar()

    OpisPola3 = TK.Label(Ramka1)
    OpisPola3.config(text = 'Plik z danymi (3)')
    OpisPola3.config(width = SzerokoscOpisu)
    OpisPola3.config(bg = B_tlo, fg = B_text)
    OpisPola3.grid(row = wiersz, column = 0)

    Pole3 = TK.Entry(Ramka1)
    Pole3.config(textvariable = text3)
    Pole3.config(width = SzerokoscPola)
    Pole3.config(bg = B_entrytlo, fg = B_text)
    Pole3.grid(row = wiersz, column = 1)

    def Browse3_Dialog():
        Browse3.filename = TKfld.askopenfilename(initialdir = "/", title = "Wybierz plik do importu", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole3.delete(0, 'end')
        Pole3.insert(0, Browse3.filename)

    Browse3 = TK.Button(Ramka1)
    Browse3.config(text = '...')
    Browse3.config(command = Browse1_Dialog)
    Browse3.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat', activebackground = B_przycisktlo)
    Browse3.grid(row = wiersz, column = 2, padx = 5, pady = 3)


    # Ścieżka pliku do importu 4
    wiersz = 4
    text4 = TK.StringVar()

    OpisPola4 = TK.Label(Ramka1)
    OpisPola4.config(text = 'Plik z danymi (4)')
    OpisPola4.config(width = SzerokoscOpisu)
    OpisPola4.config(bg = B_tlo, fg = B_text)
    OpisPola4.grid(row = wiersz, column = 0)

    Pole4 = TK.Entry(Ramka1)
    Pole4.config(textvariable = text4)
    Pole4.config(width = SzerokoscPola)
    Pole4.config(bg = B_entrytlo, fg = B_text)
    Pole4.grid(row = wiersz, column = 1)

    def Browse4_Dialog():
        Browse4.filename = TKfld.askopenfilename(initialdir = "/", title = "Wybierz plik do importu", filetypes = (("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole4.delete(0, 'end')
        Pole4.insert(0, Browse4.filename)

    Browse4 = TK.Button(Ramka1)
    Browse4.config(text = '...')
    Browse4.config(command = Browse1_Dialog)
    Browse4.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat', activebackground = B_przycisktlo)
    Browse4.grid(row = wiersz, column = 2, padx = 5, pady = 3)


    # Frame2 - Eksport
    Ramka2 = TK.LabelFrame(MainWindow)
    Ramka2.config(text = ' Ustawienia eksportu ')
    Ramka2.config(bg = B_tlo, fg = B_text)
    Ramka2.config(borderwidth = B_framewielkosc)
    Ramka2.grid(row = 2)

    # Ścieżka folderu do zapisu wygenerowanych plików
    textExport = TK.StringVar()

    OpisPolaExport = TK.Label(Ramka2)
    OpisPolaExport.config(text = 'Lokalizacja')
    OpisPolaExport.config(width = SzerokoscOpisu)
    OpisPolaExport.config(bg = B_tlo, fg = B_text, relief = 'flat', activebackground = B_przycisktlo)
    OpisPolaExport.grid(row=0, column=0)

    PoleExport = TK.Entry(Ramka2)
    PoleExport.config(textvariable = textExport)
    PoleExport.config(width = SzerokoscPola)
    PoleExport.config(bg = B_entrytlo, fg = B_text)
    PoleExport.grid(row=0, column=1)

    def BrowseExport_Dialog():
        BrowseExport.filename = TKfld.askdirectory()
        PoleExport.delete(0, 'end')
        PoleExport.insert(0, BrowseExport.filename)

    BrowseExport = TK.Button(Ramka2)
    BrowseExport.config(text='...')
    BrowseExport.config(command=BrowseExport_Dialog)
    BrowseExport.config(bg = B_przycisktlo, fg = B_przycisktext, relief='flat', activebackground = B_przycisktlo)
    BrowseExport.grid(row=0, column=2, padx=5, pady=3)


    # Przycisk START
    def PathPreprocess():
        if MDdlg.Ask(A001):
            while True:
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
                    MDdlg.Err(E003x01)
                    break
                if sciezkaExport_puste:
                    MDdlg.Err(E003x02)
                    break
                KontenerDanych = []
                if not sciezka1_puste:
                    try:
                        x = open(sciezka1)
                    except FileNotFoundError:
                        MDdlg.Err(E003x111)
                    else:
                        with open(sciezka1, 'r') as plik1:
                            KontenerDanych += MDfmt.przetworz(plik1.read())
                if not sciezka2_puste:
                    try:
                        x = open(sciezka2)
                    except FileNotFoundError:
                        MDdlg.Err(E003x112)
                    else:
                        with open(sciezka2, 'r') as plik2:
                            KontenerDanych += MDfmt.przetworz(plik2.read())
                if not sciezka3_puste:
                    try:
                        x = open(sciezka3)
                    except FileNotFoundError:
                        MDdlg.Err(E003x113)
                    else:
                        with open(sciezka3, 'r') as plik3:
                            KontenerDanych += MDfmt.przetworz(plik3.read())
                if not sciezka4_puste:
                    try:
                        x = open(sciezka4)
                    except FileNotFoundError:
                        MDdlg.Err(E003x114)
                    else:
                        with open(sciezka4, 'r') as plik4:
                            KontenerDanych += MDfmt.przetworz(plik4.read())
                break
            MDprc.do(KontenerDanych, sciezkaExport)
        else:
            pass

    PrzyciskSTART = TK.Button(MainWindow)
    PrzyciskSTART.config(text = 'START')
    PrzyciskSTART.config(command = PathPreprocess)
    PrzyciskSTART.config(width = 50)
    PrzyciskSTART.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat', activebackground = B_przycisktlo)
    PrzyciskSTART.grid(row = 3, pady = 15)


    # Pasek dolny
    PasekDolny = TK.LabelFrame(MainWindow)
    PasekDolny.config(bd = 0, bg = B_tytultlo, fg = B_tytultext)
    PasekDolny.grid(row = 4)

    InfoLabel = TK.Label(PasekDolny)
    InfoLabel.config(text = 'GeneratorCSV 3.0 | © Mateusz Skoczek 2019 dla ZSP Sobolew')
    InfoLabel.config(justify = 'left', anchor='w', width=107)
    InfoLabel.config(bg = B_tytultlo, fg = B_tytultext)
    InfoLabel.grid(row=0, column=0)

    def InfoOpen():
        try:
            x = open('instrukcja.txt')
        except FileNotFoundError:
            MDdlg.Err(E001x02)
        else:
            OS.system("notepad instrukcja.txt")

    PrzyciskINFO = TK.Button(PasekDolny)
    PrzyciskINFO.config(text = 'Instrukcja')
    PrzyciskINFO.config(command = InfoOpen)
    PrzyciskINFO.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat', activebackground = B_przycisktlo)
    PrzyciskINFO.grid(row = 0, column = 1, padx = 5, pady = 5)

    PrzyciskUSTAWIENIA = TK.Button(PasekDolny)
    PrzyciskUSTAWIENIA.config(text = 'Ustawienia')
    PrzyciskUSTAWIENIA.config(command = settings)
    PrzyciskUSTAWIENIA.config(bg = B_przycisktlo, fg = B_przycisktext, relief = 'flat')
    PrzyciskUSTAWIENIA.grid(row = 0, column = 2, padx = 5, pady = 5)

    MainWindow.mainloop()

main()