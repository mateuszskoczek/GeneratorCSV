"""
# Generator CSV
# Wersja 4.0
# Autorzy: Mateusz Skoczek
# Styczeń 2019 - Czerwiec 2020
# dla ZSP Sobolew
"""





# ----------------------------------------- # Zmienne # ----------------------------------------- #

class VAR:
    # Informacje o programie
    programName = 'Generator CSV'
    programVersion = '4.0'
    programVersionStage = ''
    programVersionBuild = '20242'
    programCustomer = 'ZSP Sobolew'
    programAuthors = ['Mateusz Skoczek']
    programToW = ['styczeń', '2019', 'wrzesień', '2020']

    # Dozwolone kodowanie plików
    allowedCoding = ['utf-8', 'ANSI']

    # Dozwolone znaki
    allowedCharactersInSeparator = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=', '+', '[', ']', ' ', '?', '/', '>', '.', '<', ',', '"', "'", ':', ';', '|']





# --------------------------- # Import wbudowanych bibliotek Pythona # -------------------------- #


# Główne
import sys as SS
import os as OS
import time as TM
import codecs as CD
import pathlib as PT
import shutil as SU


# GUI
import tkinter as TK
from tkinter import ttk as TKttk
from tkinter import messagebox as TKmsb
from tkinter import filedialog as TKfld

from PIL import ImageTk as PLitk
from PIL import Image as PLimg





# ---------------------------------------- # Komunikaty # --------------------------------------- #


MSGlist = {
    'E0000' : 'none',
    'E0001' : 'Wystąpił błąd podczas inicjalizacji katalogu z plikami konfiguracyjnymi programu w katalogu %APPDATA%',
    'E0002' : 'Wystąpił błąd podczas ładowania pliku konfiguracyjnego (config.cfg)',
    'E0003' : 'Niepoprawne dane w pliku konfiguracyjnym (config.cfg)',
    'E0004' : 'Wystąpił błąd podczas ładowania pliku stylu (style.cfg)',
    'E0005' : 'Niepoprawne dane w pliku stylu (style.cfg)',
    'E0006' : 'Niepoprawne dane w pliku formatu',
    'A0001' : 'Czy chcesz zapisać? Zostanie utworzony nowy plik',
    'A0002' : 'Czy chcesz zapisać? Plik zostanie nadpisany',
    'A0003' : 'Czy chcesz rozpocząć przetwarzanie plików?',
    'A0004' : 'Czy chcesz zapisać?',
    'A0005' : 'Czy na pewno chcesz przywrócić domyślne ustawienia ogólne?',
    'A0006' : 'Czy na pewno chcesz przywrócić domyślne ustawienia wyglądu?',
    'A0007' : 'Czy na pewno chcesz usunąc zaznaczone format presety?',
    'E0007' : 'Wymagany przynajmniej jeden plik wejściowy',
    'E0008' : 'Nie można odnaleźć jednego z powyższych plików',
    'E0009' : 'Nie można odnaleźć jednego z powyższych format presetów',
    'E0010' : 'Nie można przetworzyć danych z plików wejściowych z pomocą podanych format presetów',
    'E0011' : 'Niepoprawne dane w plikach wejściowych',
    'E0012' : 'Nie można przetworzyć danych na format wyjściowy',
    'E0013' : 'Nie można utworzyć plików wejściowych',
    'E0014' : 'Nie można zapisać plików wejściowych',
    'I0001' : 'Operacja ukończona pomyślnie',
    'I0002' : 'Aplikacja zostanie zamknięta w celu przeładowania ustawień',
    'E0015' : 'Nie można usunąć wybranych format presetów',
    'E0016' : 'Nie można uruchomić pliku instrukcji (documentation/index.html)',
}

def MSG(code, terminate, *optionalInfo):
    try:
        optionalInfo[0]
    except:
        optionalInfo = ('', '')
    
    # Błędy
    if code[0] == 'E':
        TKmsb.showerror('Wystąpił błąd!', '%s\n%s' % (MSGlist[code], optionalInfo[0]))
        if terminate:
            SS.exit(0)
    
    # Informacja
    elif code[0] == 'I':
        TKmsb.showinfo('Informacja', '%s\n%s' % (MSGlist[code], optionalInfo[0]))
        if terminate:
            SS.exit(0)

    # Ostrzeżenie
    elif code[0] == 'W':
        TKmsb.showwarning('Ostrzeżenie', '%s\n%s' % (MSGlist[code], optionalInfo[0]))
        if terminate:
            SS.exit(0)
    
    # Zapytania
    elif code[0] == 'A':
        if TKmsb.askokcancel('Pytanie', '%s\n%s' % (MSGlist[code], optionalInfo[0])):
            return True
        else:
            return False





# ------------------------- # Sprawdzanie katalogu programu w APPDATA # ------------------------- #

appdata = PT.Path.home() / 'Appdata/Roaming'

#TODO
#SU.rmtree(str(appdata) + '/Generator CSV')
#TODO

def checkAppdata():
    if 'Generator CSV' not in [x for x in OS.listdir(appdata)]:
        try:
            OS.mkdir(str(appdata) + '/Generator CSV')
            SU.copy('configs/config.cfg', str(appdata) + '\Generator CSV\config.cfg')
            SU.copy('configs/style.cfg', str(appdata) + '\Generator CSV\style.cfg')
            OS.mkdir(str(appdata) + '/Generator CSV/format-presets')
        except Exception as exceptInfo:
            MSG('E0001', True, exceptInfo)
    else:
        if 'config.cfg' not in [x for x in OS.listdir(str(appdata) + '/Generator CSV')]:
            try:
                SU.copy('configs/config.cfg', str(appdata) + '\Generator CSV\config.cfg')
            except Exception as exceptInfo:
                MSG('E0001', True, exceptInfo)
        if 'style.cfg' not in [x for x in OS.listdir(str(appdata) + '/Generator CSV')]:
            try:
                SU.copy('configs/style.cfg', str(appdata) + '\Generator CSV\style.cfg')
            except Exception as exceptInfo:
                MSG('E0001', True, exceptInfo)
        if 'format-presets'not in [x for x in OS.listdir(str(appdata) + '/Generator CSV')]:
            try:
                OS.mkdir(str(appdata) + '/Generator CSV/format-presets')
            except Exception as exceptInfo:
                MSG('E0001', True, exceptInfo)
    
checkAppdata()





# ----------------------------- # Ładowanie pliku konfiguracyjnego # ---------------------------- #

