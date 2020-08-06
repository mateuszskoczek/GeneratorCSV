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

# Wewnętrzna funkcja sprawdzająca błędy pliku formatu
def CheckFormat(format):
    uczniowiefmt = ''
    for x in format[0]:
        uczniowiefmt += x

    try:
        if format[0].count('') > 0:
            error = int('x')
    except ValueError:
        MDdlg.err(11)

    try:
        if uczniowiefmt.count('K') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(6)

    try:
        if uczniowiefmt.count('O') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(7)

    try:
        if uczniowiefmt.count('N') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(8)

    try:
        if uczniowiefmt.count('I') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(9)

    try:
        if uczniowiefmt.count('L') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(10)

    try:
        if format[1].count('') > 0:
            error = int('x')
    except ValueError:
        MDdlg.err(12)

    nauczycielefmt = ''
    for x in format[1]:
        nauczycielefmt += x

    try:
        if nauczycielefmt.count('N') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(13)

    try:
        if nauczycielefmt.count('I') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(14)

    try:
        if nauczycielefmt.count('L') != 1:
            error = int('x')
    except ValueError:
        MDdlg.err(15)

    NiedozwoloneZnaki = ['1','2','3','4','5','6','7','8','9','0','W','E','R','T','Y','U','P','A','S','D','F','G','H','J','Z','C','V','B','M']
    try:
        for x in NiedozwoloneZnaki:
            if x in nauczycielefmt+uczniowiefmt:
                error = int('x')
    except ValueError:
        MDdlg.err(16)



# Odczytywanie ustawień z pliku formatu
def read():
    try:
        check = open(r'.\format.fmt')
    except FileNotFoundError:
        MDdlg.err(5)
    else:
        with open(r'.\format.fmt', 'r') as fmt:
            fmt = fmt.read().split('\n<separator>\n')
            format = []
            for x in fmt:
                format.append(x.split('\n'))
            CheckFormat(format)
            return format



# Zapis ustawień do pliku formatu
def edit(format):
    CheckFormat(format)
    try:
        check = open(r'.\format.fmt')
    except FileNotFoundError:
        MDdlg.err(5)
    else:
        FormatToSaveX = []
        for x in format:
            FormatToSaveX.append('\n'.join(x))
        FormatToSave = FormatToSaveX[0] + '\n<separator>\n' + FormatToSaveX[1]
        with open(r'.\format.fmt', 'w') as fmt:
            fmt.write(FormatToSave)