"""
# Generator CSV
# Wersja 4.0
# Autorzy: Mateusz Skoczek
# Styczeń 2019 - Czerwiec 2020
# dla ZSP Sobolew
"""





# ----------------------------------------- # Zmienne # ----------------------------------------- #

class VARS:
    programName = 'Generator CSV'
    programVersion = '4.0'
    programCustomer = 'ZSP Sobolew'
    programAuthors = ['Mateusz Skoczek']
    programToW = ['styczeń', 2019, 'wrzesień', 2020]





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
        TKmsb.showerror('Informacja', '%s\n%s' % (MSGlist[code], optionalInfo[0]))
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
SU.rmtree(str(appdata) + '/Generator CSV')
#TODO
if 'Generator CSV' not in [x for x in OS.listdir(appdata)]:
    try:
        OS.mkdir(str(appdata) + '/Generator CSV')
        SU.copy('default-configs/config.cfg', str(appdata) + '\Generator CSV\config.cfg')
        SU.copy('default-configs/style.cfg', str(appdata) + '\Generator CSV\style.cfg')
        OS.mkdir(str(appdata) + '/Generator CSV/format-presets')
    except Exception as exceptInfo:
        MSG('E0001', True, exceptInfo)





# ----------------------------- # Ładowanie pliku konfiguracyjnego # ---------------------------- #

class CFG:
    def __checkInstance(self, write):
        if write:
            try:
                file = open((str(appdata) + '\Generator CSV\config.cfg'), 'a')
            except Exception as exceptInfo:
                MSG('E0002', False, exceptInfo)
                return False
            else:
                if not file.writable():
                    MSG('E0002', False, 'Plik tylko do odczytu')
                    return False
                else:
                    return True
        else:
            try:
                open(str(appdata) + '\Generator CSV\config.cfg')
            except Exception as exceptInfo:
                MSG('E0002', True, exceptInfo)

    def __checkContent(self, write, content):
        if write:
            return [True, content]
        else:
            class functions:
                def string(self, var):
                    if var in list(content.keys()):
                        return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def array(self, var):
                    if var in list(content.keys()):
                        new_contentVar = (content[var])[1:-1].split(', ')
                        xnew_contentVar = []
                        for x in new_contentVar:
                            xnew_contentVar.append(x[1:-1])
                        content[var] = xnew_contentVar
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
            functions = functions()
            functions.string('secret')
            functions.array('allowedCharactersInSeparator')
            return [True, content]
    
    def R(self):
        self.__checkInstance(False)
        content = {}
        for x in CD.open((str(appdata) + '\Generator CSV\config.cfg'), 'r', 'utf-8').read().split('\n'):
            x = x.split(' = ')
            try:
                content[x[0]] = (x[1]).strip('\r')
            except:
                continue
        contentCheckingOutput = self.__checkContent(False, content)
        if contentCheckingOutput[0]:
            return contentCheckingOutput[1]
        else:
            MSG('E0003', True, contentCheckingOutput[1])

    def W(self, changes):
        content = self.R()
        for x in changes:
            content[x] = changes[x]
        contentCheckingOutput = self.__checkContent(True, content)
        if contentCheckingOutput[0]:
            if self.__checkInstance(True):
                with CD.open((str(appdata) + '\Generator CSV\config.cfg'), 'w', 'utf-8') as file:
                    contentToSave = contentCheckingOutput[1]
                    for x in contentToSave:
                        file.write('%s = %s\n' % (x, str(contentToSave[x])))
            else:
                return False
        else:
            MSG('E0004', False, contentCheckingOutput[1])
CFG = CFG()
checkInstance = CFG.R()





# ---------------------------------- # Ładowanie pliku stylu # ---------------------------------- #

