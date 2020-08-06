"""
# GeneratorCSV
# Wersja 4.0: UC 1
# by Mateusz Skoczek
# luty 2019 - grudzień 2019
# dla ZSP Sobolew

#
# Główny plik składowy programu
#
"""








# ----------------------------------------- # Definicja kodów dialogowych # ------------------------------------------ #

E000x01 = "Brak modułu wywołującego okna dialogowe ('dialog.py').\nPrzywróć plik. (E000x01)"
E000x02 = ["Brak modułu zarządzającego plikiem konfiguracyjnym ('load_config.py').\nPrzywróć plik. (E000x02)", True]








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

# Biblioteki zewnętrzne interfejsu graficznego
from tkinter import filedialog as TKfld
import tkinter as TK









# ------------------------------------- # Uruchomienie interfejsu graficznego # -------------------------------------- #

# Informacje o programie
Nazwa = 'GeneratorCSV'
Wersja = '4.0' #Todo wersja

# Zmienne globalne środowiska graficznego

CiemnyMotyw =
SzerokoscOpisu = 17
SzerokoscPola = 91

def settings():
    SettingsWindow = TK.Tk()
    SettingsWindow.title('ustawienia')
    SettingsWindow.mainloop()

def main():
    # Tworzenie okna głównego
    MainWindow = TK.Tk()
    MainWindow.title(Nazwa + ' ' + Wersja)
    MainWindow.resizable(width = False, height = False)

    Tytul = TK.Label(MainWindow, text='GeneratorCSV', font=('Segoe UI Semilight', 20), borderwidth=7, justify='center',
                     bg='Gainsboro', width=47)
    Tytul.grid(row=0)

    MainWindow.mainloop()
main()

"""
def gui():
    # Tworzenie okna
    OknoGlowne = TK.Tk()
    OknoGlowne.title('GeneratorCSV')
    OknoGlowne.resizable(width=False, height=False)

    # Nazwa programu


    # Tworzenie frame dla ścieżek plików do importu
    Ramka1 = TK.LabelFrame(OknoGlowne, text='Pliki do importu zawierające dane')
    Ramka1.grid(row=1)

    # Ścieżka pliku do importu 1
    wiersz1 = 0
    text1 = TK.StringVar()
    OpisPola1 = TK.Label(Ramka1, text='Plik z danymi (1)', justify='left', width=SzerokoscOpisu)
    OpisPola1.grid(row=wiersz1, column=0)
    Pole1 = TK.Entry(Ramka1, textvariable=text1, width=SzerokoscPola)
    Pole1.grid(row=wiersz1, column=1)

    def Browse1_Dialog():
        Browse1.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik",
                                                 filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole1.delete(0, 'end')
        Pole1.insert(0, Browse1.filename)

    Browse1 = TK.Button(Ramka1, text='...', command=Browse1_Dialog, background='silver', relief='flat')
    Browse1.grid(row=wiersz1, column=2, padx=5, pady=3)

    # Ścieżka pliku do importu 2
    wiersz2 = 1
    text2 = TK.StringVar()
    OpisPola2 = TK.Label(Ramka1, text='Plik z danymi (2)', justify='left', width=SzerokoscOpisu)
    OpisPola2.grid(row=wiersz2, column=0)
    Pole2 = TK.Entry(Ramka1, textvariable=text2, width=SzerokoscPola)
    Pole2.grid(row=wiersz2, column=1)

    def Browse2_Dialog():
        Browse2.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik",
                                                 filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole2.delete(0, 'end')
        Pole2.insert(0, Browse2.filename)

    Browse2 = TK.Button(Ramka1, text='...', command=Browse2_Dialog, background='silver', relief='flat')
    Browse2.grid(row=wiersz2, column=2, padx=5, pady=3)

    # Ścieżka pliku do importu 3
    wiersz3 = 2
    text3 = TK.StringVar()
    OpisPola3 = TK.Label(Ramka1, text='Plik z danymi (3)', justify='left', width=SzerokoscOpisu)
    OpisPola3.grid(row=wiersz3, column=0)
    Pole3 = TK.Entry(Ramka1, textvariable=text3, width=SzerokoscPola)
    Pole3.grid(row=wiersz3, column=1)

    def Browse3_Dialog():
        Browse3.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik",
                                                 filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole3.delete(0, 'end')
        Pole3.insert(0, Browse3.filename)

    Browse3 = TK.Button(Ramka1, text='...', command=Browse3_Dialog, background='silver', relief='flat')
    Browse3.grid(row=wiersz3, column=2, padx=5, pady=3)

    # Ścieżka pliku do importu 4
    wiersz4 = 3
    text4 = TK.StringVar()
    OpisPola4 = TK.Label(Ramka1, text='Plik z danymi (4)', justify='left', width=SzerokoscOpisu)
    OpisPola4.grid(row=wiersz4, column=0)
    Pole4 = TK.Entry(Ramka1, textvariable=text3, width=SzerokoscPola)
    Pole4.grid(row=wiersz4, column=1)

    def Browse4_Dialog():
        Browse4.filename = TKfld.askopenfilename(initialdir="/", title="Wybierz plik",
                                                 filetypes=(("Pliki txt", "*.txt"), ("Wszystkie pliki", "*.*")))
        Pole4.delete(0, 'end')
        Pole4.insert(0, Browse4.filename)

    Browse4 = TK.Button(Ramka1, text='...', command=Browse4_Dialog, background='silver', relief='flat')
    Browse4.grid(row=wiersz4, column=2, padx=5, pady=3)

    # Tworzenie frame dla plików export
    Ramka2 = TK.LabelFrame(OknoGlowne, text='Ustawienia eksportu')
    Ramka2.grid(row=2)

    # Ścieżka folderu do zapisu wygenerowanych plików
    text4 = TK.StringVar()
    OpisPolaExport = TK.Label(Ramka2, text='Lokalizacja', justify='left', width=SzerokoscOpisu)
    OpisPolaExport.grid(row=0, column=0)
    PoleExport = TK.Entry(Ramka2, textvariable=text4, width=SzerokoscPola)
    PoleExport.grid(row=0, column=1)

    def BrowseExport_Dialog():
        BrowseExport.filename = TKfld.askdirectory()
        PoleExport.delete(0, 'end')
        PoleExport.insert(0, BrowseExport.filename)

    BrowseExport = TK.Button(Ramka2, text='...', command=BrowseExport_Dialog, background='silver', relief='flat')
    BrowseExport.grid(row=0, column=2, padx=5, pady=3)

    # Przycisk START
    Przycisk = TK.Button(OknoGlowne, text='START', justify='center', width=50, relief='flat', background='silver')
    command=Main
    Przycisk.grid(row=3, pady=15)

    # Pasek dolny
    PasekDolny = TK.LabelFrame(OknoGlowne, bd=0, background='Gainsboro')
    PasekDolny.grid(row=4)
    InfoLabel = TK.Label(PasekDolny, text='GeneratorCSV 3.0 | © Mateusz Skoczek 2019 dla ZSP Sobolew', justify='left',
                         width=93, anchor='w', background='Gainsboro')
    InfoLabel.grid(row=0, column=0)

    def InfoOpen():
        try:
            x = open('instrukcja.txt')
        except FileNotFoundError:
            DG.err(E001x03)
        else:
            OS.system("notepad instrukcja.txt")

    Przycisk = TK.Button(PasekDolny, text='Instrukcja', justify='center', foreground='blue', relief='flat',
                         command=InfoOpen, background='Gainsboro')
    Przycisk.grid(row=0, column=1)

    TK.mainloop()

gui()
"""