class CFG:
    # Funkcje sprawdzające istnienie
    def __checkIfFileExist(self, write):
        if write:
            try:
                checkAppdata()
                file = open((str(appdata) + '\Generator CSV\config.cfg'), 'a')
            except Exception as exceptInfo:
                MSG('E0002', True, exceptInfo)
                return False
            else:
                if not file.writable():
                    MSG('E0002', False, 'Plik tylko do odczytu')
                    return False
                else:
                    return True
        else:
            try:
                checkAppdata()
                open(str(appdata) + '\Generator CSV\config.cfg')
            except Exception as exceptInfo:
                MSG('E0002', True, exceptInfo)

    def __checkIfRecordExist(self, content, record):
        if record in list(content.keys()):
            return [True]
        else:
            return [False, 'Brak danych - klucz: %s' % record]

    
    # Funkcje sprawdzające poprawność recordu
    def __checkI(self, write, record, var):
        if write:
            try:
                var = int(var)
            except:
                return (False, 'Niepoprawne dane - klucz: %s' % record)
            var = str(var)
        else:
            try:
                var = int(var)
            except:
                return (False, 'Niepoprawne dane - klucz: %s' % record)
        return [True, var]
    
    def __checkD(self, write, record, var):
        if write:
            varX = ''
            if var['D'] == None:
                varX += '*'
            else:
                try:
                    var['D'] = int(var['D'])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if int(var['s']) > 31 or int(var['s']) < 1:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                day = str(var['D'])
                if len(day) == 1:
                    day = '0' + day
                varX += day
            varX += '.'
            if var['M'] == None:
                varX += '*'
            else:
                try:
                    var['M'] = int(var['M'])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if int(var['s']) > 12 or int(var['s']) < 1:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                month = str(var['M'])
                if len(month) == 1:
                    month = '0' + month
                varX += month
            varX += '.'
            if var['Y'] == None:
                varX += '*'
            else:
                try:
                    var['Y'] = int(var['Y'])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if int(var['Y']) == 0:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                varX += str(var['Y'])
            varX += ' '
            if var['h'] == None:
                varX += '*'
            else:
                try:
                    var['h'] = int(var['h'])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if int(var['h']) > 23 or int(var['h']) < 1:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                hour = str(var['h'])
                if len(hour) == 1:
                    hour = '0' + hour
                varX += hour
            varX += ':'
            if var['m'] == None:
                varX += '*'
            else:
                try:
                    var['m'] = int(var['m'])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if int(var['m']) > 59 or int(var['m']) < 0:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                minute = str(var['m'])
                if len(minute) == 1:
                    minute = '0' + minute
                varX += minute
            varX += ':'
            if var['s'] == None:
                varX += '*'
            else:
                try:
                    var['s'] = int(var['s'])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if int(var['s']) > 59 or int(var['s']) < 0:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                seconds = str(var['s'])
                if len(seconds) == 1:
                    seconds = '0' + seconds
                varX += seconds
            var = varX
        else:
            varToReturn = {}
            var = var.split(' ')
            try:
                var[0] = var[0].split('.')
                var[1] = var[1].split(':')
                var = var[0] + var[1]
                dateLabels = ['D', 'M', 'Y', 'h', 'm', 's']
                if len(var) != len(dateLabels):
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                index = 0
                for x in var:
                    if x != '*':
                        try:
                            x = int(x)
                        except:
                            return (False, 'Niepoprawne dane - klucz: %s' % record)
                        varToReturn[dateLabels[index]] = int(x)
                    else:
                        varToReturn[dateLabels[index]] = None
                    index += 1
            except:
                return (False, 'Niepoprawne dane - klucz: %s' % record)
            var = varToReturn
        return [True, var]

    def __checkMSAs(self, write, record, var):
        if write:
            varX = []
            while var.count(''):
                var.remove('')
            for x in var:
                check = x.split(' | ')
                if len(check) != 3:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                try:
                    checkX = int(check[1])
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                if not (check[2] == '0' or check[2] == '1'):
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                x = x.replace(' | ', ', ')
                x = '[' + x + ']'
                varX.append(x)
            var = '|'.join(varX)
        else:
            var = var.split('|')
            var = [x.strip('\r').strip('[').strip(']').split(', ') for x in var]
            newVar = []
            for x in var:
                if len(x) != 3:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                try:
                    if x[2] == '0':
                        x[2] = False
                    elif x[2] == '1':
                        x[2] = True
                    else:
                        return (False, 'Niepoprawne dane - klucz: %s' % record)
                    x = [x[0], int(x[1]), x[2]]
                    newVar.append(x)
                except:
                    return (False, 'Niepoprawne dane - klucz: %s' % record)
                var = newVar
        return [True, var]

    def __checkSc(self, record, var):
        var = var.strip('\r')
        if var not in VAR.allowedCoding:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        return [True, var]



    def R(self, record):
        self.__checkIfFileExist(False)
        content = {}
        for x in CD.open((str(appdata) + '\Generator CSV\config.cfg'), 'r', 'utf-8').read().strip('\r').split('\n'):
            x = x.split(' = ')
            try:
                name = x[0].split('(')[0]
                var = x[1]
                type = x[0].split('(')[1].strip(')')
                content[name] = [var, type] 
            except:
                continue
        checkingOutput = self.__checkIfRecordExist(content, record)
        if not checkingOutput[0]:
            MSG('E0003', True, checkingOutput[1])
        var = content[record]
        if var[1] == 'S':
            # String
            var = var[0].strip('\r')
            return var
        elif var[1] == 'Sc':
            # Integer
            checkingOutput = self.__checkSc(record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0003', True, checkingOutput[1])
        elif var[1] == 'I':
            # Integer
            checkingOutput = self.__checkI(False, record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0003', True, checkingOutput[1])
        elif var[1] == 'D':
            # Date (DD.MM.RRRR HH:MM:SS)
            checkingOutput = self.__checkD(False, record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0003', True, checkingOutput[1])
        elif var[1] == 'MSAs':
            # Multiple Specified Arrays - schoolData
            checkingOutput = self.__checkMSAs(False, record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0003', True, checkingOutput[1])
        else:
            MSG('E0003', True, 'Nie można rozpoznać typu klucza %s' % record)
    
    def W(self, changes):
        self.__checkIfFileExist(True)
        file = CD.open(str(appdata) + '\Generator CSV\config.cfg', 'r', 'utf-8').read().split('\n')
        if file[-1] == '':
            file = file[:-1]
        content = {}
        for x in file:
            x = x.split(' = ')
            try:
                name = x[0].split('(')[0]
                var = x[1]
                type = x[0].split('(')[1].strip(')')
                content[name] = [var, type]
            except Exception as exceptInfo:
                MSG('E0003', False, exceptInfo)
        for x in changes:
            name = x
            var = changes[name]
            type = (content[name])[1]
            if type == 'S':
                # String
                pass
            elif type == 'Sc':
                # Integer
                checkingOutput = self.__checkSc(name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'I':
                # Integer
                checkingOutput = self.__checkI(True, name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'D':
                # Date (DD.MM.RRRR HH:MM:SS)
                checkingOutput = self.__checkD(True, name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'MSAs':
                # Multiple Specified Arrays - schoolData
                checkingOutput = self.__checkMSAs(True, name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            else:
                MSG('E0003', False, 'Nie można rozpoznać typu klucza %s' % name)
                return False
            content[name] = [var, type]
        with CD.open(str(appdata) + '\Generator CSV\config.cfg', 'w', 'utf-8') as file:
            for x in content:
                file.write('%s(%s) = %s\n' % (x, (content[x])[1], (content[x][0])))
        return True



CFG = CFG()





# ---------------------------------- # Ładowanie pliku stylu # ---------------------------------- #

class GUI:
    # Funkcje sprawdzające istnienie
    def __checkIfFileExist(self):
        try:
            checkAppdata()
            open(str(appdata) + '\Generator CSV\style.cfg')
        except Exception as exceptInfo:
            checkAppdata()
    
    def __checkIfRecordExist(self, content, record):
        if record in list(content.keys()):
            return [True]
        else:
            return [False, 'Brak danych - klucz: %s' % record]
    

    # Funkcje sprawdzające poprawność rekordu
    def __checkI(self, record, var):
        try:
            var = int(var)
        except:
            return (False, 'Niepoprawne dane - klucz: %s' % record)
        return [True, var]
    
    def __checkB(self, record, var):
        try:
            var = int(var)
        except:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        if var != 0 and var != 1:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        else:
            if var == 0:
                var = False
            else:
                var = True
        return [True, var]
    
    def __checkC(self, record, var):
        if len(var) != 7:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        else:
            if var[0] != '#':
                return [False, 'Niepoprawne dane - klucz: %s' % record]
        return [True, var]
    
    def __checkP(self, record, var):
        try:
            check = open(var)
        except:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        return [True, var]
    
    def __checkFA(self, record, var, array):
        arrays = {
            'position' : ['nw', 'ne', 'en', 'es', 'se', 'sw', 'ws', 'wn'],
            'anchor' : ['center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'],
            'relief' : ['flat', 'raised', 'sunken', 'groove', 'ridge'],
            'fill' : ['x', 'y', 'both'],
            'activestyle' : ['dotbox', 'none', 'underline']
        }
        if var not in arrays[array]:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        return [True, var]
    
    def __checkF(self, record, var):
        try:
            check = int(var.split(';')[1])
        except:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        else:
            var = (var.split(';')[0], int(var.split(';')[1]))
        return [True, var]
    
    

    def R(self, record):
        self.__checkIfFileExist()
        content = {}
        for x in CD.open((str(appdata) + '\Generator CSV\style.cfg'), 'r', 'utf-8').read().strip('\r').split('\n'):
            x = x.split(' = ')
            try:
                name = x[0].split('(')[0]
                var = x[1]
                type = x[0].split('(')[1].strip(')')
                content[name] = [var.strip('\r'), type] 
            except:
                continue
        checkingOutput = self.__checkIfRecordExist(content, record)
        if not checkingOutput[0]:
            MSG('E0005', True, checkingOutput[1])
        var = content[record]
        if var[1] == 'I':
            # Integer
            checkingOutput = self.__checkI(record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0005', True, checkingOutput[1])
        elif var[1] == 'B':
            # Boolean
            checkingOutput = self.__checkB(record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0005', True, checkingOutput[1])
        elif var[1] == 'C':
            # Color
            checkingOutput = self.__checkC(record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0005', True, checkingOutput[1])
        elif var[1] == 'P':
            # Path
            checkingOutput = self.__checkP(record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0005', True, checkingOutput[1])
        elif (var[1])[:2] == 'FA':
            # From Array
            checkingOutput = self.__checkFA(record, var[0], (var[1])[2:])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0005', True, checkingOutput[1])
        elif var[1] == 'F':
            # Font
            checkingOutput = self.__checkF(record, var[0])
            if checkingOutput[0]:
                return checkingOutput[1]
            else:
                MSG('E0005', True, checkingOutput[1])
        else:
            MSG('E0005', True, 'Nie można rozpoznać typu klucza %s' % record)



GUI = GUI()





# ------------------------------- # Zarządzanie plikami formatu # ------------------------------- #

class FMT:
    # Funkcje sprawdzające istnienie
    def __checkIfFolderExist(self):
        checkAppdata()

    def __checkIfRecordExist(self, content, record):
        if record in list(content.keys()):
            return [True]
        else:
            return [False, 'Brak danych - klucz: %s' % record]

    
    # Funkcje sprawdzające poprawność rekordu
    def __checkB(self, write, record, var):
        if write:
            if var == True:
                var = '1'
            elif var == False:
                var = '0'
            else:
                return [False, 'Niepoprawne dane - klucz: %s' % record]
        else:
            try:
                var = int(var)
            except:
                return [False, 'Niepoprawne dane - klucz: %s' % record]
            if var != 0 and var != 1:
                return [False, 'Niepoprawne dane - klucz: %s' % record]
            else:
                if var == 0:
                    var = False
                else:
                    var = True
        return [True, var]

    def __checkSs(self, record, var):
        check = var
        check = check.strip('<enter>')
        for x in check:
            if x not in VAR.allowedCharactersInSeparator:
                return [False, 'Niepoprawne dane - klucz: %s' % record]
        return [True, var]
    
    def __checkAs(self, write, record, var):
        if write:
            check = var
            for x in check:
                x = x.strip('<enter>')
                for y in x:
                    if y not in VAR.allowedCharactersInSeparator:
                        return [False, 'Niepoprawne dane - klucz: %s' % record]
            var = str(var)
        else:
            new_contentVar = (var)[2:-2].split("', '")
            check = new_contentVar
            for x in check:
                x = x.strip('<enter>')
                for y in x:
                    if y not in VAR.allowedCharactersInSeparator:
                        return [False, 'Niepoprawne dane - klucz: %s' % record]
            var = new_contentVar
        return [True, var]
    
    def __checkI(self, write, record, var):
        if write:
            try:
                var = int(var)
            except:
                return (False, 'Niepoprawne dane - klucz: %s' % record)                
            var = str(var)
        else:
            try:
                var = int(var)
            except:
                return (False, 'Niepoprawne dane - klucz: %s' % record)
        return [True, var]
    
    def __checkSc(self, record, var):
        if var not in VAR.allowedCoding:
            return [False, 'Niepoprawne dane - klucz: %s' % record]
        return [True, var]


    # Funkcja zwracająca listę presetów
    def getList(self):
        self.__checkIfFolderExist()
        filesList = OS.listdir(str(appdata) + '/Generator CSV/format-presets')
        formatPresetsList = []
        for x in filesList:
            if x[-4:] == '.fmt':
                formatPresetsList.append(x[:-4])
            else:
                continue
        return formatPresetsList
    
    

    def R(self, preset, record):
        self.__checkIfFolderExist()
        if preset in self.getList():
            path = str(appdata) + '/Generator CSV/format-presets/%s.fmt' % preset
            file = CD.open(path, 'r', 'utf-8').read().strip('\r').split('\n')
            content = {}
            for x in file:
                x = x.split(' = ')
                try:
                    name = x[0].split('(')[0]
                    var = x[1]
                    type = x[0].split('(')[1].strip(')')
                    content[name] = [var, type] 
                except:
                    continue
            checkingOutput = self.__checkIfRecordExist(content, record)
            if not checkingOutput[0]:
                MSG('E0006', False, checkingOutput[1])
            var = content[record]
            if var[1] == 'B':
                # Boolean
                checkingOutput = self.__checkB(False, record, var[0])
                if checkingOutput[0]:
                    return checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
            elif var[1] == 'Ss':
                # String - separator
                checkingOutput = self.__checkSs(record, var[0])
                if checkingOutput[0]:
                    return checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
            elif var[1] == 'As':
                # Array - separator
                checkingOutput = self.__checkAs(False, record, var[0])
                if checkingOutput[0]:
                    return checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
            elif var[1] == 'I':
                # Integer
                checkingOutput = self.__checkI(False, record, var[0])
                if checkingOutput[0]:
                    return checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
            elif var[1] == 'Sc':
                # Integer
                checkingOutput = self.__checkSc(record, var[0])
                if checkingOutput[0]:
                    return checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
            else:
                MSG('E0006', True, 'Nie można rozpoznać typu klucza %s' % record)
        else:
            content = {
                "student" : True,
                "personSeparator" : '',
                "rowSeparator" : '',
                "dataSeparators" : [],
                "loginRow" : 0,
                "loginPositionInRow" : 0,
                "fnameRow" : 0,
                "fnamePositionInRow" : 0,
                "lnameRow" : 0,
                "lnamePositionInRow" : 0,
                "schoolRow" : 0,
                "schoolPositionInRow" : 0,
                "classRow" : 0,
                "classPositionInRow" : 0,
                "inputCoding" : 'utf-8',
            }
            var = content[record]
        return var

    def W(self, preset, changes):
        self.__checkIfFolderExist()
        if preset in self.getList():
            file = CD.open(str(appdata) + '/Generator CSV/format-presets/%s.fmt' % preset, 'r', 'utf-8').read().split('\n')
            if file[-1] == '':
                file = file[:-1]
            content = {}
            for x in file:
                x = x.split(' = ')
                try:
                    name = x[0].split('(')[0]
                    var = x[1]
                    type = x[0].split('(')[1].strip(')')
                    content[name] = [var, type]
                except Exception as exceptInfo:
                    MSG('E0006', False, exceptInfo)
        else:
            content = {
                "student" : ['1', 'B'],
                "personSeparator" : ['', 'Ss'],
                "rowSeparator" : ['', 'Ss'],
                "dataSeparators" : ['', 'As'],
                "loginRow" : ['0', 'I'],
                "loginPositionInRow" : ['0', 'I'],
                "fnameRow" : ['0', 'I'],
                "fnamePositionInRow" : ['0', 'I'],
                "lnameRow" : ['0', 'I'],
                "lnamePositionInRow" : ['0', 'I'],
                "schoolRow" : ['0', 'I'],
                "schoolPositionInRow" : ['0', 'I'],
                "classRow" : ['0', 'I'],
                "classPositionInRow" : ['0', 'I'],
                "inputCoding" : ['utf-8', 'Sc']
            }
        for x in changes:
            name = x
            var = changes[name]
            type = (content[name])[1]
            if type == 'B':
                checkingOutput = self.__checkB(True, name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'Ss':
                checkingOutput = self.__checkSs(name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'As':
                checkingOutput = self.__checkAs(True, name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'I':
                # Integer
                checkingOutput = self.__checkI(True, name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            elif type == 'Sc':
                checkingOutput = self.__checkSc(name, var)
                if checkingOutput[0]:
                    var = checkingOutput[1]
                else:
                    MSG('E0006', False, checkingOutput[1])
                    return False
            else:
                MSG('E0003', False, 'Nie można rozpoznać typu klucza %s' % name)
                return False
            content[name] = [var, type]
        with CD.open(str(appdata) + '/Generator CSV/format-presets/%s.fmt' % preset, 'w', 'utf-8') as file:
            for x in content:
                file.write('%s(%s) = %s\n' % (x, (content[x])[1], (content[x][0])))
        return True



FMT = FMT()





# ---------------------------------- # Przetwarzanie plików # ----------------------------------- #

class dataProcess:
    # Funkcje sprawdzające istnienie
    def __checkIfAtLeastOneInputFileIsFilled(self, files):
        filledFiles = []
        index = 0
        for x in files:
            if not (x[0] == '' or x[1] == ''):
                filledFiles.append(index)
            index += 1
        if len(filledFiles) != 0:
            return [True, filledFiles]
        else:
            return [False]

    def __checkIfInputFilesIsReadable(self, files, filledFiles):
        for x in filledFiles:
            try:
                check = CD.open((files[x])[0], 'r', FMT.R((files[x])[1], 'inputCoding'))
            except:
                return False
        return True
    
    def __checkIfInputFilesFormatPresetsExist(self, files, filledFiles):
        for x in filledFiles:
            if (files[x])[1] not in FMT.getList():
                return False
        return True

    def __checkIfCreatingOutputFilesIsPossible(self, files):
        try:
            check = CD.open(files[0], 'w', CFG.R('mailOutputCoding'))
            check = CD.open(files[1], 'w', CFG.R('officeOutputCoding'))
        except:
            return False
        return True
    

    # Funkcje sprawdzające poprawność
    def __checkLogin(self, var, student):
        if student and var[-1] != 'u':
            return [False, 'Brak końcówki "u" w loginie ucznia: ']
        if student:
            try:
                x = int(var[:-1])
            except:
                return [False, 'Niedozwolone znaki w loginie osoby: ']
        else:
            try:
                x = int(var)
            except:
                return [False, 'Niedozwolone znaki w loginie osoby: ']
        return [True]

    def __checkFname(self, var):
        if not var.isalpha():
            return [False, 'Niedozwolone znaki w imieniu osoby: ']
        return [True]

    def __checkLname(self, var):
        if not var.isalpha():
            return [False, 'Niedozwolone znaki w nazwisku osoby: ']
        return [True]
    
    def __checkSchool(self, var):
        allowedSchools = [x[0] for x in CFG.R('schoolData')]
        if var not in allowedSchools:
            return [False, 'Niewspierana szkoła w danych osoby: ']
        return [True]

    def __checkClass(self, var, school):
        if len(var) != 2:
            return [False, 'Niepoprawny format klasy w danych osoby: ']
        if not var[0].isdigit():
            return [False, 'Niepoprawny format klasy w danych osoby: ']
        if not var[1].isalpha():
            return [False, 'Niepoprawny format klasy w danych osoby: ']
        schoolData = {}
        for x in CFG.R('schoolData'):
            schoolData[x[0]] = x[1]
        if int(var[0]) == 0 or int(var[0]) > schoolData[school]:
            return [False, 'Numer klasy nie zgadza się z ilością klas szkoły w danych osoby: ']
        return [True]



    # Funkcje operujące na danych
    def __getData(self, input):
        data = []
        for x in input:
            path = x[0]
            format = x[1]
            personSeparator = FMT.R(format, 'personSeparator').replace('<enter>', '\r\n')
            linesSeparator = FMT.R(format, 'rowSeparator').replace('<enter>', '\r\n')
            dataSeparators = [x.replace('<enter>', '\n') for x in FMT.R(format, 'dataSeparators')]
            loginLocation = [FMT.R(format, 'loginRow'), FMT.R(format, 'loginPositionInRow')]
            fnameLocation = [FMT.R(format, 'fnameRow'), FMT.R(format, 'fnamePositionInRow')]
            lnameLocation = [FMT.R(format, 'lnameRow'), FMT.R(format, 'lnamePositionInRow')]
            schoolLocation = [FMT.R(format, 'schoolRow'), FMT.R(format, 'schoolPositionInRow')]
            classLocation = [FMT.R(format, 'classRow'), FMT.R(format, 'classPositionInRow')]
            student = FMT.R(format, 'student')
            file =  CD.open(path, 'r', FMT.R(format, 'inputCoding')).read().split(personSeparator)
            for x in file:
                lines = x.split(linesSeparator)
                dataX = []
                for line in lines:
                    line = [line]
                    for a in dataSeparators:
                        line2 = []
                        for b in line:
                            line2 += b.split(a)
                        line = line2
                    dataX.append(line)
                login = dataX[loginLocation[0] - 1][loginLocation[1] - 1]
                fname = dataX[fnameLocation[0] - 1][fnameLocation[1] - 1]
                lname = dataX[lnameLocation[0] - 1][lnameLocation[1] - 1]
                if student:
                    school = dataX[schoolLocation[0] - 1][schoolLocation[1] - 1]
                    classX = dataX[classLocation[0] - 1][classLocation[1] - 1]
                    data.append([student, login, fname, lname, school, classX])
                else:
                    data.append([student, login, fname, lname])
        return data
    
    def __processData(self, data):
        mailData = []
        officeData = []
        schoolData = {}
        for x in CFG.R('schoolData'):
            schoolData[x[0]] = [x[1], x[2]]
        for x in data:
            mail = ''
            office = ''
            mail += x[2].lower().replace('ę', 'e').replace('ó', 'o').replace('ą', 'a').replace('ś', 's').replace('ł', 'l').replace('ż', 'z').replace('ź', 'z').replace('ć', 'c').replace('ń', 'n')
            mail += '.'
            mail += x[3].lower().replace('ę', 'e').replace('ó', 'o').replace('ą', 'a').replace('ś', 's').replace('ł', 'l').replace('ż', 'z').replace('ź', 'z').replace('ć', 'c').replace('ń', 'n')
            if x[0]:
                classIndicator = ''
                actualYear = TM.localtime()
                schoolDuration = (schoolData[x[4]])[0]
                if actualYear[1] < CFG.R('schoolyearStart')['M'] or (actualYear[1] == CFG.R('schoolyearStart')['M'] and actualYear[2] < CFG.R('schoolyearStart')['D']):
                    yearOfGraduation = actualYear[0] + (schoolDuration - int((x[5])[0]))
                else:
                    yearOfGraduation = actualYear[0] + (schoolDuration - int((x[5])[0])) + 1
                mail += str(yearOfGraduation)
                if (schoolData[x[4]])[1]:
                    mail += x[4].lower()
                else:
                    mail += (x[5])[1].lower()
            mail += '@'
            mail += CFG.R('domain')
            office += mail
            mail += ','
            mail += x[1]
            mail += ':'
            mail += (x[2])[0].lower().replace('ę', 'e').replace('ó', 'o').replace('ą', 'a').replace('ś', 's').replace('ł', 'l').replace('ż', 'z').replace('ź', 'z').replace('ć', 'c').replace('ń', 'n').upper()
            mail += (x[3])[0].lower().replace('ę', 'e').replace('ó', 'o').replace('ą', 'a').replace('ś', 's').replace('ł', 'l').replace('ż', 'z').replace('ź', 'z').replace('ć', 'c').replace('ń', 'n').upper()
            mail += ','
            mail += str(CFG.R('quota'))
            office += ','
            office += x[2]
            office += ','
            office += x[3]
            office += ','
            office += '%s %s' % (x[2], x[3])
            office += ','
            if x[0]:
                office += 'uczeń'
            else:
                office += 'nauczyciel'
            office += ','
            if x[0]:
                office += str(yearOfGraduation)
                if (schoolData[x[4]])[1]:
                    office += x[4].lower()
                else:
                    office += (x[5])[1].lower()
            office += ','
            office += ','
            office += ','
            office += ','
            office += ','
            office += ','
            office += ','
            office += ','
            office += ','
            office += CFG.R('country')
            mailData.append(mail)
            officeData.append(office)
        return [mailData, officeData]

    def __saveData(self, output, data):
        mailPath = output[0]
        officePath = output[1]
        mailData = data[0]
        officeData = data[1]
        with CD.open(mailPath, 'w', CFG.R('mailOutputCoding')) as mail:
            mail.write('\n'.join(mailData))
        with CD.open(officePath, 'w', CFG.R('officeOutputCoding')) as office:
            office.write('\n'.join(officeData))
        



    def start(self, files):
        checkingOutput = []

        testOutput = self.__checkIfAtLeastOneInputFileIsFilled(files[:-1])
        checkingOutput.append(testOutput[0])
        if not testOutput[0]:
            return checkingOutput
        filledFiles = testOutput[1]

        testOutput = self.__checkIfInputFilesIsReadable(files[:-1], filledFiles)
        checkingOutput.append(testOutput)
        if not testOutput:
            return checkingOutput

        testOutput = self.__checkIfInputFilesFormatPresetsExist(files[:-1], filledFiles)
        checkingOutput.append(testOutput)
        if not testOutput:
            return checkingOutput

        input = []
        for x in filledFiles:
            input.append(files[x])
        output = files[-1]
        
        try:
            data = self.__getData(input)
        except:
            checkingOutput.append(False)
            return checkingOutput
        else:
            checkingOutput.append(True)
        
        for x in data:
            student = x[0]
            login = x[1]
            loginCheckingOutput = self.__checkLogin(login, student)
            if not loginCheckingOutput[0]:
                loginCheckingOutput[1] = loginCheckingOutput[1] + str(x[1:])
                checkingOutput.append(loginCheckingOutput)
                return checkingOutput
            fname = x[2]
            fnameCheckingOutput = self.__checkFname(fname)
            if not fnameCheckingOutput[0]:
                fnameCheckingOutput[1] = fnameCheckingOutput[1] + str(x[1:])
                checkingOutput.append(fnameCheckingOutput)
                return checkingOutput
            lname = x[3]
            lnameCheckingOutput = self.__checkLname(lname)
            if not lnameCheckingOutput[0]:
                lnameCheckingOutput[1] = lnameCheckingOutput[1] + str(x[1:])
                checkingOutput.append(lnameCheckingOutput)
                return checkingOutput
            if student:
                school = x[4]
                schoolCheckingOutput = self.__checkSchool(school)
                if not schoolCheckingOutput[0]:
                    schoolCheckingOutput[1] = schoolCheckingOutput[1] + str(x[1:])
                    checkingOutput.append(schoolCheckingOutput)
                    return checkingOutput
                classX = x[5]
                classCheckingOutput = self.__checkClass(classX, school)
                if not classCheckingOutput[0]:
                    classCheckingOutput[1] = classCheckingOutput[1] + str(x[1:])
                    checkingOutput.append(classCheckingOutput)
                    return checkingOutput
        checkingOutput.append([True])
        
        try:
            data = self.__processData(data)
        except:
            checkingOutput.append(False)
            return checkingOutput
        else:
            checkingOutput.append(True)

        testOutput = self.__checkIfCreatingOutputFilesIsPossible(files[-1])
        checkingOutput.append(testOutput)
        if not testOutput:
            return checkingOutput
        
        try:
            self.__saveData(output, data)
        except:
            checkingOutput.append(False)
            return checkingOutput
        else:
            checkingOutput.append(True)
            return checkingOutput



dataProcess = dataProcess()





# ------------------------------------------- # GUI # ------------------------------------------- #

class mainWindow:
    def __init__(self, master):
        # Okno
        self.master = master
        master.title('%s %s %s' % (VAR.programName, VAR.programVersion, VAR.programVersionStage))
        master.geometry('%ix%i' % (GUI.R('windowWidth'), GUI.R('windowHeight')))
        master.resizable(width = GUI.R('windowWidthResizable'), height = GUI.R('windowHeightResizable'))
        master.configure(bg = GUI.R('windowMainBG'))
        master.iconbitmap(GUI.R('mainIcon'))




        # Theme
        TKttk.Style().theme_create("main", parent = "default", settings = {
            "mainMenu.TNotebook": {
                "configure": {
                    "background": GUI.R('mainMenuBG'),
                    "tabposition": GUI.R('mainMenuPosition'),
                    "borderwidth": GUI.R('tabFramesBorderWidth'),
                },
            },
            "mainMenu.TNotebook.Tab": {
                "configure": {
                    "background": GUI.R('unselectedTabBG'),
                    "borderwidth": GUI.R('menuTabsBorderWidth'),
                    "padding": GUI.R('menuTabsPadding'),
                },
                "map": {
                    "background": [
                        ("selected", GUI.R('selectedTabBG')),
                        ("disabled", GUI.R('disabledTabBG')),
                    ]
                }
            },
            "mainMenuTabFrame.TFrame": {
                "configure": {
                    "background": GUI.R('tabFrameBG'),
                },
            },
            "tabHeader.TLabel": {
                "configure": {
                    "font": GUI.R('headerFont'),
                    "background": GUI.R('headerBG'),
                    "foreground": GUI.R('headerTextColor'),
                    "padding": GUI.R('headerPadding'),
                    "anchor": GUI.R('headerTextAnchor'),
                },
            },
            "contentTabFrame.TFrame": {
                "configure": {
                    "background": GUI.R('contentTabFrameBG'),
                },
            },
            "layoutFrame.TFrame": {
                "configure": {
                    "background": GUI.R('layoutFrameBG'),
                },
            },
            "label1.TLabel": {
                "configure": {
                    "background": GUI.R('label1BG'),
                    "foreground": GUI.R('label1TextColor'),
                    "font": GUI.R('label1Font'),
                },
            },
            "label2.TLabel": {
                "configure": {
                    "background": GUI.R('label2BG'),
                    "foreground": GUI.R('label2TextColor'),
                    "font" : GUI.R('label2Font')
                },
            },
            "label3.TLabel": {
                "configure": {
                    "background": GUI.R('label3BG'),
                    "foreground": GUI.R('label3TextColor'),
                    "font" : GUI.R('label3Font')
                },
            },
            "label4.TLabel": {
                "configure": {
                    "background": GUI.R('label4BG'),
                    "foreground": GUI.R('label4TextColor'),
                    "font": GUI.R('label4Font'),
                },
            },
            "combobox1.TCombobox": {
                "configure": {
                    "arrowcolor": GUI.R('combobox1ArrowColor'),
                    "background": GUI.R('combobox1ButtonColor'),
                    "bordercolor": GUI.R('combobox1BorderColor'),
                    "fieldbackground": GUI.R('combobox1FieldBackground'),
                    "foreground": GUI.R('combobox1TextColor'),
                    "relief": GUI.R('combobox1Relief'),
                    "borderwidth": GUI.R('combobox1BorderWidth'),
                    "padding": GUI.R('combobox1Padding'),
                },
            },
            "combobox2.TCombobox": {
                "configure": {
                    "arrowcolor": GUI.R('combobox2ArrowColor'),
                    "background": GUI.R('combobox2ButtonColor'),
                    "bordercolor": GUI.R('combobox2BorderColor'),
                    "fieldbackground": GUI.R('combobox2FieldBackground'),
                    "foreground": GUI.R('combobox2TextColor'),
                    "relief": GUI.R('combobox2Relief'),
                    "borderwidth": GUI.R('combobox2BorderWidth'),
                    "padding": GUI.R('combobox2Padding'),
                },
            },
            "button1.TButton": {
                "configure": {
                    "anchor": GUI.R('button1TextAnchor'),
                    "background": GUI.R('button1Background'),
                    "foreground": GUI.R('button1Foreground'),
                    "padding": GUI.R('button1Padding'),
                },
            },
            "button2.TButton": {
                "configure": {
                    "anchor": GUI.R('button2TextAnchor'),
                    "background": GUI.R('button2Background'),
                    "padding": GUI.R('button2Padding'),
                },
            },
            "separator1.TSeparator": {
                "configure": {
                    "background": GUI.R('separator1BG'),
                },
            },
            "spinbox1.TSpinbox": {
                "configure": {
                    "arrowcolor": GUI.R('spinbox1ArrowColor'),
                    "fieldbackground": GUI.R('spinbox1FieldBackground'),
                    "relief": GUI.R('spinbox1Relief'),
                    "borderwidth": GUI.R('spinbox1BorderWidth'),
                    "foreground": GUI.R('spinbox1TextColor'),
                    "background": GUI.R('spinbox1ButtonColor'),
                    "padding" : GUI.R('spinbox1Padding'),
                },
            },
            "entry1.TEntry": {
                "configure": {
                    "fieldbackground": GUI.R('entry1FieldBackground'),
                    "relief": GUI.R('entry1Relief'),
                    "borderwidth": GUI.R('entry1BorderWidth'),
                    "padding": GUI.R('entry1Padding'),
                    "foreground": GUI.R('entry1TextColor'),
                },
            },
        })
        TKttk.Style().theme_use("main")




        # Menu główne
        self.mainMenu = TKttk.Notebook(master, width = master.winfo_width() - (2 * GUI.R('menuTabsPadding') + GUI.R('tabIconsSize')), height = master.winfo_height())
        self.mainMenu.config(style = "mainMenu.TNotebook")
        self.mainMenu.grid(row = 0)

        # Ikona
        self.iconTab = TKttk.Frame(self.mainMenu)
        self.iconTabImg = PLimg.open(GUI.R('iconTabIcon'))
        self.iconTabImg = self.iconTabImg.resize((GUI.R('tabIconsSize'), GUI.R('tabIconsSize')), PLimg.ANTIALIAS)
        self.iconTabImg = PLitk.PhotoImage(self.iconTabImg)
        self.mainMenu.add(self.iconTab, image = self.iconTabImg, state = TK.DISABLED)




        # TAB1 - Generator ####################################################

        self.generateTab = TKttk.Frame(self.mainMenu)
        self.generateTab.config(style = "mainMenuTabFrame.TFrame")
        self.generateTabImg = PLimg.open(GUI.R('generateTabIcon'))
        self.generateTabImg = self.generateTabImg.resize((GUI.R('tabIconsSize'), GUI.R('tabIconsSize')), PLimg.ANTIALIAS)
        self.generateTabImg = PLitk.PhotoImage(self.generateTabImg)
        self.mainMenu.add(self.generateTab, image = self.generateTabImg, state = TK.NORMAL)


        # Nagłówek
        self.generateHeader = TKttk.Label(self.generateTab)
        self.generateHeader.config(style = 'tabHeader.TLabel')
        self.generateHeader.config(text = 'GENERATOR CSV')
        self.generateHeader.pack(fill = GUI.R('headerFill'))


        # Zawartość
        self.generateFrame = TKttk.Frame(self.generateTab)
        self.generateFrame.config(style = 'contentTabFrame.TFrame')
        self.generateFrame.pack(fill = GUI.R('contentTabFrameFill'), expand = GUI.R('contentTabFrameExpand'), padx = GUI.R('tabFramePadding'), pady = GUI.R('tabFramePadding'))


        # (1) Pliki #################################################

        self.generateFilesFrame = TKttk.Frame(self.generateFrame)
        self.generateFilesFrame.config(style = 'layoutFrame.TFrame')
        self.generateFilesFrame.pack(fill = TK.BOTH, expand = 1)

        # (2) Pliki wejściowe #############################

        self.generateInputFilesFrame = TKttk.Frame(self.generateFilesFrame)
        self.generateInputFilesFrame.config(style = 'layoutFrame.TFrame')
        self.generateInputFilesFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R('outsidelayoutFramesPadX'))

        # (3) Plik źródłowy 1 ###################

        self.GIF1Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF1Frame.config(style = 'layoutFrame.TFrame')
        self.GIF1Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R('GIFFrameSeparators')/2)))

        # "Plik źródłowy (1)"
        self.GIF1Label = TKttk.Label(self.GIF1Frame)
        self.GIF1Label.config(style = 'label1.TLabel')
        self.GIF1Label.config(width = GUI.R('generateFilesLabelWidth'))
        self.GIF1Label.config(anchor = GUI.R('generateFilesLabelAnchor'))
        self.GIF1Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R('generateInputFilesPadding'))))
        self.GIF1Label.config(text = 'Plik źródłowy (1)')
        self.GIF1Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF1SFrame = TKttk.Frame(self.GIF1Frame)
        self.GIF1SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF1SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF1SLocalizationFrame = TKttk.Frame(self.GIF1SFrame)
        self.GIF1SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF1SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Entry
        self.GIF1SLocalizationEntryVar = TK.StringVar()
        self.GIF1SLocalizationEntry = TKttk.Entry(self.GIF1SLocalizationFrame)
        self.GIF1SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF1SLocalizationEntry.config(textvariable = self.GIF1SLocalizationEntryVar)
        self.GIF1SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Button
        self.GIF1SLocalizationButton = TKttk.Button(self.GIF1SLocalizationFrame)
        self.GIF1SLocalizationButton.config(style = 'button1.TButton')
        self.GIF1SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF1SLocalizationButton.config(command = self.GIF1SLocalizationButtonAction)
        self.GIF1SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R('generateInputFilesPadding'))

        # Format
        self.GIF1SFormatFrame = TKttk.Frame(self.GIF1SFrame)
        self.GIF1SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF1SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Format - Label
        self.GIF1SFormatLabel = TKttk.Label(self.GIF1SFormatFrame)
        self.GIF1SFormatLabel.config(style = 'label2.TLabel')
        self.GIF1SFormatLabel.config(text = 'Format')
        self.GIF1SFormatLabel.pack(side = TK.LEFT, padx = GUI.R('generateInputFilesPadding'))

        # Format - Combobox
        self.GIF1SFormatComboboxVar = TK.StringVar()
        self.GIF1SFormatCombobox = TKttk.Combobox(self.GIF1SFormatFrame)
        self.GIF1SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox1ListBoxBackground'))
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox1ListBoxForeground'))
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox1ListBoxSelectBackground'))
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox1ListBoxSelectForeground'))
        self.GIF1SFormatCombobox.config(state = 'readonly')
        self.GIF1SFormatCombobox.config(textvariable = self.GIF1SFormatComboboxVar)
        self.GIF1SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF1SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        #########################################

        # (3) Plik źródłowy 2 ###################

        self.GIF2Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF2Frame.config(style = 'layoutFrame.TFrame')
        self.GIF2Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R('GIFFrameSeparators')/2)))

        # "Plik źródłowy (1)"
        self.GIF2Label = TKttk.Label(self.GIF2Frame)
        self.GIF2Label.config(style = 'label1.TLabel')
        self.GIF2Label.config(width = GUI.R('generateFilesLabelWidth'))
        self.GIF2Label.config(anchor = GUI.R('generateFilesLabelAnchor'))
        self.GIF2Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R('generateInputFilesPadding'))))
        self.GIF2Label.config(text = 'Plik źródłowy (2)')
        self.GIF2Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF2SFrame = TKttk.Frame(self.GIF2Frame)
        self.GIF2SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF2SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF2SLocalizationFrame = TKttk.Frame(self.GIF2SFrame)
        self.GIF2SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF2SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Entry
        self.GIF2SLocalizationEntryVar = TK.StringVar()
        self.GIF2SLocalizationEntry = TKttk.Entry(self.GIF2SLocalizationFrame)
        self.GIF2SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF2SLocalizationEntry.config(textvariable = self.GIF2SLocalizationEntryVar)
        self.GIF2SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Button
        self.GIF2SLocalizationButton = TKttk.Button(self.GIF2SLocalizationFrame)
        self.GIF2SLocalizationButton.config(style = 'button1.TButton')
        self.GIF2SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF2SLocalizationButton.config(command = self.GIF2SLocalizationButtonAction)
        self.GIF2SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R('generateInputFilesPadding'))

        # Format
        self.GIF2SFormatFrame = TKttk.Frame(self.GIF2SFrame)
        self.GIF2SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF2SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Format - Label
        self.GIF2SFormatLabel = TKttk.Label(self.GIF2SFormatFrame)
        self.GIF2SFormatLabel.config(style = 'label2.TLabel')
        self.GIF2SFormatLabel.config(text = 'Format')
        self.GIF2SFormatLabel.pack(side = TK.LEFT, padx = GUI.R('generateInputFilesPadding'))

        # Format - Combobox
        self.GIF2SFormatComboboxVar = TK.StringVar()
        self.GIF2SFormatCombobox = TKttk.Combobox(self.GIF2SFormatFrame)
        self.GIF2SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox1ListBoxBackground'))
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox1ListBoxForeground'))
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox1ListBoxSelectBackground'))
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox1ListBoxSelectForeground'))
        self.GIF2SFormatCombobox.config(state = 'readonly')
        self.GIF2SFormatCombobox.config(textvariable = self.GIF2SFormatComboboxVar)
        self.GIF2SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF2SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        #########################################

        # (3) Plik źródłowy 3 ###################

        self.GIF3Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF3Frame.config(style = 'layoutFrame.TFrame')
        self.GIF3Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R('GIFFrameSeparators')/2)))

        # "Plik źródłowy (1)"
        self.GIF3Label = TKttk.Label(self.GIF3Frame)
        self.GIF3Label.config(style = 'label1.TLabel')
        self.GIF3Label.config(width = GUI.R('generateFilesLabelWidth'))
        self.GIF3Label.config(anchor = GUI.R('generateFilesLabelAnchor'))
        self.GIF3Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R('generateInputFilesPadding'))))
        self.GIF3Label.config(text = 'Plik źródłowy (3)')
        self.GIF3Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF3SFrame = TKttk.Frame(self.GIF3Frame)
        self.GIF3SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF3SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF3SLocalizationFrame = TKttk.Frame(self.GIF3SFrame)
        self.GIF3SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF3SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Entry
        self.GIF3SLocalizationEntryVar = TK.StringVar()
        self.GIF3SLocalizationEntry = TKttk.Entry(self.GIF3SLocalizationFrame)
        self.GIF3SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF3SLocalizationEntry.config(textvariable = self.GIF3SLocalizationEntryVar)
        self.GIF3SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Button
        self.GIF3SLocalizationButton = TKttk.Button(self.GIF3SLocalizationFrame)
        self.GIF3SLocalizationButton.config(style = 'button1.TButton')
        self.GIF3SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF3SLocalizationButton.config(command = self.GIF3SLocalizationButtonAction)
        self.GIF3SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R('generateInputFilesPadding'))

        # Format
        self.GIF3SFormatFrame = TKttk.Frame(self.GIF3SFrame)
        self.GIF3SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF3SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Format - Label
        self.GIF3SFormatLabel = TKttk.Label(self.GIF3SFormatFrame)
        self.GIF3SFormatLabel.config(style = 'label2.TLabel')
        self.GIF3SFormatLabel.config(text = 'Format')
        self.GIF3SFormatLabel.pack(side = TK.LEFT, padx = GUI.R('generateInputFilesPadding'))

        # Format - Combobox
        self.GIF3SFormatComboboxVar = TK.StringVar()
        self.GIF3SFormatCombobox = TKttk.Combobox(self.GIF3SFormatFrame)
        self.GIF3SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox1ListBoxBackground'))
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox1ListBoxForeground'))
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox1ListBoxSelectBackground'))
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox1ListBoxSelectForeground'))
        self.GIF3SFormatCombobox.config(state = 'readonly')
        self.GIF3SFormatCombobox.config(textvariable = self.GIF3SFormatComboboxVar)
        self.GIF3SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF3SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        #########################################

        # (3) Plik źródłowy 4 ###################

        self.GIF4Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF4Frame.config(style = 'layoutFrame.TFrame')
        self.GIF4Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R('GIFFrameSeparators')/2)))

        # "Plik źródłowy (1)"
        self.GIF4Label = TKttk.Label(self.GIF4Frame)
        self.GIF4Label.config(style = 'label1.TLabel')
        self.GIF4Label.config(width = GUI.R('generateFilesLabelWidth'))
        self.GIF4Label.config(anchor = GUI.R('generateFilesLabelAnchor'))
        self.GIF4Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R('generateInputFilesPadding'))))
        self.GIF4Label.config(text = 'Plik źródłowy (4)')
        self.GIF4Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF4SFrame = TKttk.Frame(self.GIF4Frame)
        self.GIF4SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF4SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF4SLocalizationFrame = TKttk.Frame(self.GIF4SFrame)
        self.GIF4SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF4SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Entry
        self.GIF4SLocalizationEntryVar = TK.StringVar()
        self.GIF4SLocalizationEntry = TKttk.Entry(self.GIF4SLocalizationFrame)
        self.GIF4SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF4SLocalizationEntry.config(textvariable = self.GIF4SLocalizationEntryVar)
        self.GIF4SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        # Lokalizacja - Button
        self.GIF4SLocalizationButton = TKttk.Button(self.GIF4SLocalizationFrame)
        self.GIF4SLocalizationButton.config(style = 'button1.TButton')
        self.GIF4SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF4SLocalizationButton.config(command = self.GIF4SLocalizationButtonAction)
        self.GIF4SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R('generateInputFilesPadding'))

        # Format
        self.GIF4SFormatFrame = TKttk.Frame(self.GIF4SFrame)
        self.GIF4SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF4SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R('generateInputFilesPadding'))

        # Format - Label
        self.GIF4SFormatLabel = TKttk.Label(self.GIF4SFormatFrame)
        self.GIF4SFormatLabel.config(style = 'label2.TLabel')
        self.GIF4SFormatLabel.config(text = 'Format')
        self.GIF4SFormatLabel.pack(side = TK.LEFT, padx = GUI.R('generateInputFilesPadding'))

        # Format - Combobox
        self.GIF4SFormatComboboxVar = TK.StringVar()
        self.GIF4SFormatCombobox = TKttk.Combobox(self.GIF4SFormatFrame)
        self.GIF4SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox1ListBoxBackground'))
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox1ListBoxForeground'))
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox1ListBoxSelectBackground'))
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox1ListBoxSelectForeground'))
        self.GIF4SFormatCombobox.config(state = 'readonly')
        self.GIF4SFormatCombobox.config(textvariable = self.GIF4SFormatComboboxVar)
        self.GIF4SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF4SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R('generateInputFilesPadding'))

        #########################################

        ###################################################

        # (2) Separator1 ##################################

        self.generateSeparator1 = TKttk.Separator(self.generateFilesFrame)
        self.generateSeparator1.config(style = 'separator1.TSeparator')
        self.generateSeparator1.config(orient = TK.HORIZONTAL)
        self.generateSeparator1.pack(fill = TK.X, pady = GUI.R('generateHorizontalSeparatorPadY'))

        ###################################################

        # (2) Pliki wyjściowe #############################
    
        self.generateOutputFilesFrame = TKttk.Frame(self.generateFilesFrame)
        self.generateOutputFilesFrame.config(style = 'layoutFrame.TFrame')
        self.generateOutputFilesFrame.pack(fill = TK.X, padx = GUI.R('outsidelayoutFramesPadX'))

        # (3) Poczta ############################

        self.GOFMailFrame = TKttk.Frame(self.generateOutputFilesFrame)
        self.GOFMailFrame.config(style = 'layoutFrame.TFrame')
        self.GOFMailFrame.pack(pady = GUI.R('generateOutputFilesPadding'), fill = TK.X, expand = 1)

        # "Poczta"
        self.GOFMailLabel = TKttk.Label(self.GOFMailFrame)
        self.GOFMailLabel.config(style = 'label1.TLabel')
        self.GOFMailLabel.config(width = GUI.R('generateFilesLabelWidth'))
        self.GOFMailLabel.config(anchor = GUI.R('generateFilesLabelAnchor'))
        self.GOFMailLabel.config(text = 'Poczta')
        self.GOFMailLabel.pack(side = TK.LEFT)

        # Plik poczty - Lokalizacja (Entry)
        self.GOFMailEntryVar = TK.StringVar()
        self.GOFMailEntry = TKttk.Entry(self.GOFMailFrame)
        self.GOFMailEntry.config(style = 'entry1.TEntry')
        self.GOFMailEntry.config(textvariable = self.GOFMailEntryVar)
        self.GOFMailEntry.pack(padx = 2 * GUI.R('generateOutputFilesPadding'), side = TK.LEFT, fill = TK.X, expand = 1)

        # Plik poczty - Lokalizacja (Button)
        self.GOFMailButton = TKttk.Button(self.GOFMailFrame)
        self.GOFMailButton.config(style = 'button1.TButton')
        self.GOFMailButton.config(text = 'Przeglądaj')
        self.GOFMailButton.config(command = self.GOFMailButtonAction)
        self.GOFMailButton.pack(side = TK.LEFT)
        
        #########################################

        # (3) Office ############################

        self.GOFOfficeFrame = TKttk.Frame(self.generateOutputFilesFrame)
        self.GOFOfficeFrame.config(style = 'layoutFrame.TFrame')
        self.GOFOfficeFrame.pack(pady = GUI.R('generateOutputFilesPadding'), fill = TK.X, expand = 1)

        # "Office"
        self.GOFOfficeLabel = TKttk.Label(self.GOFOfficeFrame)
        self.GOFOfficeLabel.config(style = 'label1.TLabel')
        self.GOFOfficeLabel.config(width = GUI.R('generateFilesLabelWidth'))
        self.GOFOfficeLabel.config(anchor = GUI.R('generateFilesLabelAnchor'))
        self.GOFOfficeLabel.config(text = 'Office')
        self.GOFOfficeLabel.pack(side = TK.LEFT)

        # Plik office - Lokalizacja (Entry)
        self.GOFOfficeEntryVar = TK.StringVar()
        self.GOFOfficeEntry = TKttk.Entry(self.GOFOfficeFrame)
        self.GOFOfficeEntry.config(style = 'entry1.TEntry')
        self.GOFOfficeEntry.config(textvariable = self.GOFOfficeEntryVar)
        self.GOFOfficeEntry.pack(padx = 2 * GUI.R('generateOutputFilesPadding'), side = TK.LEFT, fill = TK.X, expand = 1)

        # Plik office - Lokalizacja (Button)
        self.GOFOfficeButton = TKttk.Button(self.GOFOfficeFrame)
        self.GOFOfficeButton.config(style = 'button1.TButton')
        self.GOFOfficeButton.config(text = 'Przeglądaj')
        self.GOFOfficeButton.config(command = self.GOFOfficeButtonAction)
        self.GOFOfficeButton.pack(side = TK.LEFT)

        #########################################

        ###################################################

        #############################################################

         # (1) Separator2 ###########################################

        self.generateSeparator2 = TKttk.Separator(self.generateFrame)
        self.generateSeparator2.config(style = 'separator1.TSeparator')
        self.generateSeparator2.config(orient = TK.HORIZONTAL)
        self.generateSeparator2.pack(fill = TK.X, pady = GUI.R('generateHorizontalSeparatorPadY'))

        #############################################################

        # (1) Przyciski #############################################

        self.generateButtonsFrame = TKttk.Frame(self.generateFrame)
        self.generateButtonsFrame.config(style = 'layoutFrame.TFrame')
        self.generateButtonsFrame.pack(fill = TK.X, padx = GUI.R('outsidelayoutFramesPadX'))

        # Przycisk "START"
        self.generateStartButton = TKttk.Button(self.generateButtonsFrame)
        self.generateStartButton.config(style = 'button1.TButton')
        self.generateStartButton.config(padding = GUI.R('generateStartButtonPadding'))
        self.generateStartButton.config(text = 'START')
        self.generateStartButton.config(command = self.generateStartButtonAction)
        self.generateStartButton.pack(side = TK.LEFT, fill = TK.X, expand = 1, pady = GUI.R('generateStartButtonPadY'))

        ##############################################################

        #######################################################################




        # TAB3 - Format #######################################################

        self.formatTab = TKttk.Frame(self.mainMenu)
        self.formatTab.config(style = "mainMenuTabFrame.TFrame")
        self.formatTabImg = PLimg.open(GUI.R('formatTabIcon'))
        self.formatTabImg = self.formatTabImg.resize((GUI.R('tabIconsSize'), GUI.R('tabIconsSize')), PLimg.ANTIALIAS)
        self.formatTabImg = PLitk.PhotoImage(self.formatTabImg)
        self.mainMenu.add(self.formatTab, image = self.formatTabImg, state = TK.NORMAL)


        # Nagłówek
        self.formatHeader = TKttk.Label(self.formatTab)
        self.formatHeader.config(style = 'tabHeader.TLabel')
        self.formatHeader.config(text = 'FORMAT DANYCH')
        self.formatHeader.pack(fill = GUI.R('headerFill'))


        # Zawartość
        self.formatFrame = TKttk.Frame(self.formatTab)
        self.formatFrame.config(style = 'contentTabFrame.TFrame')
        self.formatFrame.pack(fill = GUI.R('contentTabFrameFill'), expand = GUI.R('contentTabFrameExpand'), padx = GUI.R('tabFramePadding'), pady = GUI.R('tabFramePadding'))

        
        # (1) Ładowanie presetu #####################################

        self.loadingPresetFrame = TKttk.Frame(self.formatFrame)
        self.loadingPresetFrame.config(style = 'layoutFrame.TFrame')
        self.loadingPresetFrame.pack(fill = TK.X, side = TK.TOP, padx = GUI.R('outsidelayoutFramesPadX'))

        # "Wybierz preset do edycji lub wpisz nazwę nowego"
        self.loadingListLabel = TKttk.Label(self.loadingPresetFrame)
        self.loadingListLabel.config(style = 'label1.TLabel')
        self.loadingListLabel.config(text = 'Wybierz preset do edycji lub wpisz nazwę nowego')
        self.loadingListLabel.pack(side = TK.LEFT)

        # Rozwijana lista presetów
        self.loadingListVar = TK.StringVar()
        self.loadingList = TKttk.Combobox(self.loadingPresetFrame)
        self.loadingList.config(textvariable = self.loadingListVar)
        self.loadingList.config(style = 'combobox2.TCombobox')
        self.loadingList.option_add("*TCombobox*Listbox.background", GUI.R('combobox2ListBoxBackground'))
        self.loadingList.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox2ListBoxForeground'))
        self.loadingList.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox2ListBoxSelectBackground'))
        self.loadingList.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox2ListBoxSelectForeground'))
        self.loadingList.pack(side = TK.LEFT, padx = GUI.R('loadingListPadX'), fill = TK.X, expand = 1)
        self.loadingList['values'] = tuple(FMT.getList())

        # Przycisk "WCZYTAJ"
        self.loadingButton = TKttk.Button(self.loadingPresetFrame)
        self.loadingButton.config(style = 'button1.TButton')
        self.loadingButton.config(command = self.loadingButtonAction)
        self.loadingButton.config(width = GUI.R('loadingButtonWidth'))
        self.loadingButton.config(text = 'WCZYTAJ')
        self.loadingButton.pack(side = TK.RIGHT)

        #############################################################

        # (1) Separator 1 ###########################################

        self.formatSeparator1 = TKttk.Separator(self.formatFrame)
        self.formatSeparator1.config(style = 'separator1.TSeparator')
        self.formatSeparator1.config(orient = TK.HORIZONTAL)
        self.formatSeparator1.pack(fill = TK.X, pady = GUI.R('formatHorizontalSeparatorPadY'))

        #############################################################

        # (1) Edycja presetu ########################################

        self.editingPresetFrame = TKttk.Frame(self.formatFrame)
        self.editingPresetFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R('outsidelayoutFramesPadX'))
        
        # (2) Ustawienia ##################################

        self.editingPresetSettingsFrame = TKttk.Frame(self.editingPresetFrame)
        self.editingPresetSettingsFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetSettingsFrame.pack(fill = TK.BOTH, expand = 1)

        # (3) Inne ustawienia ###################

        self.editingPresetOSFrame = TKttk.Frame(self.editingPresetSettingsFrame)
        self.editingPresetOSFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetOSFrame.pack(fill = TK.BOTH, expand = 1, side = TK.LEFT)
        
        # (5) Typ osoby ###############

        self.EPOSTypeFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSTypeFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSTypeFrame.pack(fill = TK.X, expand = 1, pady = GUI.R('EPOSTypeFramePadY'))

        # "Typ osoby"
        self.EPOSTypeLabel = TKttk.Label(self.EPOSTypeFrame)
        self.EPOSTypeLabel.config(style = 'label1.TLabel')
        self.EPOSTypeLabel.config(width = GUI.R('EPOSLabelWidth'))
        self.EPOSTypeLabel.config(anchor = GUI.R('EPOSLabelAnchor'))
        self.EPOSTypeLabel.config(text = 'Typ osoby')
        self.EPOSTypeLabel.pack(side = TK.LEFT)

        # Radiobutton
        self.EPOSTypeVar = TK.BooleanVar(value = True)

        self.EPOSTypeStudentRadiobutton = TK.Radiobutton(self.EPOSTypeFrame)
        self.EPOSTypeStudentRadiobutton.config(background = GUI.R('radiobutton1Background'))
        self.EPOSTypeStudentRadiobutton.config(foreground = GUI.R('radiobutton1TextColor'))
        self.EPOSTypeStudentRadiobutton.config(selectcolor = GUI.R('radiobutton1IndicatorBackground'))
        self.EPOSTypeStudentRadiobutton.config(activebackground = GUI.R('radiobutton1Background'))
        self.EPOSTypeStudentRadiobutton.config(activeforeground = GUI.R('radiobutton1TextColor'))
        self.EPOSTypeStudentRadiobutton.config(variable = self.EPOSTypeVar)
        self.EPOSTypeStudentRadiobutton.config(value = True)
        self.EPOSTypeStudentRadiobutton.config(state = TK.DISABLED)
        self.EPOSTypeStudentRadiobutton.config(text = 'Uczniowie')
        self.EPOSTypeStudentRadiobutton.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        self.EPOSTypeTeacherRadiobutton = TK.Radiobutton(self.EPOSTypeFrame)
        self.EPOSTypeTeacherRadiobutton.config(background = GUI.R('radiobutton1Background'))
        self.EPOSTypeTeacherRadiobutton.config(foreground = GUI.R('radiobutton1TextColor'))
        self.EPOSTypeTeacherRadiobutton.config(selectcolor = GUI.R('radiobutton1IndicatorBackground'))
        self.EPOSTypeTeacherRadiobutton.config(activebackground = GUI.R('radiobutton1Background'))
        self.EPOSTypeTeacherRadiobutton.config(activeforeground = GUI.R('radiobutton1TextColor'))
        self.EPOSTypeTeacherRadiobutton.config(variable = self.EPOSTypeVar)
        self.EPOSTypeTeacherRadiobutton.config(value = False)
        self.EPOSTypeTeacherRadiobutton.config(state = TK.DISABLED)
        self.EPOSTypeTeacherRadiobutton.config(text = 'Nauczyciele')
        self.EPOSTypeTeacherRadiobutton.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        
        #####################

        # (5) Separator pomiedzy osobami

        self.EPOSPersonSeparatorFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSPersonSeparatorFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSPersonSeparatorFrame.pack(fill = TK.X, expand = 1, pady = GUI.R('EPOSPersonSeparatorFramePadY'))
        
        # "Separator pomiędzy osobami"
        self.EPOSPersonSeparatorLabel = TKttk.Label(self.EPOSPersonSeparatorFrame)
        self.EPOSPersonSeparatorLabel.config(style = 'label1.TLabel')
        self.EPOSPersonSeparatorLabel.config(width = GUI.R('EPOSLabelWidth'))
        self.EPOSPersonSeparatorLabel.config(anchor = GUI.R('EPOSLabelAnchor'))
        self.EPOSPersonSeparatorLabel.config(text = 'Separator pomiędzy osobami')
        self.EPOSPersonSeparatorLabel.pack(side = TK.LEFT)

        # Entry - Separator pomiedzy osobami
        self.EPOSPersonSeparatorVar = TK.StringVar()
        self.EPOSPersonSeparatorEntry = TKttk.Entry(self.EPOSPersonSeparatorFrame)
        self.EPOSPersonSeparatorEntry.config(style = 'entry1.TEntry')
        self.EPOSPersonSeparatorEntry.config(textvariable = self.EPOSPersonSeparatorVar)
        self.EPOSPersonSeparatorEntry.config(state = TK.DISABLED)
        self.EPOSPersonSeparatorEntry.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        #####################

        # (5) Separator pomiedzy wierszami

        self.EPOSRowSeparatorFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSRowSeparatorFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSRowSeparatorFrame.pack(fill = TK.X, expand = 1, pady = GUI.R('EPOSRowSeparatorFramePadY'))

        # "Separator pomiędzy wierszami"
        self.EPOSRowSeparatorLabel = TKttk.Label(self.EPOSRowSeparatorFrame)
        self.EPOSRowSeparatorLabel.config(style = 'label1.TLabel')
        self.EPOSRowSeparatorLabel.config(width = GUI.R('EPOSLabelWidth'))
        self.EPOSRowSeparatorLabel.config(anchor = GUI.R('EPOSLabelAnchor'))
        self.EPOSRowSeparatorLabel.config(text = 'Separator pomiędzy wierszami')
        self.EPOSRowSeparatorLabel.pack(side = TK.LEFT)

        # Entry - Separator pomiedzy wierszami
        self.EPOSRowSeparatorVar = TK.StringVar()
        self.EPOSRowSeparatorEntry = TKttk.Entry(self.EPOSRowSeparatorFrame)
        self.EPOSRowSeparatorEntry.config(style = 'entry1.TEntry')
        self.EPOSRowSeparatorEntry.config(textvariable = self.EPOSRowSeparatorVar)
        self.EPOSRowSeparatorEntry.config(state = TK.DISABLED)
        self.EPOSRowSeparatorEntry.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        #####################

        # (5) Separatory pomiedzy danymi

        self.EPOSDataSeparatorFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSDataSeparatorFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSDataSeparatorFrame.pack(fill = TK.BOTH, expand = 1, pady = GUI.R('EPOSDataSeparatorFramePadY'))

        # "Separatory pomiędzy danymi"
        self.EPOSDataSeparatorLabel = TKttk.Label(self.EPOSDataSeparatorFrame)
        self.EPOSDataSeparatorLabel.config(style = 'label1.TLabel')
        self.EPOSDataSeparatorLabel.config(width = GUI.R('EPOSLabelWidth'))
        self.EPOSDataSeparatorLabel.config(anchor = GUI.R('EPOSLabelAnchor'))
        self.EPOSDataSeparatorLabel.config(text = 'Separatory pomiędzy danymi')
        self.EPOSDataSeparatorLabel.pack(side = TK.LEFT)

        # Entry - Separator pomiedzy wierszami
        self.EPOSDataSeparatorText = TK.Text(self.EPOSDataSeparatorFrame)
        self.EPOSDataSeparatorText.config(state = TK.DISABLED)
        self.EPOSDataSeparatorText.config(background = GUI.R('text1Background'))
        self.EPOSDataSeparatorText.config(foreground = GUI.R('text1TextColor'))
        self.EPOSDataSeparatorText.config(relief = GUI.R('text1Relief'))
        self.EPOSDataSeparatorText.pack(side = TK.TOP, fill = TK.BOTH)

        #####################
        
        ###############################

        # (5) Separator 2 #############

        self.formatSeparator2 = TKttk.Separator(self.editingPresetSettingsFrame)
        self.formatSeparator2.config(style = 'separator1.TSeparator')
        self.formatSeparator2.config(orient = TK.VERTICAL)
        self.formatSeparator2.pack(fill = TK.Y, padx = GUI.R('formatVerticalSeparatorPadY'), side = TK.LEFT)

        ###############################

        # (5) Lokalizacja danych ######

        self.editingPresetDLFrame = TKttk.Frame(self.editingPresetSettingsFrame)
        self.editingPresetDLFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetDLFrame.pack(fill = TK.BOTH, side = TK.RIGHT)
        self.editingPresetDLFrame.grid_columnconfigure(1, weight = 1)
        self.editingPresetDLFrame.grid_columnconfigure(2, weight = 1)
        
        # C1 - "Wiersz"
        self.EPDLC1Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLC1Label.config(style = 'label1.TLabel')
        self.EPDLC1Label.config(text = 'Wiersz')
        self.EPDLC1Label.grid(row = 0, column = 1, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # C2 - "Pozycja w wierszu"
        self.EPDLC2Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLC2Label.config(style = 'label1.TLabel')
        self.EPDLC2Label.config(justify = TK.CENTER)
        self.EPDLC2Label.config(text = 'Pozycja\nw wierszu')
        self.EPDLC2Label.grid(row = 0, column = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # W1 - "Login"
        self.EPDLW1Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW1Label.config(style = 'label1.TLabel')
        self.EPDLW1Label.config(text = 'Login')
        self.EPDLW1Label.grid(row = 1, column = 0, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja loginu (wiersz)
        self.EPDLLoginRowVar = TK.IntVar()
        self.EPDLLoginRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLoginRowSpinbox.config(textvariable = self.EPDLLoginRowVar)
        self.EPDLLoginRowSpinbox.config(from_ = 0)
        self.EPDLLoginRowSpinbox.config(to = 1000000)
        self.EPDLLoginRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLoginRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLoginRowSpinbox.grid(row = 1, column = 1, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja loginu (pozycja w wierszu)
        self.EPDLLoginPosInRowVar = TK.IntVar()
        self.EPDLLoginPosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLoginPosInRowSpinbox.config(textvariable = self.EPDLLoginPosInRowVar)
        self.EPDLLoginPosInRowSpinbox.config(from_ = 0)
        self.EPDLLoginPosInRowSpinbox.config(to = 1000000)
        self.EPDLLoginPosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLoginPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLoginPosInRowSpinbox.grid(row = 1, column = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # W2 - "Imię"
        self.EPDLW2Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW2Label.config(style = 'label1.TLabel')
        self.EPDLW2Label.config(text = 'Imię')
        self.EPDLW2Label.grid(row = 2, column = 0, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja imienia (wiersz)
        self.EPDLFnameRowVar = TK.IntVar()
        self.EPDLFnameRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLFnameRowSpinbox.config(textvariable = self.EPDLFnameRowVar)
        self.EPDLFnameRowSpinbox.config(from_ = 0)
        self.EPDLFnameRowSpinbox.config(to = 1000000)
        self.EPDLFnameRowSpinbox.config(state = TK.DISABLED)
        self.EPDLFnameRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLFnameRowSpinbox.grid(row = 2, column = 1, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja imienia (pozycja w wierszu)
        self.EPDLFnamePosInRowVar = TK.IntVar()
        self.EPDLFnamePosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLFnamePosInRowSpinbox.config(textvariable = self.EPDLFnamePosInRowVar)
        self.EPDLFnamePosInRowSpinbox.config(from_ = 0)
        self.EPDLFnamePosInRowSpinbox.config(to = 1000000)
        self.EPDLFnamePosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLFnamePosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLFnamePosInRowSpinbox.grid(row = 2, column = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # W3 - "Nazwisko"
        self.EPDLW3Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW3Label.config(style = 'label1.TLabel')
        self.EPDLW3Label.config(text = 'Nazwisko')
        self.EPDLW3Label.grid(row = 3, column = 0, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja nazwiska (wiersz)
        self.EPDLLnameRowVar = TK.IntVar()
        self.EPDLLnameRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLnameRowSpinbox.config(textvariable = self.EPDLLnameRowVar)
        self.EPDLLnameRowSpinbox.config(from_ = 0)
        self.EPDLLnameRowSpinbox.config(to = 1000000)
        self.EPDLLnameRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLnameRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLnameRowSpinbox.grid(row = 3, column = 1, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja nazwiska (pozycja w wierszu)
        self.EPDLLnamePosInRowVar = TK.IntVar()
        self.EPDLLnamePosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLnamePosInRowSpinbox.config(textvariable = self.EPDLLnamePosInRowVar)
        self.EPDLLnamePosInRowSpinbox.config(from_ = 0)
        self.EPDLLnamePosInRowSpinbox.config(to = 1000000)
        self.EPDLLnamePosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLnamePosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLnamePosInRowSpinbox.grid(row = 3, column = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # W4 - "Szkoła"
        self.EPDLW4Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW4Label.config(style = 'label1.TLabel')
        self.EPDLW4Label.config(text = 'Szkoła')
        self.EPDLW4Label.grid(row = 4, column = 0, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja nazwiska (wiersz)
        self.EPDLSchoolRowVar = TK.IntVar()
        self.EPDLSchoolRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLSchoolRowSpinbox.config(textvariable = self.EPDLSchoolRowVar)
        self.EPDLSchoolRowSpinbox.config(from_ = 0)
        self.EPDLSchoolRowSpinbox.config(to = 1000000)
        self.EPDLSchoolRowSpinbox.config(state = TK.DISABLED)
        self.EPDLSchoolRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLSchoolRowSpinbox.grid(row = 4, column = 1, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja nazwiska (pozycja w wierszu)
        self.EPDLSchoolPosInRowVar = TK.IntVar()
        self.EPDLSchoolPosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLSchoolPosInRowSpinbox.config(textvariable = self.EPDLSchoolPosInRowVar)
        self.EPDLSchoolPosInRowSpinbox.config(from_ = 0)
        self.EPDLSchoolPosInRowSpinbox.config(to = 1000000)
        self.EPDLSchoolPosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLSchoolPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLSchoolPosInRowSpinbox.grid(row = 4, column = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # W5 - "Klasa"
        self.EPDLW5Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW5Label.config(style = 'label1.TLabel')
        self.EPDLW5Label.config(text = 'Klasa')
        self.EPDLW5Label.grid(row = 5, column = 0, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        
        # Lokalizacja nazwiska (wiersz)
        self.EPDLClassRowVar = TK.IntVar()
        self.EPDLClassRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLClassRowSpinbox.config(textvariable = self.EPDLClassRowVar)
        self.EPDLClassRowSpinbox.config(from_ = 0)
        self.EPDLClassRowSpinbox.config(to = 1000000)
        self.EPDLClassRowSpinbox.config(state = TK.DISABLED)
        self.EPDLClassRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLClassRowSpinbox.grid(row = 5, column = 1, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))

        # Lokalizacja nazwiska (pozycja w wierszu)
        self.EPDLClassPosInRowVar = TK.IntVar()
        self.EPDLClassPosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLClassPosInRowSpinbox.config(textvariable = self.EPDLClassPosInRowVar)
        self.EPDLClassPosInRowSpinbox.config(from_ = 0)
        self.EPDLClassPosInRowSpinbox.config(to = 1000000)
        self.EPDLClassPosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLClassPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLClassPosInRowSpinbox.grid(row = 5, column = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))

        # Separator
        self.formatSeparator4Frame = TKttk.Frame(self.editingPresetDLFrame)
        self.formatSeparator4Frame.config(style = 'layoutFrame.TFrame')
        self.formatSeparator4Frame.grid(row = 6, column = 0, columnspan = 3)

        self.formatSeparator4 = TKttk.Separator(self.formatSeparator4Frame)
        self.formatSeparator4.config(style = 'separator1.TSeparator')
        self.formatSeparator4.config(orient = TK.HORIZONTAL)
        self.formatSeparator4.pack(padx = GUI.R('formatHorizontalSeparatorPadY'), pady = 10, fill = TK.X, expand = 1)

        # "Kodowanie"
        self.formatInputCodingLabel = TKttk.Label(self.editingPresetDLFrame)
        self.formatInputCodingLabel.config(style = 'label1.TLabel')
        self.formatInputCodingLabel.config(text = 'Kodowanie')
        self.formatInputCodingLabel.grid(row = 7, column = 0, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))

        # Kodowanie - Combobox
        self.formatInputCodingVar = TK.StringVar()
        self.formatInputCodingCombobox = TKttk.Combobox(self.editingPresetDLFrame)
        self.formatInputCodingCombobox.config(textvariable = self.formatInputCodingVar)
        self.formatInputCodingCombobox.config(state = TK.DISABLED)
        self.formatInputCodingCombobox.config(style = 'combobox2.TCombobox')
        self.formatInputCodingCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox2ListBoxBackground'))
        self.formatInputCodingCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox2ListBoxForeground'))
        self.formatInputCodingCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox2ListBoxSelectBackground'))
        self.formatInputCodingCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox2ListBoxSelectForeground'))
        self.formatInputCodingCombobox.grid(row = 7, column = 1, columnspan = 2, padx = GUI.R('EPDataLocalizationPadX'), pady = GUI.R('EPDataLocalizationPadY'))
        self.formatInputCodingCombobox['values'] = tuple(VAR.allowedCoding)

        ###############################

        #########################################

        ###################################################
        
        # (1) Separator 3 ###########################################

        self.formatSeparator3 = TKttk.Separator(self.formatFrame)
        self.formatSeparator3.config(style = 'separator1.TSeparator')
        self.formatSeparator3.config(orient = TK.HORIZONTAL)
        self.formatSeparator3.pack(fill = TK.X, pady = GUI.R('formatHorizontalSeparatorPadY'))

        #############################################################

        # (1) Przyciski #############################################

        self.editingPresetButtonsFrame = TKttk.Frame(self.formatFrame)
        self.editingPresetButtonsFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetButtonsFrame.pack(fill = TK.X, side = TK.BOTTOM, pady = GUI.R('editingPresetButtonsPadY'))

        # Przycisk 'ZAPISZ'
        self.editingPresetSaveButton = TKttk.Button(self.editingPresetButtonsFrame)
        self.editingPresetSaveButton.config(command = self.editingPresetSaveButtonAction)
        self.editingPresetSaveButton.config(state = TK.DISABLED)
        self.editingPresetSaveButton.config(style = 'button1.TButton')
        self.editingPresetSaveButton.config(width = GUI.R('editingPresetSaveButtonWidth'))
        self.editingPresetSaveButton.config(text = 'ZAPISZ')
        self.editingPresetSaveButton.pack(side = TK.LEFT, expand = 1)

        # Przycisk 'Anuluj'
        self.editingPresetCancelButton = TKttk.Button(self.editingPresetButtonsFrame)
        self.editingPresetCancelButton.config(command = self.editingPresetCancelButtonAction)
        self.editingPresetCancelButton.config(state = TK.DISABLED)
        self.editingPresetCancelButton.config(style = 'button1.TButton')
        self.editingPresetCancelButton.config(width = GUI.R('editingPresetCancelButtonWidth'))
        self.editingPresetCancelButton.config(text = 'Anuluj')
        self.editingPresetCancelButton.pack(side = TK.RIGHT, expand = 1)

        #############################################################

        ######################################################################




        # TAB3 - Ustawienia ##################################################

        self.settingsTab = TKttk.Frame(self.mainMenu)
        self.settingsTab.config(style = "mainMenuTabFrame.TFrame")
        self.settingsTabImg = PLimg.open(GUI.R('settingsTabIcon'))
        self.settingsTabImg = self.settingsTabImg.resize((GUI.R('tabIconsSize'), GUI.R('tabIconsSize')), PLimg.ANTIALIAS)
        self.settingsTabImg = PLitk.PhotoImage(self.settingsTabImg)
        self.mainMenu.add(self.settingsTab, image = self.settingsTabImg, state = TK.NORMAL)


        # Nagłówek
        self.settingsHeader = TKttk.Label(self.settingsTab)
        self.settingsHeader.config(style = 'tabHeader.TLabel')
        self.settingsHeader.config(text = 'USTAWIENIA')
        self.settingsHeader.pack(fill = GUI.R('headerFill'))


        # Zawartość
        self.settingsFrame = TKttk.Frame(self.settingsTab)
        self.settingsFrame.config(style = 'contentTabFrame.TFrame')
        self.settingsFrame.pack(fill = GUI.R('contentTabFrameFill'), expand = GUI.R('contentTabFrameExpand'), padx = GUI.R('tabFramePadding'), pady = GUI.R('tabFramePadding'))

        # (1) Ustwienia #############################################

        self.settingsMainFrame = TKttk.Frame(self.settingsFrame)
        self.settingsMainFrame.config(style = 'layoutFrame.TFrame')
        self.settingsMainFrame.pack(side = TK.TOP, fill = TK.BOTH, expand = 1)

        # (2) Po lewo #####################################

        self.settingsLeftFrame = TKttk.Frame(self.settingsMainFrame)
        self.settingsLeftFrame.config(style = 'layoutFrame.TFrame')
        self.settingsLeftFrame.pack(side = TK.LEFT, fill = TK.BOTH, expand = 1)

        # (3) Kodowanie #########################

        self.settingsCodeFrame = TKttk.Frame(self.settingsLeftFrame)
        self.settingsCodeFrame.config(style = 'layoutFrame.TFrame')
        self.settingsCodeFrame.pack(side = TK.TOP, fill = TK.X)

        # (4) Kodowanie dla pliku poczty

        self.settingsMailCodeFrame = TKttk.Frame(self.settingsCodeFrame)
        self.settingsMailCodeFrame.config(style = 'layoutFrame.TFrame')
        self.settingsMailCodeFrame.pack(side = TK.TOP, fill = TK.X, pady = 6, expand = 1)

        # 'Kodowanie wyjściowe dla pliku poczty'
        self.settingsMailCodeLabel = TKttk.Label(self.settingsMailCodeFrame)
        self.settingsMailCodeLabel.config(style = 'label1.TLabel')
        self.settingsMailCodeLabel.config(width = GUI.R('settingsCodeLabelWidth'))
        self.settingsMailCodeLabel.config(anchor = GUI.R('settingsCodeLabelAnchor'))
        self.settingsMailCodeLabel.config(text = 'Kodowanie wyjściowe dla pliku poczty')
        self.settingsMailCodeLabel.pack(side = TK.LEFT)

        # Kodowanie dla poczty - Combobox
        self.settingsMailCodeVar = TK.StringVar()
        self.settingsMailCodeCombobox = TKttk.Combobox(self.settingsMailCodeFrame)
        self.settingsMailCodeCombobox.config(textvariable = self.settingsMailCodeVar)
        self.settingsMailCodeCombobox.config(style = 'combobox2.TCombobox')
        self.settingsMailCodeCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox2ListBoxBackground'))
        self.settingsMailCodeCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox2ListBoxForeground'))
        self.settingsMailCodeCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox2ListBoxSelectBackground'))
        self.settingsMailCodeCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox2ListBoxSelectForeground'))
        self.settingsMailCodeCombobox.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        self.settingsMailCodeCombobox['values'] = tuple(VAR.allowedCoding)
        self.settingsMailCodeCombobox.set(CFG.R('mailOutputCoding'))

        ###############################

        # (4) Kodowanie dla pliku office

        self.settingsOfficeCodeFrame = TKttk.Frame(self.settingsCodeFrame)
        self.settingsOfficeCodeFrame.config(style = 'layoutFrame.TFrame')
        self.settingsOfficeCodeFrame.pack(side = TK.BOTTOM, fill = TK.X, pady = 6, expand = 1)

        # 'Kodowanie wyjściowe dla pliku office'
        self.settingsOfficeCodeLabel = TKttk.Label(self.settingsOfficeCodeFrame)
        self.settingsOfficeCodeLabel.config(style = 'label1.TLabel')
        self.settingsOfficeCodeLabel.config(width = GUI.R('settingsCodeLabelWidth'))
        self.settingsOfficeCodeLabel.config(anchor = GUI.R('settingsCodeLabelAnchor'))
        self.settingsOfficeCodeLabel.config(text = 'Kodowanie wyjściowe dla pliku office')
        self.settingsOfficeCodeLabel.pack(side = TK.LEFT)

        # Kodowanie dla poczty - Combobox
        self.settingsOfficeCodeVar = TK.StringVar()
        self.settingsOfficeCodeCombobox = TKttk.Combobox(self.settingsOfficeCodeFrame)
        self.settingsOfficeCodeCombobox.config(textvariable = self.settingsOfficeCodeVar)
        self.settingsOfficeCodeCombobox.config(style = 'combobox2.TCombobox')
        self.settingsOfficeCodeCombobox.option_add("*TCombobox*Listbox.background", GUI.R('combobox2ListBoxBackground'))
        self.settingsOfficeCodeCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R('combobox2ListBoxForeground'))
        self.settingsOfficeCodeCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R('combobox2ListBoxSelectBackground'))
        self.settingsOfficeCodeCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R('combobox2ListBoxSelectForeground'))
        self.settingsOfficeCodeCombobox.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        self.settingsOfficeCodeCombobox['values'] = tuple(VAR.allowedCoding)
        self.settingsOfficeCodeCombobox.set(CFG.R('officeOutputCoding'))

        ###############################

        #########################################

        # (3) Separator #########################

        self.settingsSeparator3 = TKttk.Separator(self.settingsLeftFrame)
        self.settingsSeparator3.config(style = 'separator1.TSeparator')
        self.settingsSeparator3.config(orient = TK.HORIZONTAL)
        self.settingsSeparator3.pack(fill = TK.X, pady = GUI.R('settingsHorizontalSeparatorPadY'))

        #########################################

        # (3) Inne dane #########################

        self.settingsOtherFrame = TKttk.Frame(self.settingsLeftFrame)
        self.settingsOtherFrame.config(style = 'layoutFrame.TFrame')
        self.settingsOtherFrame.pack(fill = TK.X)

        # (4) Domena ##################

        self.settingsOtherDomainFrame = TKttk.Frame(self.settingsOtherFrame)
        self.settingsOtherDomainFrame.config(style = 'layoutFrame.TFrame')
        self.settingsOtherDomainFrame.pack(fill = TK.X, pady = 6, expand = 1)

        # 'Domena (używana w mailu)'
        self.settingsOtherDomainLabel = TKttk.Label(self.settingsOtherDomainFrame)
        self.settingsOtherDomainLabel.config(style = 'label1.TLabel')
        self.settingsOtherDomainLabel.config(width = GUI.R('settingsOtherLabelWidth'))
        self.settingsOtherDomainLabel.config(anchor = GUI.R('settingsOtherLabelAnchor'))
        self.settingsOtherDomainLabel.config(text = 'Domena (używana w mailu)')
        self.settingsOtherDomainLabel.pack(side = TK.LEFT)

        # Domena - Entry
        self.settingsOtherDomainVar = TK.StringVar()
        self.settingsOtherDomainEntry = TKttk.Entry(self.settingsOtherDomainFrame)
        self.settingsOtherDomainEntry.config(style = 'entry1.TEntry')
        self.settingsOtherDomainEntry.config(textvariable = self.settingsOtherDomainVar)
        self.settingsOtherDomainEntry.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        self.settingsOtherDomainVar.set(CFG.R('domain'))

        ###############################

        # (4) Quota ###################

        self.settingsOtherQuotaFrame = TKttk.Frame(self.settingsOtherFrame)
        self.settingsOtherQuotaFrame.config(style = 'layoutFrame.TFrame')
        self.settingsOtherQuotaFrame.pack(fill = TK.X, pady = 6, expand = 1)

        # 'Quota (MB)'
        self.settingsOtherQuotaLabel = TKttk.Label(self.settingsOtherQuotaFrame)
        self.settingsOtherQuotaLabel.config(style = 'label1.TLabel')
        self.settingsOtherQuotaLabel.config(width = GUI.R('settingsOtherLabelWidth'))
        self.settingsOtherQuotaLabel.config(anchor = GUI.R('settingsOtherLabelAnchor'))
        self.settingsOtherQuotaLabel.config(text = 'Quota (MB)')
        self.settingsOtherQuotaLabel.pack(side = TK.LEFT)

        # Domena - Entry
        self.settingsOtherQuotaVar = TK.IntVar()
        self.settingsOtherQuotaSpinbox = TKttk.Spinbox(self.settingsOtherQuotaFrame)
        self.settingsOtherQuotaSpinbox.config(textvariable = self.settingsOtherQuotaVar)
        self.settingsOtherQuotaSpinbox.config(from_ = 0)
        self.settingsOtherQuotaSpinbox.config(to = 10000000000000000000000)
        self.settingsOtherQuotaSpinbox.config(style = 'spinbox1.TSpinbox')
        self.settingsOtherQuotaSpinbox.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        self.settingsOtherQuotaSpinbox.set(CFG.R('quota'))

        ###############################

        # (4) Kraj ##################

        self.settingsOtherCountryFrame = TKttk.Frame(self.settingsOtherFrame)
        self.settingsOtherCountryFrame.config(style = 'layoutFrame.TFrame')
        self.settingsOtherCountryFrame.pack(fill = TK.X, pady = 6, expand = 1)

        # 'Kraj (zapisany w danych na office)'
        self.settingsOtherCountryLabel = TKttk.Label(self.settingsOtherCountryFrame)
        self.settingsOtherCountryLabel.config(style = 'label1.TLabel')
        self.settingsOtherCountryLabel.config(width = GUI.R('settingsOtherLabelWidth'))
        self.settingsOtherCountryLabel.config(anchor = GUI.R('settingsOtherLabelAnchor'))
        self.settingsOtherCountryLabel.config(text = 'Kraj (zapisany w danych na office)')
        self.settingsOtherCountryLabel.pack(side = TK.LEFT)

        # Domena - Entry
        self.settingsOtherCountryVar = TK.StringVar()
        self.settingsOtherCountryEntry = TKttk.Entry(self.settingsOtherCountryFrame)
        self.settingsOtherCountryEntry.config(style = 'entry1.TEntry')
        self.settingsOtherCountryEntry.config(textvariable = self.settingsOtherCountryVar)
        self.settingsOtherCountryEntry.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        self.settingsOtherCountryVar.set(CFG.R('country'))

        ###############################

        # (4) Rozpoczęcir roku szkolnego

        self.settingsOtherDRRSFrame = TKttk.Frame(self.settingsOtherFrame)
        self.settingsOtherDRRSFrame.config(style = 'layoutFrame.TFrame')
        self.settingsOtherDRRSFrame.pack(fill = TK.X, expand = 1, pady = 6)

        # 'Rozpoczęcie roku szkolnego (Dzień | Miesiąc)'
        self.settingsOtherDRRSLabel = TKttk.Label(self.settingsOtherDRRSFrame)
        self.settingsOtherDRRSLabel.config(style = 'label1.TLabel')
        self.settingsOtherDRRSLabel.config(width = GUI.R('settingsOtherLabelWidth'))
        self.settingsOtherDRRSLabel.config(anchor = GUI.R('settingsOtherLabelAnchor'))
        self.settingsOtherDRRSLabel.config(text = 'Rozpoczęcie roku szkolnego (DD | MM)')
        self.settingsOtherDRRSLabel.pack(side = TK.LEFT)

        # Rozpoczęcie roku szkolnego - Miesiąc
        self.settingsOtherDRRSMonthVar = TK.IntVar()
        self.settingsOtherDRRSMonthSpinbox = TKttk.Spinbox(self.settingsOtherDRRSFrame)
        self.settingsOtherDRRSMonthSpinbox.config(textvariable = self.settingsOtherDRRSMonthVar)
        self.settingsOtherDRRSMonthSpinbox.config(from_ = 1)
        self.settingsOtherDRRSMonthSpinbox.config(to = 12)
        self.settingsOtherDRRSMonthSpinbox.config(style = 'spinbox1.TSpinbox')
        self.settingsOtherDRRSMonthSpinbox.pack(side = TK.RIGHT, fill = TK.X, expand = 1, padx = (6, 0))
        self.settingsOtherDRRSMonthSpinbox.set(CFG.R('schoolyearStart')['M'])

        # Rozpoczęcie roku szkolnego - Dzień
        self.settingsOtherDRRSDayVar = TK.IntVar()
        self.settingsOtherDRRSDaySpinbox = TKttk.Spinbox(self.settingsOtherDRRSFrame)
        self.settingsOtherDRRSDaySpinbox.config(textvariable = self.settingsOtherDRRSDayVar)
        self.settingsOtherDRRSDaySpinbox.config(from_ = 1)
        self.settingsOtherDRRSDaySpinbox.config(to = 31)
        self.settingsOtherDRRSDaySpinbox.config(style = 'spinbox1.TSpinbox')
        self.settingsOtherDRRSDaySpinbox.pack(side = TK.RIGHT, fill = TK.X, expand = 1, padx = (0, 6))
        self.settingsOtherDRRSDaySpinbox.set(CFG.R('schoolyearStart')['D'])

        ###############################

        #########################################

        ###################################################

        # (2) Separator ###################################

        self.settingsSeparator2 = TKttk.Separator(self.settingsMainFrame)
        self.settingsSeparator2.config(style = 'separator1.TSeparator')
        self.settingsSeparator2.config(orient = TK.VERTICAL)
        self.settingsSeparator2.pack(side = TK.LEFT, fill = TK.Y, padx = GUI.R('settingsVerticalSeparatorPadY'))

        ###################################################

        # (2) Dane o szkołach #############################

        self.settingsSchoolDataFrame = TKttk.Frame(self.settingsMainFrame)
        self.settingsSchoolDataFrame.config(style = 'layoutFrame.TFrame')
        self.settingsSchoolDataFrame.pack(side = TK.RIGHT, fill = TK.BOTH)

        # 'Dane o szkołach'
        self.settingsSchoolDataLabel = TKttk.Label(self.settingsSchoolDataFrame)
        self.settingsSchoolDataLabel.config(style = 'label1.TLabel')
        self.settingsSchoolDataLabel.config(anchor = GUI.R('settingsSchoolDataLabelAnchor'))
        self.settingsSchoolDataLabel.config(text = 'Dane o szkołach')
        self.settingsSchoolDataLabel.pack(side = TK.TOP, pady = 6)

        # Label - oznaczenia kolumn
        self.settingsSchoolDataInstructionLabel = TKttk.Label(self.settingsSchoolDataFrame)
        self.settingsSchoolDataInstructionLabel.config(style = 'label3.TLabel')
        self.settingsSchoolDataInstructionLabel.config(anchor = GUI.R('settingsSchoolDataLabelAnchor'))
        self.settingsSchoolDataInstructionLabel.config(text = 'OZNACZENIE SZKOŁY | ILOŚĆ KLAS | CZY OZNACZENIE SZKOŁY W ZNACZNIKU KLASY? (0/1)')
        self.settingsSchoolDataInstructionLabel.pack()

        # Dane o szkołach - Text
        self.settingsSchoolDataText = TK.Text(self.settingsSchoolDataFrame)
        self.settingsSchoolDataText.config(background = GUI.R('text1Background'))
        self.settingsSchoolDataText.config(foreground = GUI.R('text1TextColor'))
        self.settingsSchoolDataText.config(relief = GUI.R('text1Relief'))
        self.settingsSchoolDataText.config(width = 50)
        self.settingsSchoolDataText.pack(pady = 6, fill = TK.Y, expand = 1)
        for x in CFG.R('schoolData'):
            if x[2]:
                x[2] = '1'
            else:
                x[2] = '0'
            x[1] = str(x[1])
            self.settingsSchoolDataText.insert(TK.END, (' | '.join(x) + '\n'))

        ###################################################

        #############################################################
        
        # (1) Separator #############################################

        self.settingsSeparator1 = TKttk.Separator(self.settingsFrame)
        self.settingsSeparator1.config(style = 'separator1.TSeparator')
        self.settingsSeparator1.config(orient = TK.HORIZONTAL)
        self.settingsSeparator1.pack(fill = TK.X, pady = GUI.R('settingsHorizontalSeparatorPadY'))

        #############################################################

        # (1) Przyciski #############################################

        self.settingsButtonsFrame = TKttk.Frame(self.settingsFrame)
        self.settingsButtonsFrame.config(style = 'layoutFrame.TFrame')
        self.settingsButtonsFrame.pack(side = TK.BOTTOM, fill = TK.X, pady = GUI.R('settingsButtonsPadY'))

        # (2) Przyciski ZAPISZ i Anuluj ###################

        self.settingsButtonsSaveCancelFrame = TKttk.Frame(self.settingsButtonsFrame)
        self.settingsButtonsSaveCancelFrame.config(style = 'layoutFrame.TFrame')
        self.settingsButtonsSaveCancelFrame.pack(side = TK.LEFT)

        # Przycisk ZAPISZ
        self.settingsButtonSave = TKttk.Button(self.settingsButtonsSaveCancelFrame)
        self.settingsButtonSave.config(command = self.settingsButtonSaveAction)
        self.settingsButtonSave.config(style = 'button1.TButton')
        self.settingsButtonSave.config(width = GUI.R('settingsButtonSaveWidth'))
        self.settingsButtonSave.config(text = 'ZAPISZ')
        self.settingsButtonSave.pack(side = TK.LEFT, padx = 6)

        # Przycisk Anuluj
        self.settingsButtonCancel = TKttk.Button(self.settingsButtonsSaveCancelFrame)
        self.settingsButtonCancel.config(command = self.settingsButtonCancelAction)
        self.settingsButtonCancel.config(style = 'button1.TButton')
        self.settingsButtonCancel.config(width = GUI.R('settingsButtonCancelWidth'))
        self.settingsButtonCancel.config(text = 'Anuluj')
        self.settingsButtonCancel.pack(side = TK.RIGHT, padx = 6)

        ###################################################

        # (2) Inne przyciski ##############################

        self.settingsButtonsOtherFrame = TKttk.Frame(self.settingsButtonsFrame)
        self.settingsButtonsOtherFrame.config(style = 'layoutFrame.TFrame')
        self.settingsButtonsOtherFrame.pack(side = TK.RIGHT)

        # Przycisk "Zarządzaj presetami formatu"
        self.settingsButtonZPF = TKttk.Button(self.settingsButtonsOtherFrame)
        self.settingsButtonZPF.config(command = self.settingsButtonZPFAction)
        self.settingsButtonZPF.config(style = 'button1.TButton')
        self.settingsButtonZPF.config(width = GUI.R('settingsButtonZPFWidth'))
        self.settingsButtonZPF.config(text = 'Zarządzaj presetami formatu')
        self.settingsButtonZPF.pack(side = TK.RIGHT, padx = 6)

        # Przycisk "Przywróć domyślne ustawienia wyglądu"
        self.settingsButtonPDUW = TKttk.Button(self.settingsButtonsOtherFrame)
        self.settingsButtonPDUW.config(command = self.settingsButtonPDUWAction)
        self.settingsButtonPDUW.config(style = 'button1.TButton')
        self.settingsButtonPDUW.config(width = GUI.R('settingsButtonPDUWWidth'))
        self.settingsButtonPDUW.config(text = 'Przywróć domyślne ustawienia wyglądu')
        self.settingsButtonPDUW.pack(side = TK.RIGHT, padx = 6)

        # Przycisk "Przywróć domyślne ustwienia ogólne"
        self.settingsButtonPDUO = TKttk.Button(self.settingsButtonsOtherFrame)
        self.settingsButtonPDUO.config(command = self.settingsButtonPDUOAction)
        self.settingsButtonPDUO.config(style = 'button1.TButton')
        self.settingsButtonPDUO.config(width = GUI.R('settingsButtonPDUOWidth'))
        self.settingsButtonPDUO.config(text = 'Przywróć domyślne ustawienia ogólne')
        self.settingsButtonPDUO.pack(side = TK.RIGHT, padx = 6)

        ###################################################

        #############################################################

        ######################################################################




        # TAB4 - O programie #################################################
        
        self.aboutTab = TKttk.Frame(self.mainMenu)
        self.aboutTab.config(style = "mainMenuTabFrame.TFrame")
        self.aboutTabImg = PLimg.open(GUI.R('aboutTabIcon'))
        self.aboutTabImg = self.aboutTabImg.resize((GUI.R('tabIconsSize'), GUI.R('tabIconsSize')), PLimg.ANTIALIAS)
        self.aboutTabImg = PLitk.PhotoImage(self.aboutTabImg)
        self.mainMenu.add(self.aboutTab, image = self.aboutTabImg, state = TK.NORMAL)


        # Nagłówek
        self.aboutHeader = TKttk.Label(self.aboutTab)
        self.aboutHeader.config(style = 'tabHeader.TLabel')
        self.aboutHeader.config(text = 'O PROGRAMIE')
        self.aboutHeader.pack(fill = GUI.R('headerFill'))


        # Zawartość
        self.aboutFrame = TKttk.Frame(self.aboutTab)
        self.aboutFrame.config(style = 'contentTabFrame.TFrame')
        self.aboutFrame.pack(fill = GUI.R('contentTabFrameFill'), expand = GUI.R('contentTabFrameExpand'), padx = GUI.R('tabFramePadding'), pady = GUI.R('tabFramePadding'))

        # (1) Info & Logo ###########################################

        self.aboutInfoLogoFrame = TKttk.Frame(self.aboutFrame)
        self.aboutInfoLogoFrame.config(style = 'layoutFrame.TFrame')
        self.aboutInfoLogoFrame.pack(fill = TK.BOTH, expand = 1)

        # (2) Logo ########################################

        self.aboutLogoFrame = TKttk.Frame(self.aboutInfoLogoFrame)
        self.aboutLogoFrame.config(style = 'layoutFrame.TFrame')
        self.aboutLogoFrame.pack(fill = TK.BOTH, expand = 1)

        # Logo - Button
        self.aboutLogoButton = TKttk.Button(self.aboutLogoFrame)
        self.aboutLogoButton.config(style = 'button2.TButton')
        self.aboutLogoButtonImg = PLimg.open(GUI.R('aboutLogoButtonImg'))
        self.aboutLogoButtonImg = self.aboutLogoButtonImg.resize((GUI.R('aboutLogoButtonImgSize'), GUI.R('aboutLogoButtonImgSize')), PLimg.ANTIALIAS)
        self.aboutLogoButtonImg = PLitk.PhotoImage(self.aboutLogoButtonImg)
        self.aboutLogoButton.config(image = self.aboutLogoButtonImg)
        self.aboutLogoButton.pack(expand = 1)

        ###################################################

        # (2) Informacje ##################################

        self.aboutInfoFrame = TKttk.Frame(self.aboutInfoLogoFrame)
        self.aboutInfoFrame.config(style = 'layoutFrame.TFrame')
        self.aboutInfoFrame.pack(fill = TK.BOTH, expand = 1)

        # Nazwa programu
        self.aboutInfoProgramNameLabel = TKttk.Label(self.aboutInfoFrame)
        self.aboutInfoProgramNameLabel.config(style = 'label4.TLabel')
        self.aboutInfoProgramNameLabel.config(text = VAR.programName)
        self.aboutInfoProgramNameLabel.pack()

        # Wersja programu
        self.aboutInfoProgramNameLabel = TKttk.Label(self.aboutInfoFrame)
        self.aboutInfoProgramNameLabel.config(style = 'label1.TLabel')
        self.aboutInfoProgramNameLabel.config(text = 'Wersja %s %s (Build %s)' % (VAR.programVersion, VAR.programVersionStage, VAR.programVersionBuild))
        self.aboutInfoProgramNameLabel.pack()

        # (3) Pozostałe informacje ##############

        self.aboutOtherInfoFrame = TKttk.Frame(self.aboutInfoFrame)
        self.aboutOtherInfoFrame.config(style = 'layoutFrame.TFrame')
        self.aboutOtherInfoFrame.pack(pady = GUI.R('aboutOtherInfoFramePadX'))

        # Czas pracy
        self.aboutOIToWLabel = TKttk.Label(self.aboutOtherInfoFrame)
        self.aboutOIToWLabel.config(style = 'label2.TLabel')
        self.aboutOIToWLabel.config(text = '© %s %s - %s %s' % (VAR.programToW[0], VAR.programToW[1], VAR.programToW[2], VAR.programToW[3]))
        self.aboutOIToWLabel.pack()

        # Autorzy
        self.aboutOIAuthorsLabel = TKttk.Label(self.aboutOtherInfoFrame)
        self.aboutOIAuthorsLabel.config(style = 'label2.TLabel')
        self.aboutOIAuthorsLabel.config(text = '\n'.join(VAR.programAuthors))
        self.aboutOIAuthorsLabel.pack()

        # Dla kogo
        self.aboutOICustomerLabel = TKttk.Label(self.aboutOtherInfoFrame)
        self.aboutOICustomerLabel.config(style = 'label2.TLabel')
        self.aboutOICustomerLabel.config(text = 'dla %s' % VAR.programCustomer)
        self.aboutOICustomerLabel.pack()

        #########################################

        ###################################################

        #############################################################

        # (1) Instrukcja ############################################

        self.aboutInstructionFrame = TKttk.Frame(self.aboutFrame)
        self.aboutInstructionFrame.config(style = 'layoutFrame.TFrame')
        self.aboutInstructionFrame.pack(fill = TK.X, side = TK.BOTTOM)

        # Instrukcja - Button
        self.aboutInstructionButton = TKttk.Button(self.aboutInstructionFrame)
        self.aboutInstructionButton.config(command = self.aboutInstructionButtonAction)
        self.aboutInstructionButton.config(style = 'button1.TButton')
        self.aboutInstructionButton.config(width = GUI.R('aboutInstructionButtonWidth'))
        self.aboutInstructionButton.config(text = 'Instrukcja')
        self.aboutInstructionButton.pack(side = TK.RIGHT)

        #############################################################

        ######################################################################
        


    # Akcje przycisków - TAB1

    def GIF1SLocalizationButtonAction(self):
        filename = str(TKfld.askopenfilename(initialdir = '/', title = "Wybierz plik z danymi"))
        self.GIF1SLocalizationEntryVar.set(filename)

    def GIF2SLocalizationButtonAction(self):
        filename = str(TKfld.askopenfilename(initialdir = '/', title = "Wybierz plik z danymi"))
        self.GIF2SLocalizationEntryVar.set(filename)
    
    def GIF3SLocalizationButtonAction(self):
        filename = str(TKfld.askopenfilename(initialdir = '/', title = "Wybierz plik z danymi"))
        self.GIF3SLocalizationEntryVar.set(filename)

    def GIF4SLocalizationButtonAction(self):
        filename = str(TKfld.askopenfilename(initialdir = '/', title = "Wybierz plik z danymi"))
        self.GIF4SLocalizationEntryVar.set(filename)

    def GOFMailButtonAction(self):
        filename = str(TKfld.asksaveasfilename(initialdir = '/', title = "Wybierz miejsce zapisu pliku csv dla poczty", filetypes = [('Plik CSV', '*.csv')]))
        if not filename:
            return
        if not filename.endswith('.csv'):
            filename += '.csv'
        self.GOFMailEntryVar.set(filename)

    def GOFOfficeButtonAction(self):
        filename = str(TKfld.asksaveasfilename(initialdir = '/', title = "Wybierz miejsce zapisu pliku csv dla Office", filetypes = [('Plik CSV', '*.csv')]))
        if not filename:
            return
        if not filename.endswith('.csv'):
            filename += '.csv'
        self.GOFOfficeEntryVar.set(filename)

    def generateStartButtonAction(self):
        if MSG('A0003', False):
            GIF1SFilename = self.GIF1SLocalizationEntryVar.get()
            GIF1SFormat = self.GIF1SFormatComboboxVar.get()
            GIF2SFilename = self.GIF2SLocalizationEntryVar.get()
            GIF2SFormat = self.GIF2SFormatComboboxVar.get()
            GIF3SFilename = self.GIF3SLocalizationEntryVar.get()
            GIF3SFormat = self.GIF3SFormatComboboxVar.get()
            GIF4SFilename = self.GIF4SLocalizationEntryVar.get()
            GIF4SFormat = self.GIF4SFormatComboboxVar.get()
            GOFMailFilename = self.GOFMailEntryVar.get()
            GOFOfficeFilename = self.GOFOfficeEntryVar.get()
            GIF1 = (GIF1SFilename, GIF1SFormat)
            GIF2 = (GIF2SFilename, GIF2SFormat)
            GIF3 = (GIF3SFilename, GIF3SFormat)
            GIF4 = (GIF4SFilename, GIF4SFormat)
            GOF = (GOFMailFilename, GOFOfficeFilename)
            filesList = (GIF1, GIF2, GIF3, GIF4, GOF)
            output = dataProcess.start(filesList)
            if not output[0]:
                MSG('E0007', False)
            else:
                if not output[1]:
                    MSG('E0008', False)
                else:
                    if not output[2]:
                        MSG('E0009', False)
                    else:
                        if not output[3]:
                            MSG('E0010', False)
                        else:
                            if not (output[4])[0]:
                                MSG('E0011', False, (output[4])[1])
                            else:
                                if not output[5]:
                                    MSG('E0012', False)
                                else:
                                    if not output[6]:
                                        MSG('E0013', False)
                                    else:
                                        if not output[7]:
                                            MSG('E0014', False)
                                        else:
                                            MSG('I0001', False)
                                            self.GIF1SLocalizationEntryVar.set('')
                                            self.GIF1SFormatComboboxVar.set('')
                                            self.GIF2SLocalizationEntryVar.set('')
                                            self.GIF2SFormatComboboxVar.set('')
                                            self.GIF3SLocalizationEntryVar.set('')
                                            self.GIF3SFormatComboboxVar.set('')
                                            self.GIF4SLocalizationEntryVar.set('')
                                            self.GIF4SFormatComboboxVar.set('')
                                            self.GOFMailEntryVar.set('')
                                            self.GOFOfficeEntryVar.set('')

        else:
            return
        
    # Akcje przycisków - TAB2

    def loadingButtonAction(self):
        self.loadingList['state'] = TK.DISABLED
        self.loadingButton['state'] = TK.DISABLED
        self.EPOSTypeVar.set(FMT.R(self.loadingList.get(), 'student'))
        self.EPOSTypeStudentRadiobutton['state'] = TK.NORMAL
        self.EPOSTypeTeacherRadiobutton['state'] = TK.NORMAL
        self.EPOSPersonSeparatorEntry['state'] = TK.NORMAL
        self.EPOSPersonSeparatorVar.set(FMT.R(self.loadingList.get(), 'personSeparator'))
        self.EPOSRowSeparatorEntry['state'] = TK.NORMAL
        self.EPOSRowSeparatorVar.set(FMT.R(self.loadingList.get(), 'rowSeparator'))
        self.EPOSDataSeparatorText['state'] = TK.NORMAL
        self.EPOSDataSeparatorText.insert(TK.END, '\n'.join(FMT.R(self.loadingList.get(), 'dataSeparators')))
        self.EPDLLoginRowSpinbox['state'] = TK.NORMAL
        self.EPDLLoginRowVar.set(FMT.R(self.loadingList.get(), 'loginRow'))
        self.EPDLLoginPosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLLoginPosInRowVar.set(FMT.R(self.loadingList.get(), 'loginPositionInRow'))
        self.EPDLFnameRowSpinbox['state'] = TK.NORMAL
        self.EPDLFnameRowVar.set(FMT.R(self.loadingList.get(), 'fnameRow'))
        self.EPDLFnamePosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLFnamePosInRowVar.set(FMT.R(self.loadingList.get(), 'fnamePositionInRow'))
        self.EPDLLnameRowSpinbox['state'] = TK.NORMAL
        self.EPDLLnameRowVar.set(FMT.R(self.loadingList.get(), 'lnameRow'))
        self.EPDLLnamePosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLLnamePosInRowVar.set(FMT.R(self.loadingList.get(), 'lnamePositionInRow'))
        self.EPDLSchoolRowSpinbox['state'] = TK.NORMAL
        self.EPDLSchoolRowVar.set(FMT.R(self.loadingList.get(), 'schoolRow'))
        self.EPDLSchoolPosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLSchoolPosInRowVar.set(FMT.R(self.loadingList.get(), 'schoolPositionInRow'))
        self.EPDLClassRowSpinbox['state'] = TK.NORMAL
        self.EPDLClassRowVar.set(FMT.R(self.loadingList.get(), 'classRow'))
        self.EPDLClassPosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLClassPosInRowVar.set(FMT.R(self.loadingList.get(), 'classPositionInRow'))
        self.formatInputCodingCombobox['state'] = 'readonly'
        self.formatInputCodingVar.set(FMT.R(self.loadingList.get(), 'inputCoding'))
        self.editingPresetSaveButton['state'] = TK.NORMAL
        self.editingPresetCancelButton['state'] = TK.NORMAL

    def editingPresetClear(self):
        formatFileContent = {
            "student" : True,
            "personSeparator" : '',
            "rowSeparator" : '',
            "dataSeparators" : [],
            "loginRow" : 0,
            "loginPositionInRow" : 0,
            "fnameRow" : 0,
            "fnamePositionInRow" : 0,
            "lnameRow" : 0,
            "lnamePositionInRow" : 0,
            "schoolRow" : 0,
            "schoolPositionInRow" : 0,
            "classRow" : 0,
            "classPositionInRow" : 0,
            "inputCoding" : '',
        }
        self.loadingList['state'] = TK.NORMAL
        self.loadingButton['state'] = TK.NORMAL
        self.EPOSTypeVar.set(formatFileContent['student'])
        self.EPOSTypeStudentRadiobutton['state'] = TK.DISABLED
        self.EPOSTypeTeacherRadiobutton['state'] = TK.DISABLED
        self.EPOSPersonSeparatorEntry['state'] = TK.DISABLED
        self.EPOSPersonSeparatorVar.set(formatFileContent['personSeparator'])
        self.EPOSRowSeparatorEntry['state'] = TK.DISABLED
        self.EPOSRowSeparatorVar.set(formatFileContent['rowSeparator'])
        self.EPOSDataSeparatorText.delete('1.0', TK.END)
        self.EPOSDataSeparatorText['state'] = TK.DISABLED
        self.EPDLLoginRowSpinbox['state'] = TK.DISABLED
        self.EPDLLoginRowVar.set(formatFileContent['loginRow'])
        self.EPDLLoginPosInRowSpinbox['state'] = TK.DISABLED
        self.EPDLLoginPosInRowVar.set(formatFileContent['loginPositionInRow'])
        self.EPDLFnameRowSpinbox['state'] = TK.DISABLED
        self.EPDLFnameRowVar.set(formatFileContent['fnameRow'])
        self.EPDLFnamePosInRowSpinbox['state'] = TK.DISABLED
        self.EPDLFnamePosInRowVar.set(formatFileContent['fnamePositionInRow'])
        self.EPDLLnameRowSpinbox['state'] = TK.DISABLED
        self.EPDLLnameRowVar.set(formatFileContent['lnameRow'])
        self.EPDLLnamePosInRowSpinbox['state'] = TK.DISABLED
        self.EPDLLnamePosInRowVar.set(formatFileContent['lnamePositionInRow'])
        self.EPDLSchoolRowSpinbox['state'] = TK.DISABLED
        self.EPDLSchoolRowVar.set(formatFileContent['schoolRow'])
        self.EPDLSchoolPosInRowSpinbox['state'] = TK.DISABLED
        self.EPDLSchoolPosInRowVar.set(formatFileContent['schoolPositionInRow'])
        self.EPDLClassRowSpinbox['state'] = TK.DISABLED
        self.EPDLClassRowVar.set(formatFileContent['classRow'])
        self.EPDLClassPosInRowSpinbox['state'] = TK.DISABLED
        self.EPDLClassPosInRowVar.set(formatFileContent['classPositionInRow'])
        self.formatInputCodingCombobox['state'] = TK.DISABLED
        self.formatInputCodingVar.set(formatFileContent['inputCoding'])
        self.editingPresetSaveButton['state'] = TK.DISABLED
        self.editingPresetCancelButton['state'] = TK.DISABLED
        self.loadingList['values'] = tuple(FMT.getList())
    
    def updatePresetListInGenerateTab(self):
        self.GIF1SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF2SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF3SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF4SFormatCombobox['values'] = tuple(FMT.getList())

    def editingPresetSave(self):
        formatFileContentToSave = {
            "student" : self.EPOSTypeVar.get(),
            "personSeparator" : self.EPOSPersonSeparatorEntry.get(),
            "rowSeparator" : self.EPOSRowSeparatorEntry.get(),
            "dataSeparators" : (self.EPOSDataSeparatorText.get("1.0", TK.END)).split('\n')[:-1],
            "loginRow" : self.EPDLLoginRowSpinbox.get(),
            "loginPositionInRow" : self.EPDLLoginPosInRowSpinbox.get(),
            "fnameRow" : self.EPDLFnameRowSpinbox.get(),
            "fnamePositionInRow" : self.EPDLFnamePosInRowSpinbox.get(),
            "lnameRow" : self.EPDLLnameRowSpinbox.get(),
            "lnamePositionInRow" : self.EPDLLnamePosInRowSpinbox.get(),
            "schoolRow" : self.EPDLSchoolRowSpinbox.get(),
            "schoolPositionInRow" : self.EPDLSchoolPosInRowSpinbox.get(),
            "classRow" : self.EPDLClassRowSpinbox.get(),
            "classPositionInRow" : self.EPDLClassPosInRowSpinbox.get(),
            "inputCoding" : self.formatInputCodingCombobox.get()
        }
        if not FMT.W(self.loadingList.get(), formatFileContentToSave):
            return
        self.editingPresetClear()
        self.updatePresetListInGenerateTab()

    def editingPresetSaveButtonAction(self):
        if self.loadingList.get() not in FMT.getList():
            if MSG('A0001', False):
                self.editingPresetSave()
            else:
                return
        else:
            if MSG('A0002', False):
                self.editingPresetSave()
            else:
                return

    def editingPresetCancelButtonAction(self):
        self.editingPresetClear()
    
    # Akcje przycisków - TAB3

    def settingsReset(self):
        self.settingsMailCodeCombobox.set(CFG.R('mailOutputCoding'))
        self.settingsOfficeCodeCombobox.set(CFG.R('officeOutputCoding'))
        self.settingsOtherDomainVar.set(CFG.R('domain'))
        self.settingsOtherQuotaSpinbox.set(CFG.R('quota'))
        self.settingsOtherCountryVar.set(CFG.R('country'))
        self.settingsOtherDRRSMonthSpinbox.set(CFG.R('schoolyearStart')['M'])
        self.settingsOtherDRRSDaySpinbox.set(CFG.R('schoolyearStart')['D'])
        self.settingsSchoolDataText.delete('1.0', TK.END)
        for x in CFG.R('schoolData'):
            if x[2]:
                x[2] = '1'
            else:
                x[2] = '0'
            x[1] = str(x[1])
            self.settingsSchoolDataText.insert(TK.END, (' | '.join(x) + '\n'))

    def settingsButtonSaveAction(self):
        if MSG('A0004', False):
            changes = {}
            changes['mailOutputCoding'] = self.settingsMailCodeCombobox.get()
            changes['officeOutputCoding'] = self.settingsOfficeCodeCombobox.get()
            changes['domain'] = self.settingsOtherDomainVar.get()
            changes['quota'] = self.settingsOtherQuotaSpinbox.get()
            changes['country'] = self.settingsOtherCountryVar.get()
            changes['schoolyearStart'] = {
                'D' : self.settingsOtherDRRSDaySpinbox.get(),
                'M' : self.settingsOtherDRRSMonthSpinbox.get(),
                'Y' : None,
                'h' : None,
                'm' : None,
                's' : None,
            }
            changes['schoolData'] = (self.settingsSchoolDataText.get("1.0", TK.END)).split('\n')
            CFG.W(changes)
            self.settingsReset()
        else:
            return

    def settingsButtonCancelAction(self):
        self.settingsReset()

    def settingsButtonPDUOAction(self):
        if MSG('A0005', False):
            try:
                OS.remove(str(appdata) + '\Generator CSV\config.cfg')
                SU.copy('configs/config.cfg', str(appdata) + '\Generator CSV\config.cfg')
            except Exception as exceptInfo:
                MSG('E0001', True, exceptInfo)
            MSG('I0002', True)
        else:
            return

    def settingsButtonPDUWAction(self):
        if MSG('A0006', False):
            try:
                OS.remove(str(appdata) + '\Generator CSV\style.cfg')
                SU.copy('configs/style.cfg', str(appdata) + '\Generator CSV\style.cfg')
            except Exception as exceptInfo:
                MSG('E0001', True, exceptInfo)
            MSG('I0002', True)
        else:
            return
    
    def deleteSelectedFPButtonAction(self):
        if MSG('A0007', False):
            selected = self.selectFPListbox.curselection()
            for x in selected:
                try:
                    OS.remove(str(appdata) + ('/Generator CSV/format-presets') + ('\%s.fmt' % self.selectFPListbox.get(x)))
                except Exception as exceptInfo:
                    MSG('E0015', True, exceptInfo)
            MSG('I0001', False)
            self.updatePresetListInGenerateTab()
            self.loadingList['values'] = tuple(FMT.getList())
            self.selectFPListbox.delete(0, TK.END)
            for x in FMT.getList():
                self.selectFPListbox.insert(TK.END, x)
        else:
            return

    def settingsButtonZPFAction(self):
        # Pod okno
        self.ZPFWindow = TK.Toplevel(self.master)
        self.ZPFWindow.title("Zarządzanie presetami formatu")
        self.ZPFWindow.geometry('%ix%i' % (GUI.R('ZPFWindowWidth'), GUI.R('ZPFWindowHeight')))
        self.ZPFWindow.resizable(width = GUI.R('ZPFWindowWidthResizable'), height = GUI.R('ZPFWindowHeightResizable'))
        self.ZPFWindow.configure(bg = GUI.R('ZPFWindowMainBG'))
        self.ZPFWindow.iconbitmap(GUI.R('mainIcon'))

        # Wybór format presetu - listbox
        self.selectFPListbox = TK.Listbox(self.ZPFWindow)
        self.selectFPListbox.config(activestyle = GUI.R('listbox1ActiveStyle'))
        self.selectFPListbox.config(bg = GUI.R('listbox1BG'))
        self.selectFPListbox.config(fg = GUI.R('listbox1TextColor'))
        self.selectFPListbox.config(relief = GUI.R('listbox1Relief'))
        self.selectFPListbox.config(bd = GUI.R('listbox1BorderWidth'))
        self.selectFPListbox.config(highlightthickness = GUI.R('listbox1HighlightThickness'))
        self.selectFPListbox.config(selectbackground = GUI.R('listbox1SelectBG'))
        self.selectFPListbox.config(selectmode = TK.MULTIPLE)
        self.selectFPListbox.pack(fill = TK.BOTH, expand = 1, padx = 6, pady = 6)
        for x in FMT.getList():
            self.selectFPListbox.insert(TK.END, x)

        # Usuń zaznaczone - Button
        self.deleteSelectedFPButton = TKttk.Button(self.ZPFWindow)
        self.deleteSelectedFPButton.config(style = 'button1.TButton')
        self.deleteSelectedFPButton.config(text = 'Usuń zaznaczone')
        self.deleteSelectedFPButton.config(command = self.deleteSelectedFPButtonAction)
        self.deleteSelectedFPButton.pack(fill = TK.X, padx = 6, pady = 6)
    
    def aboutInstructionButtonAction(self):
        try:
            OS.startfile('documentation\index.html')
        except Exception as exceptInfo:
            MSG('E0016', False, exceptInfo)




# Inicjacja okna
root = TK.Tk()
windowInit = mainWindow(root)
root.mainloop()