class GUI:
    def __checkInstance(self):
        try:
            open(str(appdata) + '\Generator CSV\style.cfg')
        except Exception as exceptInfo:
            MSG('E0004', True, exceptInfo)

    def __checkContent(self, content):
        class functions:
            def integer(self, var):
                if var in list(content.keys()):
                    try:
                        check = int(content[var])
                    except:
                        return [False, 'Niepoprawne dane - klucz: %s' % var]
                    else:
                        content[var] = int(content[var])
                        return [True]
                else:
                    return [False, 'Brak danych - klucz: %s' % var]
            def bool(self, var):
                if var in list(content.keys()):
                    if content[var] != '0' and content[var] != '1':
                        return [False, 'Niepoprawne dane - klucz: %s' % var]
                    else:
                        if content[var] == '0':
                            content[var] = False
                            return [True]
                        else:
                            content[var] = True
                            return [True]
                else:
                    return [False, 'Brak danych - klucz: %s' % var]
            def color(self, var):
                if var in list(content.keys()):
                    if len(content[var]) != 7:
                        return [False, 'Niepoprawne dane - klucz: %s' % var]
                    else:
                        if content[var][0] != '#':
                            return [False, 'Niepoprawne dane - klucz: %s' % var]
                        else:
                            return [True]
                else:
                    return [False, 'Brak danych - klucz: %s' % var]
            def file(self, var):
                if var in list(content.keys()):
                    try:
                        check = open(content[var])
                    except:
                        return [False, 'Niepoprawne dane - klucz: %s' % var]
                    else:
                        return [True]
                else:
                    return [False, 'Brak danych - klucz: %s' % var]
            def fromArray(self, var, array):
                if var in list(content.keys()):
                    if content[var] not in array:
                        return [False, 'Niepoprawne dane - klucz: %s' % var]
                    else:
                        return [True]
                else:
                    return [False, 'Brak danych - klucz: %s' % var]
            def font(self, var):
                if var in list(content.keys()):
                    try:
                        check = int(content[var].split(';')[1])
                    except:
                        return [False, 'Niepoprawne dane - klucz: %s' % var]
                    else:
                        content[var] = (content[var].split(';')[0], int(content[var].split(';')[1]))
                        return [True]
                else:
                    return [False, 'Brak danych - klucz: %s' % var]
        functions = functions()
        check = functions.integer('windowWidth')
        if not check[0]:
            return check
        check = functions.integer('windowHeight')
        if not check[0]:
            return check
        check = functions.bool('windowWidthResizable')
        if not check[0]:
            return check
        check = functions.bool('windowHeightResizable')
        if not check[0]:
            return check
        check = functions.color('windowMainBG')
        if not check[0]:
            return check
        check = functions.file('mainIcon')
        if not check[0]:
            return check
        check = functions.color('mainMenuBG')
        if not check[0]:
            return check
        check = functions.fromArray('mainMenuPosition', ['nw', 'ne', 'en', 'es', 'se', 'sw', 'ws', 'wn'])
        if not check[0]:
            return check
        check = functions.integer('tabIconsSize')
        if not check[0]:
            return check
        check = functions.file('generateTabIcon')
        if not check[0]:
            return check
        check = functions.integer('tabFramesBorderWidth')
        if not check[0]:
            return check
        check = functions.color('unselectedTabBG')
        if not check[0]:
            return check
        check = functions.integer('menuTabsBorderWidth')
        if not check[0]:
            return check
        check = functions.integer('menuTabsPadding')
        if not check[0]:
            return check
        check = functions.color('selectedTabBG')
        if not check[0]:
            return check
        check = functions.color('disabledTabBG')
        if not check[0]:
            return check
        check = functions.font('headerFont')
        if not check[0]:
            return check
        check = functions.color('headerBG')
        if not check[0]:
            return check
        check = functions.color('headerTextColor')
        if not check[0]:
            return check
        check = functions.integer('headerPadding')
        if not check[0]:
            return check
        check = functions.integer('headerWidth')
        if not check[0]:
            return check
        check = functions.color('tabFrameBG')
        if not check[0]:
            return check
        check = functions.file('formatTabIcon')
        if not check[0]:
            return check
        check = functions.integer('tabFramePadding')
        if not check[0]:
            return check
        check = functions.color('label1BG')
        if not check[0]:
            return check
        check = functions.color('label1TextColor')
        if not check[0]:
            return check
        check = functions.fromArray('headerTextAnchor', ['center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'])
        if not check[0]:
            return check
        check = functions.color('combobox1ArrowColor')
        if not check[0]:
            return check
        check = functions.color('combobox1ButtonColor')
        if not check[0]:
            return check
        check = functions.color('combobox1BorderColor')
        if not check[0]:
            return check
        check = functions.color('combobox1FieldBackground')
        if not check[0]:
            return check
        check = functions.color('combobox1TextColor')
        if not check[0]:
            return check
        check = functions.fromArray('combobox1Relief', ['flat', 'raised', 'sunken', 'groove', 'ridge'])
        if not check[0]:
            return check
        check = functions.integer('combobox1BorderWidth')
        if not check[0]:
            return check
        check = functions.integer('combobox1Padding')
        if not check[0]:
            return check
        check = functions.color('combobox1ListBoxBackground')
        if not check[0]:
            return check
        check = functions.color('combobox1ListBoxForeground')
        if not check[0]:
            return check
        check = functions.color('combobox1ListBoxSelectBackground')
        if not check[0]:
            return check
        check = functions.color('combobox1ListBoxSelectForeground')
        if not check[0]:
            return check
        check = functions.fromArray('button1TextAnchor', ['center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'])
        if not check[0]:
            return check
        check = functions.color('button1Background')
        if not check[0]:
            return check
        check = functions.color('button1Foreground')
        if not check[0]:
            return check
        check = functions.integer('button1Padding')
        if not check[0]:
            return check
        check = functions.integer('editingPresetSaveButtonWidth')
        if not check[0]:
            return check
        check = functions.integer('editingPresetCancelButtonWidth')
        if not check[0]:
            return check
        check = functions.integer('loadingButtonWidth')
        if not check[0]:
            return check
        check = functions.integer('loadingListWidth')
        if not check[0]:
            return check
        check = functions.integer('label2Width')
        if not check[0]:
            return check
        check = functions.fromArray('label2Anchor', ['center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'])
        if not check[0]:
            return check
        check = functions.color('spinbox1ArrowColor')
        if not check[0]:
            return check
        check = functions.color('spinbox1FieldBackground')
        if not check[0]:
            return check
        check = functions.fromArray('spinbox1Relief', ['flat', 'raised', 'sunken', 'groove', 'ridge'])
        if not check[0]:
            return check
        check = functions.integer('spinbox1BorderWidth')
        if not check[0]:
            return check
        check = functions.color('spinbox1TextColor')
        if not check[0]:
            return check
        check = functions.color('spinbox1ButtonColor')
        if not check[0]:
            return check
        check = functions.color('radiobutton1Background')
        if not check[0]:
            return check
        check = functions.color('radiobutton1TextColor')
        if not check[0]:
            return check
        check = functions.color('entry1FieldBackground')
        if not check[0]:
            return check
        check = functions.fromArray('entry1Relief', ['flat', 'raised', 'sunken', 'groove', 'ridge'])
        if not check[0]:
            return check
        check = functions.integer('entry1BorderWidth')
        if not check[0]:
            return check
        check = functions.integer('entry1Padding')
        if not check[0]:
            return check
        check = functions.color('text1Background')
        if not check[0]:
            return check
        check = functions.color('text1TextColor')
        if not check[0]:
            return check
        check = functions.fromArray('text1Relief', ['flat', 'raised', 'sunken', 'groove', 'ridge'])
        if not check[0]:
            return check
        check = functions.color('entry1TextColor')
        if not check[0]:
            return check
        check = functions.color('label2BG')
        if not check[0]:
            return check
        check = functions.color('label2TextColor')
        if not check[0]:
            return check
        check = functions.color('label3BG')
        if not check[0]:
            return check
        check = functions.color('label3TextColor')
        if not check[0]:
            return check
        check = functions.fromArray('label3Anchor', ['center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'])
        if not check[0]:
            return check
        check = functions.color('radiobutton1IndicatorBackground')
        if not check[0]:
            return check
        check = functions.integer('loadingListPadX')
        if not check[0]:
            return check
        check = functions.integer('EPOSTypeStudentRadiobuttonPadY')
        if not check[0]:
            return check
        check = functions.integer('EPOSTypeStudentRadiobuttonWidth')
        if not check[0]:
            return check
        check = functions.integer('EPOSTypeTeacherRadiobuttonWidth')
        if not check[0]:
            return check
        check = functions.integer('EPOSTypeTeacherRadiobuttonPadY')
        if not check[0]:
            return check
        check = functions.integer('EPOSPersonSeparatorEntryWidth')
        if not check[0]:
            return check
        check = functions.integer('EPOSRowSeparatorEntryWidth')
        if not check[0]:
            return check
        check = functions.integer('EPOSDataSeparatorTextWidth')
        if not check[0]:
            return check
        check = functions.integer('EPOSDataSeparatorTextHeight')
        if not check[0]:
            return check
        check = functions.integer('EPDataLocalizationPadX')
        if not check[0]:
            return check
        check = functions.integer('EPDataLocalizationPadY')
        if not check[0]:
            return check
        check = functions.color('label3BG')
        if not check[0]:
            return check
        check = functions.color('label3TextColor')
        if not check[0]:
            return check
        check = functions.font('label3Font')
        if not check[0]:
            return check
        return [True, content]
    
    def R(self):
        self.__checkInstance()
        content = {}
        for x in CD.open((str(appdata) + '\Generator CSV\style.cfg'), 'r', 'utf-8').read().split('\n'):
            x = x.split(' = ')
            try:
                content[x[0]] = (x[1]).strip('\r')
            except:
                continue
        contentCheckingOutput = self.__checkContent(content)
        if contentCheckingOutput[0]:
            return contentCheckingOutput[1]
        else:
            MSG('E0005', True, contentCheckingOutput[1])
GUI = GUI()
checkInstance = GUI.R()





# ------------------------------- # Zarządzanie plikami formatu # ------------------------------- #

