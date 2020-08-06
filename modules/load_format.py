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








# --------------------------------------------------- # Funkcje # ---------------------------------------------------- #

# Wewnętrzna funkcja sprawdzająca błędy pliku formatu
def CheckFormat(Read, format):
    poprawne = True
    check = True
    while check:
        uczniowiefmt = ''
        for x in format[0]:
            uczniowiefmt += x

        try:
            if format[0].count('') > 0:
                error = int('x')
        except ValueError:
            MDdlg.err(11)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if uczniowiefmt.count('K') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(6)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if uczniowiefmt.count('O') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(7)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if uczniowiefmt.count('N') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(8)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if uczniowiefmt.count('I') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(9)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if uczniowiefmt.count('L') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(10)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if format[1].count('') > 0:
                error = int('x')
        except ValueError:
            MDdlg.err(12)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        nauczycielefmt = ''
        for x in format[1]:
            nauczycielefmt += x

        try:
            if nauczycielefmt.count('N') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(13)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if nauczycielefmt.count('I') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(14)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        try:
            if nauczycielefmt.count('L') != 1:
                error = int('x')
        except ValueError:
            MDdlg.err(15)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break

        NiedozwoloneZnaki = ['1','2','3','4','5','6','7','8','9','0','W','E','R','T','Y','U','P','A','S','D','F','G','H','J','Z','C','V','B','M']
        try:
            for x in NiedozwoloneZnaki:
                if x in nauczycielefmt+uczniowiefmt:
                    error = int('x')
        except ValueError:
            MDdlg.err(16)
            if Read:
                SS.exit(0)
            else:
                poprawne = False
                break
        check = False
    return poprawne



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
            CheckFormat(True, format)
            return format



# Zapis ustawień do pliku formatu
def edit(format):
    xformat = []
    for x in format:
        xformat.append(x.split('\n')[:-1])
    if CheckFormat(False, xformat):
        try:
            check = open(r'.\format.fmt')
        except FileNotFoundError:
            MDdlg.err(5)
        else:
            FormatToSaveX = []
            for x in xformat:
                FormatToSaveX.append('\n'.join(x))
            FormatToSave = FormatToSaveX[0] + '\n<separator>\n' + FormatToSaveX[1]
            with open(r'.\format.fmt', 'w') as fmt:
                fmt.write(FormatToSave)
            return True
    else:
        return False