class FMT:
    def __checkFolderInstance(self):
        if 'Generator CSV' not in [x for x in OS.listdir(appdata)]:
            OS.mkdir(str(appdata) + '/Generator CSV')
        else:
            if 'format-presets' not in [x for x in OS.listdir(str(appdata) + '\Generator CSV')]:
                OS.mkdir(str(appdata) + '/Generator CSV/format-presets')
    
    def __checkContent(self, write, content):
        if write:
            class functions:
                def bool(self, var):
                    if var in list(content.keys()):
                        if content[var] != True and content[var] != False:
                            return [False, 'Niepoprawne dane - klucz: %s' % var]
                        else:
                            if content[var] == False:
                                content[var] = '0'
                                return [True]
                            else:
                                content[var] = '1'
                                return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def separator_string(self, var):
                    if var in list(content.keys()):
                        allowedCharactersInSeparator = CFG.R()['allowedCharactersInSeparator']
                        check = content[var]
                        check = check.strip('<enter>')
                        for x in check:
                            if x not in allowedCharactersInSeparator:
                                return [False, 'Niepoprawne dane - klucz: %s' % var]
                        return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def separator_array(self, var):
                    if var in list(content.keys()):
                        allowedCharactersInSeparator = CFG.R()['allowedCharactersInSeparator']
                        check = content[var]
                        for x in check:
                            x = x.strip('<enter>')
                            for y in x:
                                if y not in allowedCharactersInSeparator:
                                    return [False, 'Niepoprawne dane - klucz: %s' % var]
                        content[var] = str(content[var])
                        return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def integer(self, var):
                    if var in list(content.keys()):
                        content[var] = str(content[var])
                        return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
            functions = functions()
            check = functions.bool('student')
            if not check[0]:
                return check
            check = functions.separator_string('personSeparator')
            if not check[0]:
                return check
            check = functions.separator_string('rowSeparator')
            if not check[0]:
                return check
            check = functions.separator_array('dataSeparators')
            if not check[0]:
                return check
            check = functions.integer('loginRow')
            if not check[0]:
                return check
            check = functions.integer('loginPositionInRow')
            if not check[0]:
                return check
            check = functions.integer('fnameRow')
            if not check[0]:
                return check
            check = functions.integer('fnamePositionInRow')
            if not check[0]:
                return check
            check = functions.integer('lnameRow')
            if not check[0]:
                return check
            check = functions.integer('lnamePositionInRow')
            if not check[0]:
                return check
            check = functions.integer('schoolRow')
            if not check[0]:
                return check
            check = functions.integer('schoolPositionInRow')
            if not check[0]:
                return check
            check = functions.integer('classRow')
            if not check[0]:
                return check
            check = functions.integer('classPositionInRow')
            if not check[0]:
                return check
            return [True, content]
        else:
            class functions:
                def bool(self, var):
                    if var in list(content.keys()):
                        if content[var] != '0' and content[var] != '1':
                            return [False, 'Niepoprawne dane - klucz: %s' % var]
                        else:
                            if content[var] == '0':
                                content[var] = False
                                return [True]
                            else:
                                content[var] = True
                                return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def separator_string(self, var):
                    if var in list(content.keys()):
                        allowedCharactersInSeparator = CFG.R()['allowedCharactersInSeparator']
                        check = content[var]
                        check = check.strip('<enter>')
                        for x in check:
                            if x not in allowedCharactersInSeparator:
                                return [False, 'Niepoprawne dane - klucz: %s' % var]
                        return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def separator_array(self, var):
                    if var in list(content.keys()):
                        allowedCharactersInSeparator = CFG.R()['allowedCharactersInSeparator']
                        new_contentVar = (content[var])[1:-1].split(', ')
                        xnew_contentVar = []
                        for x in new_contentVar:
                            xnew_contentVar.append(x[1:-1])
                        check = xnew_contentVar
                        for x in check:
                            x = x.strip('<enter>')
                            for y in x:
                                if y not in allowedCharactersInSeparator:
                                    return [False, 'Niepoprawne dane - klucz: %s' % var]
                        content[var] = xnew_contentVar
                        return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
                def integer(self, var):
                    if var in list(content.keys()):
                        try:
                            check = int(content[var])
                        except:
                            return [False, 'Niepoprawne dane - klucz: %s' % var]
                        else:
                            content[var] = int(content[var])
                            return [True]
                    else:
                        return [False, 'Brak danych - klucz: %s' % var]
            functions = functions()
            check = functions.bool('student')
            if not check[0]:
                return check
            check = functions.separator_string('personSeparator')
            if not check[0]:
                return check
            check = functions.separator_string('rowSeparator')
            if not check[0]:
                return check
            check = functions.separator_array('dataSeparators')
            if not check[0]:
                return check
            check = functions.integer('loginRow')
            if not check[0]:
                return check
            check = functions.integer('loginPositionInRow')
            if not check[0]:
                return check
            check = functions.integer('fnameRow')
            if not check[0]:
                return check
            check = functions.integer('fnamePositionInRow')
            if not check[0]:
                return check
            check = functions.integer('lnameRow')
            if not check[0]:
                return check
            check = functions.integer('lnamePositionInRow')
            if not check[0]:
                return check
            check = functions.integer('schoolRow')
            if not check[0]:
                return check
            check = functions.integer('schoolPositionInRow')
            if not check[0]:
                return check
            check = functions.integer('classRow')
            if not check[0]:
                return check
            check = functions.integer('classPositionInRow')
            if not check[0]:
                return check
            return [True, content]
    
    def getList(self):
        self.__checkFolderInstance()
        filesList = OS.listdir(str(appdata) + '/Generator CSV/format-presets')
        formatPresetsList = []
        for x in filesList:
            if x[-4:] == '.fmt':
                formatPresetsList.append(x[:-4])
            else:
                continue
        return formatPresetsList

    def R(self, preset):
        if preset in self.getList():
            path = str(appdata) + '/Generator CSV/format-presets/%s.fmt' % preset
            file = CD.open(path, 'r', 'utf-8').read().split('\n')
            content = {}
            for x in file:
                x = x.split(' = ')
                try:
                    content[x[0]] = (x[1]).strip('\r')
                except:
                    continue
            contentCheckingOutput = self.__checkContent(False, content)
            if contentCheckingOutput[0]:
                content = contentCheckingOutput[1]
            else:
                MSG('E0006', False, contentCheckingOutput[1])
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
            }
        return content
    
    def W(self, preset, content):
        contentCheckingOutput = self.__checkContent(True, content)
        if contentCheckingOutput[0]:
            contentToSave = contentCheckingOutput[1]
            with CD.open(str(appdata) + '/Generator CSV/format-presets/%s.fmt' % preset, 'w', 'utf-8') as file:
                for x in contentToSave:
                    file.write(x + ' = ' + content[x] + '\n')
            return True
        else:
            MSG('E0006', False, contentCheckingOutput[1])
            return False
FMT = FMT()





# ------------------------------------------- # GUI # ------------------------------------------- #

def window():
    # Ustawienia okna
    window = TK.Tk()
    window.title('%s %s' % (VARS.programName, VARS.programVersion))
    window.geometry('%sx%s' % (str(GUI.R()['windowWidth']), str(GUI.R()['windowHeight'])))
    window.resizable(width = GUI.R()['windowWidthResizable'], height = GUI.R()['windowHeightResizable'])
    window.configure(bg = GUI.R()['windowMainBG'])
    window.iconbitmap(GUI.R()['mainIcon'])



    # Theme
    TKttk.Style().theme_create("main", parent = "default", settings = {
        "mainMenu.TNotebook": {
            "configure": {
                "background": GUI.R()['mainMenuBG'],
                "tabposition": GUI.R()['mainMenuPosition'],
                "borderwidth": GUI.R()['tabFramesBorderWidth'],
            },
        },
        "mainMenu.TNotebook.Tab": {
            "configure": {
                "background": GUI.R()['unselectedTabBG'],
                "borderwidth": GUI.R()['menuTabsBorderWidth'],
                "padding": GUI.R()['menuTabsPadding'],
            },
            "map": {
                "background": [
                    ("selected", GUI.R()['selectedTabBG']),
                    ("disabled", GUI.R()['disabledTabBG']),
                ]
            }
        },
        "mainMenuTabFrame.TFrame": {
            "configure": {
                "background": GUI.R()['tabFrameBG'],
            },
        },
        "tabHeader.TLabel": {
            "configure": {
                "font": GUI.R()['headerFont'],
                "background": GUI.R()['headerBG'],
                "foreground": GUI.R()['headerTextColor'],
                "padding": GUI.R()['headerPadding'],
                "anchor": GUI.R()['headerTextAnchor'],
            },
        },
        "tabFrame.TFrame": {
            "configure": {
                "background": GUI.R()['tabFrameBG'],
            },
        },
        "layoutFrame.TFrame": {
            "configure": {
                "background": GUI.R()['tabFrameBG'],
            },
        },
        "label1.TLabel": {
            "configure": {
                "background": GUI.R()['label1BG'],
                "foreground": GUI.R()['label1TextColor']
            },
        },
        "label2.TLabel": {
            "configure": {
                "background": GUI.R()['label2BG'],
                "foreground": GUI.R()['label2TextColor'],
                "anchor": GUI.R()['label2Anchor'],
                "width": GUI.R()['label2Width'],
            },
        },
        "label3.TLabel": {
            "configure": {
                "background": GUI.R()['label3BG'],
                "foreground": GUI.R()['label3TextColor'],
                "font" : GUI.R()['label3Font'],
            },
        },
        "combobox1.TCombobox": {
            "configure": {
                "arrowcolor": GUI.R()['combobox1ArrowColor'],
                "background": GUI.R()['combobox1ButtonColor'],
                "bordercolor": GUI.R()['combobox1BorderColor'],
                "fieldbackground": GUI.R()['combobox1FieldBackground'],
                "foreground": GUI.R()['combobox1TextColor'],
                "relief": GUI.R()['combobox1Relief'],
                "borderwidth": GUI.R()['combobox1BorderWidth'],
                "padding": GUI.R()['combobox1Padding'],
            },
        },
        "button1.TButton": {
            "configure": {
                "anchor": GUI.R()['button1TextAnchor'],
                "background": GUI.R()['button1Background'],
                "foreground": GUI.R()['button1Foreground'],
                "padding": GUI.R()['button1Padding'],
            },
        },
        "separator1.TSeparator": {
            "configure": {
                "background": GUI.R()['tabFrameBG'],
            },
        },
        "spinbox1.TSpinbox": {
            "configure": {
                "arrowcolor": GUI.R()['spinbox1ArrowColor'],
                "fieldbackground": GUI.R()['spinbox1FieldBackground'],
                "relief": GUI.R()['spinbox1Relief'],
                "borderwidth": GUI.R()['spinbox1BorderWidth'],
                "foreground": GUI.R()['spinbox1TextColor'],
                "background": GUI.R()['spinbox1ButtonColor']
            },
        },
        "entry1.TEntry": {
            "configure": {
                "fieldbackground": GUI.R()['entry1FieldBackground'],
                "relief": GUI.R()['entry1Relief'],
                "borderwidth": GUI.R()['entry1BorderWidth'],
                "padding": GUI.R()['entry1Padding'],
                "foreground": GUI.R()['entry1TextColor']
            }
        }
    })
    TKttk.Style().theme_use("main")



    # Menu główne
    mainMenu = TKttk.Notebook(window, width = window.winfo_width() - (2 * GUI.R()['menuTabsPadding'] + GUI.R()['tabIconsSize']), height = window.winfo_height())
    mainMenu.config(style = "mainMenu.TNotebook")
    mainMenu.grid(row = 0)

    # Ikona
    iconTab = TKttk.Frame(mainMenu)
    iconTabImg = PLimg.open(GUI.R()['mainIcon'])
    iconTabImg = iconTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
    iconTabImg = PLitk.PhotoImage(iconTabImg)
    mainMenu.add(iconTab, image = iconTabImg, state = TK.DISABLED)



    # TAB2 - Generator ###################################################

    generateTab = TKttk.Frame(mainMenu)
    generateTab.config(style = "mainMenuTabFrame.TFrame")
    generateTabImg = PLimg.open(GUI.R()['generateTabIcon'])
    generateTabImg = generateTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
    generateTabImg = PLitk.PhotoImage(generateTabImg)
    mainMenu.add(generateTab, image = generateTabImg, state = TK.NORMAL)


    # Nagłówek
    generateHeader = TKttk.Label(generateTab)
    generateHeader.config(style = 'tabHeader.TLabel')
    generateHeader.config(text = 'GENERATOR CSV')
    generateHeader.pack(fill = TK.X)


    # Zawartość
    generateFrame = TKttk.Frame(generateTab)
    generateFrame.config(style = 'tabFrame.TFrame')
    generateFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])

    ######################################################################



    # TAB3 - Format ######################################################

    formatTab = TKttk.Frame(mainMenu)
    formatTab.config(style = "mainMenuTabFrame.TFrame")
    formatTabImg = PLimg.open(GUI.R()['formatTabIcon'])
    formatTabImg = formatTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
    formatTabImg = PLitk.PhotoImage(formatTabImg)
    mainMenu.add(formatTab, image = formatTabImg, state = TK.NORMAL)


    # Nagłówek
    formatHeader = TKttk.Label(formatTab)
    formatHeader.config(style = 'tabHeader.TLabel')
    formatHeader.config(text = 'FORMAT DANYCH')
    formatHeader.pack(fill = TK.X)


    # Zawartość
    formatFrame = TKttk.Frame(formatTab)
    formatFrame.config(style = 'tabFrame.TFrame')
    formatFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])


    # (1) Ładowanie presetu #####################

    loadingPresetFrame = TKttk.Frame(formatFrame)
    loadingPresetFrame.config(style = 'layoutFrame.TFrame')
    loadingPresetFrame.pack(fill = TK.X)

    # "Wybierz preset do edycji lub wpisz nazwę nowego"
    loadingListLabel = TKttk.Label(loadingPresetFrame)
    loadingListLabel.config(style = 'label1.TLabel')
    loadingListLabel.config(text = 'Wybierz preset do edycji lub wpisz nazwę nowego')
    loadingListLabel.pack(side = 'left')

    # Rozwijana lista presetów
    loadingListVar = TK.StringVar()
    loadingList = TKttk.Combobox(loadingPresetFrame)
    loadingList.config(textvariable = loadingListVar)
    loadingList.config(style = 'combobox1.TCombobox')
    loadingList.config(width = GUI.R()['loadingListWidth'])
    loadingList.option_add("*TCombobox*Listbox.background", GUI.R()['combobox1ListBoxBackground'])
    loadingList.option_add("*TCombobox*Listbox.foreground", GUI.R()['combobox1ListBoxForeground'])
    loadingList.option_add("*TCombobox*Listbox.selectBackground", GUI.R()['combobox1ListBoxSelectBackground'])
    loadingList.option_add("*TCombobox*Listbox.selectForeground", GUI.R()['combobox1ListBoxSelectForeground'])
    loadingList.pack(side = 'left', padx = GUI.R()['loadingListPadX'])
    loadingList['values'] = tuple(FMT.getList())

    # Przycisk "WCZYTAJ"
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
    }
    def loadingButtonAction():
        formatFileContent = FMT.R(loadingList.get())
        loadingList['state'] = TK.DISABLED
        loadingButton['state'] = TK.DISABLED
        EPOSTypeVar.set(formatFileContent['student'])
        EPOSTypeStudentRadiobutton['state'] = TK.NORMAL
        EPOSTypeTeacherRadiobutton['state'] = TK.NORMAL
        EPOSPersonSeparatorEntry['state'] = TK.NORMAL
        EPOSPersonSeparatorVar.set(formatFileContent['personSeparator'])
        EPOSRowSeparatorEntry['state'] = TK.NORMAL
        EPOSRowSeparatorVar.set(formatFileContent['rowSeparator'])
        EPOSDataSeparatorText['state'] = TK.NORMAL
        EPOSDataSeparatorText.insert(TK.END, '\n'.join(formatFileContent['dataSeparators']))
        EPDataLocalizationLoginRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationLoginRowVar.set(formatFileContent['loginRow'])
        EPDataLocalizationLoginPosInRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationLoginPosInRowVar.set(formatFileContent['loginPositionInRow'])
        EPDataLocalizationFnameRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationFnameRowVar.set(formatFileContent['fnameRow'])
        EPDataLocalizationFnamePosInRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationFnamePosInRowVar.set(formatFileContent['fnamePositionInRow'])
        EPDataLocalizationLnameRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationLnameRowVar.set(formatFileContent['lnameRow'])
        EPDataLocalizationLnamePosInRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationLnamePosInRowVar.set(formatFileContent['lnamePositionInRow'])
        EPDataLocalizationSchoolRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationSchoolRowVar.set(formatFileContent['schoolRow'])
        EPDataLocalizationSchoolPosInRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationSchoolPosInRowVar.set(formatFileContent['schoolPositionInRow'])
        EPDataLocalizationClassRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationClassRowVar.set(formatFileContent['classRow'])
        EPDataLocalizationClassPosInRowSpinbox['state'] = TK.NORMAL
        EPDataLocalizationClassPosInRowVar.set(formatFileContent['classPositionInRow'])
        editingPresetSaveButton['state'] = TK.NORMAL
        editingPresetCancelButton['state'] = TK.NORMAL
    loadingButton = TKttk.Button(loadingPresetFrame)
    loadingButton.config(style = 'button1.TButton')
    loadingButton.config(command = loadingButtonAction)
    loadingButton.config(width = GUI.R()['loadingButtonWidth'])
    loadingButton.config(text = 'WCZYTAJ')
    loadingButton.pack(side = 'right')

    #############################################

    # (1) Separator 1 ###########################

    formatSeparator1 = TKttk.Separator(formatFrame)
    formatSeparator1.config(style = 'separator1.TSeparator')
    formatSeparator1.config(orient = TK.HORIZONTAL)
    formatSeparator1.pack(fill = TK.X, pady = 10)

    #############################################

    # (1) Edycja presetu ########################

    editingPresetFrame = TKttk.Frame(formatFrame)
    editingPresetFrame.config(style = 'layoutFrame.TFrame')
    editingPresetFrame.pack(fill = TK.BOTH, expand = 1)

    # (2) Ustawienia ##################

    editingPresetSettingsFrame = TKttk.Frame(editingPresetFrame)
    editingPresetSettingsFrame.config(style = 'layoutFrame.TFrame')
    editingPresetSettingsFrame.pack(fill = TK.BOTH, expand = 1)

    # (3) Inne ustawienia ###

    editingPresetOtherSettingsFrame = TKttk.Frame(editingPresetSettingsFrame)
    editingPresetOtherSettingsFrame.config(style = 'layoutFrame.TFrame')
    editingPresetOtherSettingsFrame.pack(fill = TK.BOTH, expand = 1, side = TK.LEFT)

    # (4) Typ osoby

    editingPresetOSFrame = TKttk.Frame(editingPresetOtherSettingsFrame)
    editingPresetOSFrame.config(style = 'layoutFrame.TFrame')
    editingPresetOSFrame.pack(fill = TK.BOTH, expand = 1, side = TK.BOTTOM, pady = 5)

    # "Typ osoby"
    EPOSTypeLabel = TKttk.Label(editingPresetOSFrame)
    EPOSTypeLabel.config(style = 'label1.TLabel')
    EPOSTypeLabel.config(text = 'Typ osoby')
    EPOSTypeLabel.grid(row = 0, column = 0, pady = 5, sticky = 'w')

    # Typ osoby - Radiobutton
    EPOSTypeVar = TK.BooleanVar(value = True)

    EPOSTypeStudentRadiobutton = TK.Radiobutton(editingPresetOSFrame)
    EPOSTypeStudentRadiobutton.config(background = GUI.R()['radiobutton1Background'])
    EPOSTypeStudentRadiobutton.config(foreground = GUI.R()['radiobutton1TextColor'])
    EPOSTypeStudentRadiobutton.config(selectcolor = GUI.R()['radiobutton1IndicatorBackground'])
    EPOSTypeStudentRadiobutton.config(activebackground = GUI.R()['radiobutton1Background'])
    EPOSTypeStudentRadiobutton.config(activeforeground = GUI.R()['radiobutton1TextColor'])
    EPOSTypeStudentRadiobutton.config(variable = EPOSTypeVar)
    EPOSTypeStudentRadiobutton.config(value = True)
    EPOSTypeStudentRadiobutton.config(state = TK.DISABLED)
    EPOSTypeStudentRadiobutton.config(width = GUI.R()['EPOSTypeStudentRadiobuttonWidth'])
    EPOSTypeStudentRadiobutton.config(text = 'Uczniowie')
    EPOSTypeStudentRadiobutton.grid(row = 0, column = 1, pady = GUI.R()['EPOSTypeStudentRadiobuttonPadY'])

    EPOSTypeTeacherRadiobutton = TK.Radiobutton(editingPresetOSFrame)
    EPOSTypeTeacherRadiobutton.config(background = GUI.R()['radiobutton1Background'])
    EPOSTypeTeacherRadiobutton.config(foreground = GUI.R()['radiobutton1TextColor'])
    EPOSTypeTeacherRadiobutton.config(selectcolor = GUI.R()['radiobutton1IndicatorBackground'])
    EPOSTypeTeacherRadiobutton.config(activebackground = GUI.R()['radiobutton1Background'])
    EPOSTypeTeacherRadiobutton.config(activeforeground = GUI.R()['radiobutton1TextColor'])
    EPOSTypeTeacherRadiobutton.config(variable = EPOSTypeVar)
    EPOSTypeTeacherRadiobutton.config(value = False)
    EPOSTypeTeacherRadiobutton.config(state = TK.DISABLED)
    EPOSTypeTeacherRadiobutton.config(width = GUI.R()['EPOSTypeTeacherRadiobuttonWidth'])
    EPOSTypeTeacherRadiobutton.config(text = 'Nauczyciele')
    EPOSTypeTeacherRadiobutton.grid(row = 0, column = 2, pady = GUI.R()['EPOSTypeTeacherRadiobuttonPadY'])

    # "Separator pomiędzy osobami"
    EPOSPersonSeparatorLabel = TKttk.Label(editingPresetOSFrame)
    EPOSPersonSeparatorLabel.config(style = 'label1.TLabel')
    EPOSPersonSeparatorLabel.config(text = 'Separator pomiędzy osobami')
    EPOSPersonSeparatorLabel.grid(row = 1, column = 0, pady = 5, sticky = 'w')

    # Entry - Separator pomiedzy osobami
    EPOSPersonSeparatorVar = TK.StringVar()
    EPOSPersonSeparatorEntry = TKttk.Entry(editingPresetOSFrame)
    EPOSPersonSeparatorEntry.config(style = 'entry1.TEntry')
    EPOSPersonSeparatorEntry.config(textvariable = EPOSPersonSeparatorVar)
    EPOSPersonSeparatorEntry.config(state = TK.DISABLED)
    EPOSPersonSeparatorEntry.config(width = GUI.R()['EPOSPersonSeparatorEntryWidth'])
    EPOSPersonSeparatorEntry.grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 5)

    # "Separator pomiędzy wierszami"
    EPOSRowSeparatorLabel = TKttk.Label(editingPresetOSFrame)
    EPOSRowSeparatorLabel.config(style = 'label1.TLabel')
    EPOSRowSeparatorLabel.config(text = 'Separator pomiędzy wierszami')
    EPOSRowSeparatorLabel.grid(row = 2, column = 0, pady = 5, sticky = 'w')

    # Entry - Separator pomiedzy wierszami
    EPOSRowSeparatorVar = TK.StringVar()
    EPOSRowSeparatorEntry = TKttk.Entry(editingPresetOSFrame)
    EPOSRowSeparatorEntry.config(style = 'entry1.TEntry')
    EPOSRowSeparatorEntry.config(textvariable = EPOSRowSeparatorVar)
    EPOSRowSeparatorEntry.config(state = TK.DISABLED)
    EPOSRowSeparatorEntry.config(width = GUI.R()['EPOSRowSeparatorEntryWidth'])
    EPOSRowSeparatorEntry.grid(row = 2, column = 1, columnspan = 2, padx = 5, pady = 5)

    # "Separatory pomiędzy danymi"
    EPOSDataSeparatorLabel = TKttk.Label(editingPresetOSFrame)
    EPOSDataSeparatorLabel.config(style = 'label1.TLabel')
    EPOSDataSeparatorLabel.config(text = 'Separatory pomiędzy danymi')
    EPOSDataSeparatorLabel.grid(row = 3, column = 0, pady = 5, sticky = 'nw')

    # Entry - Separator pomiedzy wierszami
    EPOSDataSeparatorText = TK.Text(editingPresetOSFrame)
    EPOSDataSeparatorText.config(state = TK.DISABLED)
    EPOSDataSeparatorText.config(width = GUI.R()['EPOSDataSeparatorTextWidth'])
    EPOSDataSeparatorText.config(height = GUI.R()['EPOSDataSeparatorTextHeight'])
    EPOSDataSeparatorText.config(background = GUI.R()['text1Background'])
    EPOSDataSeparatorText.config(foreground = GUI.R()['text1TextColor'])
    EPOSDataSeparatorText.config(relief = GUI.R()['text1Relief'])
    EPOSDataSeparatorText.grid(row = 3, column = 1, columnspan = 2, padx = 5, pady = 5)

    # "<enter> - nowa linia | wciśnięcie przycisku ENTER | \n"
    EPOSSeparatorEnterInfoLabel = TKttk.Label(editingPresetOSFrame)
    EPOSSeparatorEnterInfoLabel.config(style = 'label1.TLabel')
    EPOSSeparatorEnterInfoLabel.config(text = (r'<enter> - nowa linia | wciśnięcie przycisku ENTER | \n' + '\n' + 'Niedozwolone znaki: litery, cyfry, *'))
    EPOSSeparatorEnterInfoLabel.grid(row = 4, column = 1, columnspan = 2)

    ###############

    #########################

    # (3) Separator 2 #######

    formatSeparator2 = TKttk.Separator(editingPresetSettingsFrame)
    formatSeparator2.config(style = 'separator1.TSeparator')
    formatSeparator2.config(orient = TK.VERTICAL)
    formatSeparator2.pack(fill = TK.Y, padx = 10, side = TK.LEFT)

    #########################

    # (3) Lokalizacja danych

    editingPresetDataLocalizationSettingsFrame = TKttk.Frame(editingPresetSettingsFrame)
    editingPresetDataLocalizationSettingsFrame.config(style = 'layoutFrame.TFrame')
    editingPresetDataLocalizationSettingsFrame.pack(fill = TK.BOTH, side = TK.RIGHT)

    # C1 - "Wiersz"
    editingPresetDataLocalizationC1Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationC1Label.config(style = 'label1.TLabel')
    editingPresetDataLocalizationC1Label.config(text = 'Wiersz')
    editingPresetDataLocalizationC1Label.grid(row = 0, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # C2 - "Pozycja w wierszu"
    editingPresetDataLocalizationC2Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationC2Label.config(style = 'label1.TLabel')
    editingPresetDataLocalizationC2Label.config(text = 'Pozycja w wierszu')
    editingPresetDataLocalizationC2Label.grid(row = 0, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # W1 - "Login"
    editingPresetDataLocalizationW1Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationW1Label.config(style = 'label2.TLabel')
    editingPresetDataLocalizationW1Label.config(text = 'Login')
    editingPresetDataLocalizationW1Label.grid(row = 1, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja loginu (wiersz)
    EPDataLocalizationLoginRowVar = TK.IntVar()
    EPDataLocalizationLoginRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationLoginRowSpinbox.config(textvariable = EPDataLocalizationLoginRowVar)
    EPDataLocalizationLoginRowSpinbox.config(from_ = 0)
    EPDataLocalizationLoginRowSpinbox.config(to = 1000000)
    EPDataLocalizationLoginRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationLoginRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationLoginRowSpinbox.grid(row = 1, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja loginu (pozycja w wierszu)
    EPDataLocalizationLoginPosInRowVar = TK.IntVar()
    EPDataLocalizationLoginPosInRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationLoginPosInRowSpinbox.config(textvariable = EPDataLocalizationLoginPosInRowVar)
    EPDataLocalizationLoginPosInRowSpinbox.config(from_ = 0)
    EPDataLocalizationLoginPosInRowSpinbox.config(to = 1000000)
    EPDataLocalizationLoginPosInRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationLoginPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationLoginPosInRowSpinbox.grid(row = 1, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # W2 - "Imię"
    editingPresetDataLocalizationW2Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationW2Label.config(style = 'label2.TLabel')
    editingPresetDataLocalizationW2Label.config(text = 'Imię')
    editingPresetDataLocalizationW2Label.grid(row = 2, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja imienia (wiersz)
    EPDataLocalizationFnameRowVar = TK.IntVar()
    EPDataLocalizationFnameRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationFnameRowSpinbox.config(textvariable = EPDataLocalizationFnameRowVar)
    EPDataLocalizationFnameRowSpinbox.config(from_ = 0)
    EPDataLocalizationFnameRowSpinbox.config(to = 1000000)
    EPDataLocalizationFnameRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationFnameRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationFnameRowSpinbox.grid(row = 2, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja imienia (pozycja w wierszu)
    EPDataLocalizationFnamePosInRowVar = TK.IntVar()
    EPDataLocalizationFnamePosInRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationFnamePosInRowSpinbox.config(textvariable = EPDataLocalizationFnamePosInRowVar)
    EPDataLocalizationFnamePosInRowSpinbox.config(from_ = 0)
    EPDataLocalizationFnamePosInRowSpinbox.config(to = 1000000)
    EPDataLocalizationFnamePosInRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationFnamePosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationFnamePosInRowSpinbox.grid(row = 2, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # W3 - "Nazwisko"
    editingPresetDataLocalizationW3Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationW3Label.config(style = 'label2.TLabel')
    editingPresetDataLocalizationW3Label.config(text = 'Nazwisko')
    editingPresetDataLocalizationW3Label.grid(row = 3, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja nazwiska (wiersz)
    EPDataLocalizationLnameRowVar = TK.IntVar()
    EPDataLocalizationLnameRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationLnameRowSpinbox.config(textvariable = EPDataLocalizationLnameRowVar)
    EPDataLocalizationLnameRowSpinbox.config(from_ = 0)
    EPDataLocalizationLnameRowSpinbox.config(to = 1000000)
    EPDataLocalizationLnameRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationLnameRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationLnameRowSpinbox.grid(row = 3, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja nazwiska (pozycja w wierszu)
    EPDataLocalizationLnamePosInRowVar = TK.IntVar()
    EPDataLocalizationLnamePosInRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationLnamePosInRowSpinbox.config(textvariable = EPDataLocalizationLnamePosInRowVar)
    EPDataLocalizationLnamePosInRowSpinbox.config(from_ = 0)
    EPDataLocalizationLnamePosInRowSpinbox.config(to = 1000000)
    EPDataLocalizationLnamePosInRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationLnamePosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationLnamePosInRowSpinbox.grid(row = 3, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # W4 - "Szkoła"
    editingPresetDataLocalizationW4Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationW4Label.config(style = 'label2.TLabel')
    editingPresetDataLocalizationW4Label.config(text = 'Szkoła')
    editingPresetDataLocalizationW4Label.grid(row = 4, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja nazwiska (wiersz)
    EPDataLocalizationSchoolRowVar = TK.IntVar()
    EPDataLocalizationSchoolRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationSchoolRowSpinbox.config(textvariable = EPDataLocalizationSchoolRowVar)
    EPDataLocalizationSchoolRowSpinbox.config(from_ = 0)
    EPDataLocalizationSchoolRowSpinbox.config(to = 1000000)
    EPDataLocalizationSchoolRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationSchoolRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationSchoolRowSpinbox.grid(row = 4, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja nazwiska (pozycja w wierszu)
    EPDataLocalizationSchoolPosInRowVar = TK.IntVar()
    EPDataLocalizationSchoolPosInRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationSchoolPosInRowSpinbox.config(textvariable = EPDataLocalizationSchoolPosInRowVar)
    EPDataLocalizationSchoolPosInRowSpinbox.config(from_ = 0)
    EPDataLocalizationSchoolPosInRowSpinbox.config(to = 1000000)
    EPDataLocalizationSchoolPosInRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationSchoolPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationSchoolPosInRowSpinbox.grid(row = 4, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # W5 - "Klasa"
    editingPresetDataLocalizationW5Label = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    editingPresetDataLocalizationW5Label.config(style = 'label2.TLabel')
    editingPresetDataLocalizationW5Label.config(text = 'Klasa')
    editingPresetDataLocalizationW5Label.grid(row = 5, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja nazwiska (wiersz)
    EPDataLocalizationClassRowVar = TK.IntVar()
    EPDataLocalizationClassRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationClassRowSpinbox.config(textvariable = EPDataLocalizationClassRowVar)
    EPDataLocalizationClassRowSpinbox.config(from_ = 0)
    EPDataLocalizationClassRowSpinbox.config(to = 1000000)
    EPDataLocalizationClassRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationClassRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationClassRowSpinbox.grid(row = 5, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Lokalizacja nazwiska (pozycja w wierszu)
    EPDataLocalizationClassPosInRowVar = TK.IntVar()
    EPDataLocalizationClassPosInRowSpinbox = TKttk.Spinbox(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationClassPosInRowSpinbox.config(textvariable = EPDataLocalizationClassPosInRowVar)
    EPDataLocalizationClassPosInRowSpinbox.config(from_ = 0)
    EPDataLocalizationClassPosInRowSpinbox.config(to = 1000000)
    EPDataLocalizationClassPosInRowSpinbox.config(state = TK.DISABLED)
    EPDataLocalizationClassPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
    EPDataLocalizationClassPosInRowSpinbox.grid(row = 5, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    # Informacje
    EPDataLocalizationInfoLabel = TKttk.Label(editingPresetDataLocalizationSettingsFrame)
    EPDataLocalizationInfoLabel.config(style = 'label3.TLabel')
    EPDataLocalizationInfoLabel.config(justify = 'center')
    EPDataLocalizationInfoLabel.config(text = "1234567u\nAdam Nowak, 18\n1a LO\n*******\n\n7654321u\nJan Kowalski, 11\n2a BS\n**********\n\n------------------\n\nTyp osoby: Uczniowie\nSeparator pomiedzy osobami: '<enter><enter>'\nSeparator pomiedzy wierszami: '<enter>'\nSeparator pomiedzy danymi: ' *enter*, '\nLogin: 1 | 1\nImię: 2 | 1\nNazwisko: 2 | 2\nSzkoła: 3 | 2\nKlasa: 3 | 1")
    EPDataLocalizationInfoLabel.grid(row = 6, column = 0, columnspan = 3, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

    #########################

    ###################################

    # (2) Przyciski ###################

    editingPresetButtonsFrame = TKttk.Frame(editingPresetFrame)
    editingPresetButtonsFrame.config(style = 'layoutFrame.TFrame')
    editingPresetButtonsFrame.pack(fill = TK.X, side = TK.BOTTOM, pady = 10)

    def editingPresetSave():
        studentVar = EPOSTypeVar.get()
        if studentVar == 's':
            studentVar = True
        else:
            studentVar = False
        formatFileContentToSave = {
            "student" : studentVar,
            "personSeparator" : EPOSPersonSeparatorEntry.get(),
            "rowSeparator" : EPOSRowSeparatorEntry.get(),
            "dataSeparators" : (EPOSDataSeparatorText.get("1.0", TK.END)).split('\n')[:-1],
            "loginRow" : int(EPDataLocalizationLoginRowSpinbox.get()),
            "loginPositionInRow" : int(EPDataLocalizationLoginPosInRowSpinbox.get()),
            "fnameRow" : int(EPDataLocalizationFnameRowSpinbox.get()),
            "fnamePositionInRow" : int(EPDataLocalizationFnamePosInRowSpinbox.get()),
            "lnameRow" : int(EPDataLocalizationLnameRowSpinbox.get()),
            "lnamePositionInRow" : int(EPDataLocalizationLnamePosInRowSpinbox.get()),
            "schoolRow" : int(EPDataLocalizationSchoolRowSpinbox.get()),
            "schoolPositionInRow" : int(EPDataLocalizationSchoolPosInRowSpinbox.get()),
            "classRow" : int(EPDataLocalizationClassRowSpinbox.get()),
            "classPositionInRow" : int(EPDataLocalizationClassPosInRowSpinbox.get()),
        }
        if not FMT.W(loadingList.get(), formatFileContentToSave):
            return
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
        }
        loadingList['state'] = TK.NORMAL
        loadingButton['state'] = TK.NORMAL
        EPOSTypeVar.set(formatFileContent['student'])
        EPOSTypeStudentRadiobutton['state'] = TK.DISABLED
        EPOSTypeTeacherRadiobutton['state'] = TK.DISABLED
        EPOSPersonSeparatorEntry['state'] = TK.DISABLED
        EPOSPersonSeparatorVar.set(formatFileContent['personSeparator'])
        EPOSRowSeparatorEntry['state'] = TK.DISABLED
        EPOSRowSeparatorVar.set(formatFileContent['rowSeparator'])
        EPOSDataSeparatorText.delete('1.0', TK.END)
        EPOSDataSeparatorText['state'] = TK.DISABLED
        EPDataLocalizationLoginRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLoginRowVar.set(formatFileContent['loginRow'])
        EPDataLocalizationLoginPosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLoginPosInRowVar.set(formatFileContent['loginPositionInRow'])
        EPDataLocalizationFnameRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationFnameRowVar.set(formatFileContent['fnameRow'])
        EPDataLocalizationFnamePosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationFnamePosInRowVar.set(formatFileContent['fnamePositionInRow'])
        EPDataLocalizationLnameRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLnameRowVar.set(formatFileContent['lnameRow'])
        EPDataLocalizationLnamePosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLnamePosInRowVar.set(formatFileContent['lnamePositionInRow'])
        EPDataLocalizationSchoolRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationSchoolRowVar.set(formatFileContent['schoolRow'])
        EPDataLocalizationSchoolPosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationSchoolPosInRowVar.set(formatFileContent['schoolPositionInRow'])
        EPDataLocalizationClassRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationClassRowVar.set(formatFileContent['classRow'])
        EPDataLocalizationClassPosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationClassPosInRowVar.set(formatFileContent['classPositionInRow'])
        editingPresetSaveButton['state'] = TK.DISABLED
        editingPresetCancelButton['state'] = TK.DISABLED
        loadingList['values'] = tuple(FMT.getList())

    def editingPresetSaveButtonAction():
        if loadingList.get() not in FMT.getList():
            if MSG('A0001', False):
                editingPresetSave()
            else:
                return
        else:
            if MSG('A0002', False):
                editingPresetSave()
            else:
                return
    editingPresetSaveButton = TKttk.Button(editingPresetButtonsFrame)
    editingPresetSaveButton.config(command = editingPresetSaveButtonAction)
    editingPresetSaveButton.config(state = TK.DISABLED)
    editingPresetSaveButton.config(style = 'button1.TButton')
    editingPresetSaveButton.config(width = GUI.R()['editingPresetSaveButtonWidth'])
    editingPresetSaveButton.config(text = 'ZAPISZ')
    editingPresetSaveButton.pack(side = TK.LEFT, expand = 1)

    def editingPresetCancelAction():
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
        }
        loadingList['state'] = TK.NORMAL
        loadingButton['state'] = TK.NORMAL
        EPOSTypeStudentRadiobutton['state'] = TK.DISABLED
        EPOSTypeTeacherRadiobutton['state'] = TK.DISABLED
        EPOSTypeVar.set(formatFileContent['student'])
        EPOSPersonSeparatorEntry['state'] = TK.DISABLED
        EPOSPersonSeparatorVar.set(formatFileContent['personSeparator'])
        EPOSRowSeparatorEntry['state'] = TK.DISABLED
        EPOSRowSeparatorVar.set(formatFileContent['rowSeparator'])
        EPOSDataSeparatorText.delete('1.0', TK.END)
        EPOSDataSeparatorText['state'] = TK.DISABLED
        EPDataLocalizationLoginRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLoginRowVar.set(formatFileContent['loginRow'])
        EPDataLocalizationLoginPosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLoginPosInRowVar.set(formatFileContent['loginPositionInRow'])
        EPDataLocalizationFnameRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationFnameRowVar.set(formatFileContent['fnameRow'])
        EPDataLocalizationFnamePosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationFnamePosInRowVar.set(formatFileContent['fnamePositionInRow'])
        EPDataLocalizationLnameRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLnameRowVar.set(formatFileContent['lnameRow'])
        EPDataLocalizationLnamePosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationLnamePosInRowVar.set(formatFileContent['lnamePositionInRow'])
        EPDataLocalizationSchoolRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationSchoolRowVar.set(formatFileContent['schoolRow'])
        EPDataLocalizationSchoolPosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationSchoolPosInRowVar.set(formatFileContent['schoolPositionInRow'])
        EPDataLocalizationClassRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationClassRowVar.set(formatFileContent['classRow'])
        EPDataLocalizationClassPosInRowSpinbox['state'] = TK.DISABLED
        EPDataLocalizationClassPosInRowVar.set(formatFileContent['classPositionInRow'])
        editingPresetSaveButton['state'] = TK.DISABLED
        editingPresetCancelButton['state'] = TK.DISABLED
        loadingList['values'] = tuple(FMT.getList())
    editingPresetCancelButton = TKttk.Button(editingPresetButtonsFrame)
    editingPresetCancelButton.config(command = editingPresetCancelAction)
    editingPresetCancelButton.config(state = TK.DISABLED)
    editingPresetCancelButton.config(style = 'button1.TButton')
    editingPresetCancelButton.config(width = GUI.R()['editingPresetCancelButtonWidth'])
    editingPresetCancelButton.config(text = 'Anuluj')
    editingPresetCancelButton.pack(side = TK.RIGHT, expand = 1)

    ###################################

    #############################################

    ######################################################################



    # TAB4 - Ustawienia ##################################################

    settingsTab = TKttk.Frame(mainMenu)
    settingsTab.config(style = "mainMenuTabFrame.TFrame")
    settingsTabImg = PLimg.open(GUI.R()['settingsTabIcon'])
    settingsTabImg = settingsTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
    settingsTabImg = PLitk.PhotoImage(settingsTabImg)
    mainMenu.add(settingsTab, image = settingsTabImg, state = TK.NORMAL)


    # Nagłówek
    settingsHeader = TKttk.Label(settingsTab)
    settingsHeader.config(style = 'tabHeader.TLabel')
    settingsHeader.config(text = 'USTAWIENIA')
    settingsHeader.pack(fill = TK.X)


    # Zawartość
    settingsFrame = TKttk.Frame(settingsTab)
    settingsFrame.config(style = 'tabFrame.TFrame')
    settingsFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])

    ######################################################################



    # TAB5 - O programie #################################################
    
    aboutTab = TKttk.Frame(mainMenu)
    aboutTab.config(style = "mainMenuTabFrame.TFrame")
    aboutTabImg = PLimg.open(GUI.R()['aboutTabIcon'])
    aboutTabImg = aboutTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
    aboutTabImg = PLitk.PhotoImage(aboutTabImg)
    mainMenu.add(aboutTab, image = aboutTabImg, state = TK.NORMAL)


    # Nagłówek
    aboutHeader = TKttk.Label(aboutTab)
    aboutHeader.config(style = 'tabHeader.TLabel')
    aboutHeader.config(text = 'O PROGRAMIE')
    aboutHeader.pack(fill = TK.X)


    # Zawartość
    aboutFrame = TKttk.Frame(aboutTab)
    aboutFrame.config(style = 'tabFrame.TFrame')
    aboutFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])

    ######################################################################



    # Mainloop
    window.mainloop()
window()