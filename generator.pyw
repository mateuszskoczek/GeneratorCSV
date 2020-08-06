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
    'A0003' : 'Czy chcesz rozpocząć przetwarzanie plików?'
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
#SU.rmtree(str(appdata) + '/Generator CSV')
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
        check = functions.integer('generateFilesLabelWidth')
        if not check[0]:
            return check
        check = functions.fromArray('generateFilesLabelAnchor', ['center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'])
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
        check = functions.integer('GIFSLocalizationEntryWidth')
        if not check[0]:
            return check
        check = functions.integer('GIFFrameSeparators')
        if not check[0]:
            return check
        check = functions.integer('generateInputFilesPlusMinusButtonsWidth')
        if not check[0]:
            return check
        check = functions.integer('generateResetButtonWidth')
        if not check[0]:
            return check
        check = functions.integer('generateInputFilesPadding')
        if not check[0]:
            return check
        check = functions.integer('generateOutputFilesPadding')
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
                        new_contentVar = (content[var])[2:-2].split("', '")
                        check = new_contentVar
                        for x in check:
                            x = x.strip('<enter>')
                            for y in x:
                                if y not in allowedCharactersInSeparator:
                                    return [False, 'Niepoprawne dane - klucz: %s' % var]
                        content[var] = new_contentVar
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





# ---------------------------------- # Przetwarzanie plików # ----------------------------------- #

class dataProcess:
    def start(self, files):
        pass
dataProcess = dataProcess()





# ------------------------------------------- # GUI # ------------------------------------------- #

class mainWindow:
    def __init__(self, master):
        # Okno
        self.master = master
        master.title('%s %s' % (VARS.programName, VARS.programVersion))
        master.geometry('%sx%s' % (str(GUI.R()['windowWidth']), str(GUI.R()['windowHeight'])))
        master.resizable(width = GUI.R()['windowWidthResizable'], height = GUI.R()['windowHeightResizable'])
        master.configure(bg = GUI.R()['windowMainBG'])
        master.iconbitmap(GUI.R()['mainIcon'])




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
                    "foreground": GUI.R()['label1TextColor'],
                    "font": ('Segoe UI', 10)
                },
            },
            "label2.TLabel": {
                "configure": {
                    "background": GUI.R()['label2BG'],
                    "foreground": GUI.R()['label2TextColor'],
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
            "combobox2.TCombobox": {
                "configure": {
                    "arrowcolor": GUI.R()['combobox2ArrowColor'],
                    "background": GUI.R()['combobox2ButtonColor'],
                    "bordercolor": GUI.R()['combobox2BorderColor'],
                    "fieldbackground": GUI.R()['combobox2FieldBackground'],
                    "foreground": GUI.R()['combobox2TextColor'],
                    "relief": GUI.R()['combobox2Relief'],
                    "borderwidth": GUI.R()['combobox2BorderWidth'],
                    "padding": GUI.R()['combobox2Padding'],
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
                    "background": GUI.R()['spinbox1ButtonColor'],
                    "padding" : GUI.R()['spinbox1Padding'],
                },
            },
            "entry1.TEntry": {
                "configure": {
                    "fieldbackground": GUI.R()['entry1FieldBackground'],
                    "relief": GUI.R()['entry1Relief'],
                    "borderwidth": GUI.R()['entry1BorderWidth'],
                    "padding": GUI.R()['entry1Padding'],
                    "foreground": GUI.R()['entry1TextColor'],
                },
            },
        })
        TKttk.Style().theme_use("main")




        # Menu główne
        self.mainMenu = TKttk.Notebook(master, width = master.winfo_width() - (2 * GUI.R()['menuTabsPadding'] + GUI.R()['tabIconsSize']), height = master.winfo_height())
        self.mainMenu.config(style = "mainMenu.TNotebook")
        self.mainMenu.grid(row = 0)

        # Ikona
        self.iconTab = TKttk.Frame(self.mainMenu)
        self.iconTabImg = PLimg.open(GUI.R()['mainIcon'])
        self.iconTabImg = self.iconTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
        self.iconTabImg = PLitk.PhotoImage(self.iconTabImg)
        self.mainMenu.add(self.iconTab, image = self.iconTabImg, state = TK.DISABLED)




        # TAB1 - Generator ####################################################

        self.generateTab = TKttk.Frame(self.mainMenu)
        self.generateTab.config(style = "mainMenuTabFrame.TFrame")
        self.generateTabImg = PLimg.open(GUI.R()['generateTabIcon'])
        self.generateTabImg = self.generateTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
        self.generateTabImg = PLitk.PhotoImage(self.generateTabImg)
        self.mainMenu.add(self.generateTab, image = self.generateTabImg, state = TK.NORMAL)


        # Nagłówek
        self.generateHeader = TKttk.Label(self.generateTab)
        self.generateHeader.config(style = 'tabHeader.TLabel')
        self.generateHeader.config(text = 'GENERATOR CSV')
        self.generateHeader.pack(fill = TK.X)


        # Zawartość
        self.generateFrame = TKttk.Frame(self.generateTab)
        self.generateFrame.config(style = 'tabFrame.TFrame')
        self.generateFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])


        # (1) Pliki #################################################

        self.generateFilesFrame = TKttk.Frame(self.generateFrame)
        self.generateFilesFrame.config(style = 'layoutFrame.TFrame')
        self.generateFilesFrame.pack(fill = TK.BOTH, expand = 1)

        # (2) Pliki wejściowe #############################

        self.generateInputFilesFrame = TKttk.Frame(self.generateFilesFrame)
        self.generateInputFilesFrame.config(style = 'layoutFrame.TFrame')
        self.generateInputFilesFrame.pack(fill = TK.BOTH, expand = 1, padx = 6)

        # (3) Plik źródłowy 1 ###################

        self.GIF1Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF1Frame.config(style = 'layoutFrame.TFrame')
        self.GIF1Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R()['GIFFrameSeparators'])/2))

        # "Plik źródłowy (1)"
        self.GIF1Label = TKttk.Label(self.GIF1Frame)
        self.GIF1Label.config(style = 'label1.TLabel')
        self.GIF1Label.config(width = GUI.R()['generateFilesLabelWidth'])
        self.GIF1Label.config(anchor = GUI.R()['generateFilesLabelAnchor'])
        self.GIF1Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R()['generateInputFilesPadding'])))
        self.GIF1Label.config(text = 'Plik źródłowy (1)')
        self.GIF1Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF1SFrame = TKttk.Frame(self.GIF1Frame)
        self.GIF1SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF1SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF1SLocalizationFrame = TKttk.Frame(self.GIF1SFrame)
        self.GIF1SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF1SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Entry
        self.GIF1SLocalizationEntryVar = TK.StringVar()
        self.GIF1SLocalizationEntry = TKttk.Entry(self.GIF1SLocalizationFrame)
        self.GIF1SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF1SLocalizationEntry.config(textvariable = self.GIF1SLocalizationEntryVar)
        self.GIF1SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Button
        self.GIF1SLocalizationButton = TKttk.Button(self.GIF1SLocalizationFrame)
        self.GIF1SLocalizationButton.config(style = 'button1.TButton')
        self.GIF1SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF1SLocalizationButton.config(command = self.GIF1SLocalizationButtonAction)
        self.GIF1SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R()['generateInputFilesPadding'])

        # Format
        self.GIF1SFormatFrame = TKttk.Frame(self.GIF1SFrame)
        self.GIF1SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF1SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Format - Label
        self.GIF1SFormatLabel = TKttk.Label(self.GIF1SFormatFrame)
        self.GIF1SFormatLabel.config(style = 'label2.TLabel')
        self.GIF1SFormatLabel.config(text = 'Format')
        self.GIF1SFormatLabel.pack(side = TK.LEFT, padx = GUI.R()['generateInputFilesPadding'])

        # Format - Combobox
        self.GIF1SFormatComboboxVar = TK.StringVar()
        self.GIF1SFormatCombobox = TKttk.Combobox(self.GIF1SFormatFrame)
        self.GIF1SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R()['combobox1ListBoxBackground'])
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R()['combobox1ListBoxForeground'])
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R()['combobox1ListBoxSelectBackground'])
        self.GIF1SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R()['combobox1ListBoxSelectForeground'])
        self.GIF1SFormatCombobox.config(state = 'readonly')
        self.GIF1SFormatCombobox.config(textvariable = self.GIF1SFormatComboboxVar)
        self.GIF1SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF1SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        #########################################

        # (3) Plik źródłowy 2 ###################

        self.GIF2Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF2Frame.config(style = 'layoutFrame.TFrame')
        self.GIF2Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R()['GIFFrameSeparators'])/2))

        # "Plik źródłowy (2)"
        self.GIF2Label = TKttk.Label(self.GIF2Frame)
        self.GIF2Label.config(style = 'label1.TLabel')
        self.GIF2Label.config(width = GUI.R()['generateFilesLabelWidth'])
        self.GIF2Label.config(anchor = GUI.R()['generateFilesLabelAnchor'])
        self.GIF2Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R()['generateInputFilesPadding'])))
        self.GIF2Label.config(text = 'Plik źródłowy (2)')
        self.GIF2Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF2SFrame = TKttk.Frame(self.GIF2Frame)
        self.GIF2SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF2SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF2SLocalizationFrame = TKttk.Frame(self.GIF2SFrame)
        self.GIF2SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF2SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Entry
        self.GIF2SLocalizationEntryVar = TK.StringVar()
        self.GIF2SLocalizationEntry = TKttk.Entry(self.GIF2SLocalizationFrame)
        self.GIF2SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF2SLocalizationEntry.config(textvariable = self.GIF2SLocalizationEntryVar)
        self.GIF2SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Button
        self.GIF2SLocalizationButton = TKttk.Button(self.GIF2SLocalizationFrame)
        self.GIF2SLocalizationButton.config(style = 'button1.TButton')
        self.GIF2SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF2SLocalizationButton.config(command = self.GIF2SLocalizationButtonAction)
        self.GIF2SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R()['generateInputFilesPadding'])

        # Format
        self.GIF2SFormatFrame = TKttk.Frame(self.GIF2SFrame)
        self.GIF2SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF2SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Format - Label
        self.GIF2SFormatLabel = TKttk.Label(self.GIF2SFormatFrame)
        self.GIF2SFormatLabel.config(style = 'label2.TLabel')
        self.GIF2SFormatLabel.config(text = 'Format')
        self.GIF2SFormatLabel.pack(side = TK.LEFT, padx = GUI.R()['generateInputFilesPadding'])

        # Format - Combobox
        self.GIF2SFormatComboboxVar = TK.StringVar()
        self.GIF2SFormatCombobox = TKttk.Combobox(self.GIF2SFormatFrame)
        self.GIF2SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R()['combobox1ListBoxBackground'])
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R()['combobox1ListBoxForeground'])
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R()['combobox1ListBoxSelectBackground'])
        self.GIF2SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R()['combobox1ListBoxSelectForeground'])
        self.GIF2SFormatCombobox.config(state = 'readonly')
        self.GIF2SFormatCombobox.config(textvariable = self.GIF2SFormatComboboxVar)
        self.GIF2SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF2SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        #########################################

        # (3) Plik źródłowy 3 ###################

        self.GIF3Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF3Frame.config(style = 'layoutFrame.TFrame')
        self.GIF3Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R()['GIFFrameSeparators'])/2))

        # "Plik źródłowy (3)"
        self.GIF3Label = TKttk.Label(self.GIF3Frame)
        self.GIF3Label.config(style = 'label1.TLabel')
        self.GIF3Label.config(width = GUI.R()['generateFilesLabelWidth'])
        self.GIF3Label.config(anchor = GUI.R()['generateFilesLabelAnchor'])
        self.GIF3Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R()['generateInputFilesPadding'])))
        self.GIF3Label.config(text = 'Plik źródłowy (3)')
        self.GIF3Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF3SFrame = TKttk.Frame(self.GIF3Frame)
        self.GIF3SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF3SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF3SLocalizationFrame = TKttk.Frame(self.GIF3SFrame)
        self.GIF3SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF3SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Entry
        self.GIF3SLocalizationEntryVar = TK.StringVar()
        self.GIF3SLocalizationEntry = TKttk.Entry(self.GIF3SLocalizationFrame)
        self.GIF3SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF3SLocalizationEntry.config(textvariable = self.GIF3SLocalizationEntryVar)
        self.GIF3SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Button
        self.GIF3SLocalizationButton = TKttk.Button(self.GIF3SLocalizationFrame)
        self.GIF3SLocalizationButton.config(style = 'button1.TButton')
        self.GIF3SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF3SLocalizationButton.config(command = self.GIF3SLocalizationButtonAction)
        self.GIF3SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R()['generateInputFilesPadding'])

        # Format
        self.GIF3SFormatFrame = TKttk.Frame(self.GIF3SFrame)
        self.GIF3SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF3SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Format - Label
        self.GIF3SFormatLabel = TKttk.Label(self.GIF3SFormatFrame)
        self.GIF3SFormatLabel.config(style = 'label2.TLabel')
        self.GIF3SFormatLabel.config(text = 'Format')
        self.GIF3SFormatLabel.pack(side = TK.LEFT, padx = GUI.R()['generateInputFilesPadding'])

        # Format - Combobox
        self.GIF3SFormatComboboxVar = TK.StringVar()
        self.GIF3SFormatCombobox = TKttk.Combobox(self.GIF3SFormatFrame)
        self.GIF3SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R()['combobox1ListBoxBackground'])
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R()['combobox1ListBoxForeground'])
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R()['combobox1ListBoxSelectBackground'])
        self.GIF3SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R()['combobox1ListBoxSelectForeground'])
        self.GIF3SFormatCombobox.config(state = 'readonly')
        self.GIF3SFormatCombobox.config(textvariable = self.GIF3SFormatComboboxVar)
        self.GIF3SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF3SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        #########################################

        # (3) Plik źródłowy 4 ###################

        self.GIF4Frame = TKttk.Frame(self.generateInputFilesFrame)
        self.GIF4Frame.config(style = 'layoutFrame.TFrame')
        self.GIF4Frame.pack(fill = TK.X, expand = 1, pady = int((GUI.R()['GIFFrameSeparators'])/2))

        # "Plik źródłowy (4)"
        self.GIF4Label = TKttk.Label(self.GIF4Frame)
        self.GIF4Label.config(style = 'label1.TLabel')
        self.GIF4Label.config(width = GUI.R()['generateFilesLabelWidth'])
        self.GIF4Label.config(anchor = GUI.R()['generateFilesLabelAnchor'])
        self.GIF4Label.config(padding = ('0 0 %s 0' % str(2 * GUI.R()['generateInputFilesPadding'])))
        self.GIF4Label.config(text = 'Plik źródłowy (4)')
        self.GIF4Label.pack(side = TK.LEFT)

        # Plik żródłowy (1) - Ustawienia
        self.GIF4SFrame = TKttk.Frame(self.GIF4Frame)
        self.GIF4SFrame.config(style = 'layoutFrame.TFrame')
        self.GIF4SFrame.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        # Lokalizacja
        self.GIF4SLocalizationFrame = TKttk.Frame(self.GIF4SFrame)
        self.GIF4SLocalizationFrame.config(style = 'layoutFrame.TFrame')
        self.GIF4SLocalizationFrame.pack(side = TK.TOP, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Entry
        self.GIF4SLocalizationEntryVar = TK.StringVar()
        self.GIF4SLocalizationEntry = TKttk.Entry(self.GIF4SLocalizationFrame)
        self.GIF4SLocalizationEntry.config(style = 'entry1.TEntry')
        self.GIF4SLocalizationEntry.config(textvariable = self.GIF4SLocalizationEntryVar)
        self.GIF4SLocalizationEntry.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        # Lokalizacja - Button
        self.GIF4SLocalizationButton = TKttk.Button(self.GIF4SLocalizationFrame)
        self.GIF4SLocalizationButton.config(style = 'button1.TButton')
        self.GIF4SLocalizationButton.config(text = 'Przeglądaj')
        self.GIF4SLocalizationButton.config(command = self.GIF4SLocalizationButtonAction)
        self.GIF4SLocalizationButton.pack(side = TK.RIGHT, padx = GUI.R()['generateInputFilesPadding'])

        # Format
        self.GIF4SFormatFrame = TKttk.Frame(self.GIF4SFrame)
        self.GIF4SFormatFrame.config(style = 'layoutFrame.TFrame')
        self.GIF4SFormatFrame.pack(side = TK.BOTTOM, fill = TK.X, expand = 1, pady = GUI.R()['generateInputFilesPadding'])

        # Format - Label
        self.GIF4SFormatLabel = TKttk.Label(self.GIF4SFormatFrame)
        self.GIF4SFormatLabel.config(style = 'label2.TLabel')
        self.GIF4SFormatLabel.config(text = 'Format')
        self.GIF4SFormatLabel.pack(side = TK.LEFT, padx = GUI.R()['generateInputFilesPadding'])

        # Format - Combobox
        self.GIF4SFormatComboboxVar = TK.StringVar()
        self.GIF4SFormatCombobox = TKttk.Combobox(self.GIF4SFormatFrame)
        self.GIF4SFormatCombobox.config(style = 'combobox1.TCombobox')
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.background", GUI.R()['combobox1ListBoxBackground'])
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.foreground", GUI.R()['combobox1ListBoxForeground'])
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.selectBackground", GUI.R()['combobox1ListBoxSelectBackground'])
        self.GIF4SFormatCombobox.option_add("*TCombobox*Listbox.selectForeground", GUI.R()['combobox1ListBoxSelectForeground'])
        self.GIF4SFormatCombobox.config(state = 'readonly')
        self.GIF4SFormatCombobox.config(textvariable = self.GIF4SFormatComboboxVar)
        self.GIF4SFormatCombobox['values'] = tuple(FMT.getList())
        self.GIF4SFormatCombobox.pack(side = TK.LEFT, expand = 1, fill = TK.X, padx = GUI.R()['generateInputFilesPadding'])

        #########################################

        ###################################################

        # (2) Separator1 ##################################

        self.generateSeparator1 = TKttk.Separator(self.generateFilesFrame)
        self.generateSeparator1.config(style = 'separator1.TSeparator')
        self.generateSeparator1.pack(fill = TK.X, pady = 10)

        ###################################################

        # (2) Pliki wyjściowe #############################
    
        self.generateOutputFilesFrame = TKttk.Frame(self.generateFilesFrame)
        self.generateOutputFilesFrame.config(style = 'layoutFrame.TFrame')
        self.generateOutputFilesFrame.pack(fill = TK.X, pady = 10, padx = 12)

        # (3) Poczta ############################

        self.GOFMailFrame = TKttk.Frame(self.generateOutputFilesFrame)
        self.GOFMailFrame.config(style = 'layoutFrame.TFrame')
        self.GOFMailFrame.pack(pady = GUI.R()['generateOutputFilesPadding'], fill = TK.X, expand = 1)

        # "Poczta"
        self.GOFMailLabel = TKttk.Label(self.GOFMailFrame)
        self.GOFMailLabel.config(style = 'label1.TLabel')
        self.GOFMailLabel.config(width = GUI.R()['generateFilesLabelWidth'])
        self.GOFMailLabel.config(anchor = GUI.R()['generateFilesLabelAnchor'])
        self.GOFMailLabel.config(text = 'Poczta')
        self.GOFMailLabel.pack(side = TK.LEFT)

        # Plik poczty - Lokalizacja (Entry)
        self.GOFMailEntryVar = TK.StringVar()
        self.GOFMailEntry = TKttk.Entry(self.GOFMailFrame)
        self.GOFMailEntry.config(style = 'entry1.TEntry')
        self.GOFMailEntry.config(textvariable = self.GOFMailEntryVar)
        self.GOFMailEntry.pack(padx = 2 * GUI.R()['generateOutputFilesPadding'], side = TK.LEFT, fill = TK.X, expand = 1)

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
        self.GOFOfficeFrame.pack(pady = GUI.R()['generateOutputFilesPadding'], fill = TK.X, expand = 1)

        # "Office"
        self.GOFOfficeLabel = TKttk.Label(self.GOFOfficeFrame)
        self.GOFOfficeLabel.config(style = 'label1.TLabel')
        self.GOFOfficeLabel.config(width = GUI.R()['generateFilesLabelWidth'])
        self.GOFOfficeLabel.config(anchor = GUI.R()['generateFilesLabelAnchor'])
        self.GOFOfficeLabel.config(text = 'Office')
        self.GOFOfficeLabel.pack(side = TK.LEFT)

        # Plik office - Lokalizacja (Entry)
        self.GOFOfficeEntryVar = TK.StringVar()
        self.GOFOfficeEntry = TKttk.Entry(self.GOFOfficeFrame)
        self.GOFOfficeEntry.config(style = 'entry1.TEntry')
        self.GOFOfficeEntry.config(textvariable = self.GOFOfficeEntryVar)
        self.GOFOfficeEntry.pack(padx = 2 * GUI.R()['generateOutputFilesPadding'], side = TK.LEFT, fill = TK.X, expand = 1)

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
        self.generateSeparator2.pack(fill = TK.X, pady = 10)

        #############################################################

        # (1) Przyciski #############################################

        self.generateButtonsFrame = TKttk.Frame(self.generateFrame)
        self.generateButtonsFrame.config(style = 'layoutFrame.TFrame')
        self.generateButtonsFrame.pack(fill = TK.X, pady = 10, padx = 12)

        # Przycisk "START"
        self.generateStartButton = TKttk.Button(self.generateButtonsFrame)
        self.generateStartButton.config(style = 'button1.TButton')
        self.generateStartButton.config(padding = 10)
        self.generateStartButton.config(text = 'START')
        self.generateStartButton.config(command = self.generateStartButtonAction)
        self.generateStartButton.pack(side = TK.LEFT, fill = TK.X, expand = 1)

        ##############################################################

        #######################################################################




        # TAB3 - Format #######################################################

        self.formatTab = TKttk.Frame(self.mainMenu)
        self.formatTab.config(style = "mainMenuTabFrame.TFrame")
        self.formatTabImg = PLimg.open(GUI.R()['formatTabIcon'])
        self.formatTabImg = self.formatTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
        self.formatTabImg = PLitk.PhotoImage(self.formatTabImg)
        self.mainMenu.add(self.formatTab, image = self.formatTabImg, state = TK.NORMAL)


        # Nagłówek
        self.formatHeader = TKttk.Label(self.formatTab)
        self.formatHeader.config(style = 'tabHeader.TLabel')
        self.formatHeader.config(text = 'FORMAT DANYCH')
        self.formatHeader.pack(fill = TK.X)


        # Zawartość
        self.formatFrame = TKttk.Frame(self.formatTab)
        self.formatFrame.config(style = 'tabFrame.TFrame')
        self.formatFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])


        # (1) Ładowanie presetu #####################################

        self.loadingPresetFrame = TKttk.Frame(self.formatFrame)
        self.loadingPresetFrame.config(style = 'layoutFrame.TFrame')
        self.loadingPresetFrame.pack(fill = TK.X, side = TK.TOP, pady = 5, padx = 10)

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
        self.loadingList.option_add("*TCombobox*Listbox.background", GUI.R()['combobox2ListBoxBackground'])
        self.loadingList.option_add("*TCombobox*Listbox.foreground", GUI.R()['combobox2ListBoxForeground'])
        self.loadingList.option_add("*TCombobox*Listbox.selectBackground", GUI.R()['combobox2ListBoxSelectBackground'])
        self.loadingList.option_add("*TCombobox*Listbox.selectForeground", GUI.R()['combobox2ListBoxSelectForeground'])
        self.loadingList.pack(side = TK.LEFT, padx = GUI.R()['loadingListPadX'], fill = TK.X, expand = 1)
        self.loadingList['values'] = tuple(FMT.getList())

        # Przycisk "WCZYTAJ"
        self.loadingButton = TKttk.Button(self.loadingPresetFrame)
        self.loadingButton.config(style = 'button1.TButton')
        self.loadingButton.config(command = self.loadingButtonAction)
        self.loadingButton.config(width = GUI.R()['loadingButtonWidth'])
        self.loadingButton.config(text = 'WCZYTAJ')
        self.loadingButton.pack(side = TK.RIGHT)

        #############################################################

        # (1) Separator 1 ###########################################

        self.formatSeparator1 = TKttk.Separator(self.formatFrame)
        self.formatSeparator1.config(style = 'separator1.TSeparator')
        self.formatSeparator1.config(orient = TK.HORIZONTAL)
        self.formatSeparator1.pack(fill = TK.X, pady = 10)

        #############################################################

        # (1) Edycja presetu ########################################

        self.editingPresetFrame = TKttk.Frame(self.formatFrame)
        self.editingPresetFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetFrame.pack(fill = TK.BOTH, expand = 1, padx = 10)

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
        self.EPOSTypeFrame.pack(fill = TK.X, expand = 1, pady = 5)

        # "Typ osoby"
        self.EPOSTypeLabel = TKttk.Label(self.EPOSTypeFrame)
        self.EPOSTypeLabel.config(style = 'label1.TLabel')
        self.EPOSTypeLabel.config(width = GUI.R()['EPOSLabelWidth'])
        self.EPOSTypeLabel.config(anchor = GUI.R()['EPOSLabelAnchor'])
        self.EPOSTypeLabel.config(text = 'Typ osoby')
        self.EPOSTypeLabel.pack(side = TK.LEFT)

        # Radiobutton
        self.EPOSTypeVar = TK.BooleanVar(value = True)

        self.EPOSTypeStudentRadiobutton = TK.Radiobutton(self.EPOSTypeFrame)
        self.EPOSTypeStudentRadiobutton.config(background = GUI.R()['radiobutton1Background'])
        self.EPOSTypeStudentRadiobutton.config(foreground = GUI.R()['radiobutton1TextColor'])
        self.EPOSTypeStudentRadiobutton.config(selectcolor = GUI.R()['radiobutton1IndicatorBackground'])
        self.EPOSTypeStudentRadiobutton.config(activebackground = GUI.R()['radiobutton1Background'])
        self.EPOSTypeStudentRadiobutton.config(activeforeground = GUI.R()['radiobutton1TextColor'])
        self.EPOSTypeStudentRadiobutton.config(variable = self.EPOSTypeVar)
        self.EPOSTypeStudentRadiobutton.config(value = True)
        self.EPOSTypeStudentRadiobutton.config(state = TK.DISABLED)
        self.EPOSTypeStudentRadiobutton.config(text = 'Uczniowie')
        self.EPOSTypeStudentRadiobutton.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        self.EPOSTypeTeacherRadiobutton = TK.Radiobutton(self.EPOSTypeFrame)
        self.EPOSTypeTeacherRadiobutton.config(background = GUI.R()['radiobutton1Background'])
        self.EPOSTypeTeacherRadiobutton.config(foreground = GUI.R()['radiobutton1TextColor'])
        self.EPOSTypeTeacherRadiobutton.config(selectcolor = GUI.R()['radiobutton1IndicatorBackground'])
        self.EPOSTypeTeacherRadiobutton.config(activebackground = GUI.R()['radiobutton1Background'])
        self.EPOSTypeTeacherRadiobutton.config(activeforeground = GUI.R()['radiobutton1TextColor'])
        self.EPOSTypeTeacherRadiobutton.config(variable = self.EPOSTypeVar)
        self.EPOSTypeTeacherRadiobutton.config(value = False)
        self.EPOSTypeTeacherRadiobutton.config(state = TK.DISABLED)
        self.EPOSTypeTeacherRadiobutton.config(text = 'Nauczyciele')
        self.EPOSTypeTeacherRadiobutton.pack(side = TK.RIGHT, fill = TK.X, expand = 1)
        
        #####################

        # (5) Separator pomiedzy osobami

        self.EPOSPersonSeparatorFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSPersonSeparatorFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSPersonSeparatorFrame.pack(fill = TK.X, expand = 1, pady = 5)
        
        # "Separator pomiędzy osobami"
        self.EPOSPersonSeparatorLabel = TKttk.Label(self.EPOSPersonSeparatorFrame)
        self.EPOSPersonSeparatorLabel.config(style = 'label1.TLabel')
        self.EPOSPersonSeparatorLabel.config(width = GUI.R()['EPOSLabelWidth'])
        self.EPOSPersonSeparatorLabel.config(anchor = GUI.R()['EPOSLabelAnchor'])
        self.EPOSPersonSeparatorLabel.config(text = 'Separator pomiędzy osobami')
        self.EPOSPersonSeparatorLabel.pack(side = TK.LEFT)

        # Entry - Separator pomiedzy osobami
        self.EPOSPersonSeparatorVar = TK.StringVar()
        self.EPOSPersonSeparatorEntry = TKttk.Entry(self.EPOSPersonSeparatorFrame)
        self.EPOSPersonSeparatorEntry.config(style = 'entry1.TEntry')
        self.EPOSPersonSeparatorEntry.config(textvariable = self.EPOSPersonSeparatorVar)
        self.EPOSPersonSeparatorEntry.config(state = TK.DISABLED)
        self.EPOSPersonSeparatorEntry.config(width = GUI.R()['EPOSPersonSeparatorEntryWidth'])
        self.EPOSPersonSeparatorEntry.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        #####################

        # (5) Separator pomiedzy wierszami

        self.EPOSRowSeparatorFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSRowSeparatorFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSRowSeparatorFrame.pack(fill = TK.X, expand = 1, pady = 5)

        # "Separator pomiędzy wierszami"
        self.EPOSRowSeparatorLabel = TKttk.Label(self.EPOSRowSeparatorFrame)
        self.EPOSRowSeparatorLabel.config(style = 'label1.TLabel')
        self.EPOSRowSeparatorLabel.config(width = GUI.R()['EPOSLabelWidth'])
        self.EPOSRowSeparatorLabel.config(anchor = GUI.R()['EPOSLabelAnchor'])
        self.EPOSRowSeparatorLabel.config(text = 'Separator pomiędzy wierszami')
        self.EPOSRowSeparatorLabel.pack(side = TK.LEFT)

        # Entry - Separator pomiedzy wierszami
        self.EPOSRowSeparatorVar = TK.StringVar()
        self.EPOSRowSeparatorEntry = TKttk.Entry(self.EPOSRowSeparatorFrame)
        self.EPOSRowSeparatorEntry.config(style = 'entry1.TEntry')
        self.EPOSRowSeparatorEntry.config(textvariable = self.EPOSRowSeparatorVar)
        self.EPOSRowSeparatorEntry.config(state = TK.DISABLED)
        self.EPOSRowSeparatorEntry.config(width = GUI.R()['EPOSRowSeparatorEntryWidth'])
        self.EPOSRowSeparatorEntry.pack(side = TK.RIGHT, fill = TK.X, expand = 1)

        #####################

        # (5) Separatory pomiedzy danymi

        self.EPOSDataSeparatorFrame = TKttk.Frame(self.editingPresetOSFrame)
        self.EPOSDataSeparatorFrame.config(style = 'layoutFrame.TFrame')
        self.EPOSDataSeparatorFrame.pack(fill = TK.BOTH, expand = 1, pady = 5)

        # "Separatory pomiędzy danymi"
        self.EPOSDataSeparatorLabel = TKttk.Label(self.EPOSDataSeparatorFrame)
        self.EPOSDataSeparatorLabel.config(style = 'label1.TLabel')
        self.EPOSDataSeparatorLabel.config(width = GUI.R()['EPOSLabelWidth'])
        self.EPOSDataSeparatorLabel.config(anchor = GUI.R()['EPOSLabelAnchor'])
        self.EPOSDataSeparatorLabel.config(text = 'Separatory pomiędzy danymi')
        self.EPOSDataSeparatorLabel.pack(side = TK.LEFT)

        # Entry - Separator pomiedzy wierszami
        self.EPOSDataSeparatorText = TK.Text(self.EPOSDataSeparatorFrame)
        self.EPOSDataSeparatorText.config(state = TK.DISABLED)
        self.EPOSDataSeparatorText.config(background = GUI.R()['text1Background'])
        self.EPOSDataSeparatorText.config(foreground = GUI.R()['text1TextColor'])
        self.EPOSDataSeparatorText.config(relief = GUI.R()['text1Relief'])
        self.EPOSDataSeparatorText.pack(side = TK.TOP, fill = TK.BOTH)

        #####################

        ###############################

        # (4) Separator 2 #############

        self.formatSeparator2 = TKttk.Separator(self.editingPresetSettingsFrame)
        self.formatSeparator2.config(style = 'separator1.TSeparator')
        self.formatSeparator2.config(orient = TK.VERTICAL)
        self.formatSeparator2.pack(fill = TK.Y, padx = 12, expand = 1, side = TK.LEFT)

        ###############################

        # (4) Lokalizacja danych ######

        self.editingPresetDLFrame = TKttk.Frame(self.editingPresetSettingsFrame)
        self.editingPresetDLFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetDLFrame.pack(fill = TK.BOTH, side = TK.RIGHT)
        self.editingPresetDLFrame.grid_columnconfigure(1, weight = 1)
        self.editingPresetDLFrame.grid_columnconfigure(2, weight = 1)

        # C1 - "Wiersz"
        self.EPDLC1Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLC1Label.config(style = 'label1.TLabel')
        self.EPDLC1Label.config(text = 'Wiersz')
        self.EPDLC1Label.grid(row = 0, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # C2 - "Pozycja w wierszu"
        self.EPDLC2Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLC2Label.config(style = 'label1.TLabel')
        self.EPDLC2Label.config(justify = TK.CENTER)
        self.EPDLC2Label.config(text = 'Pozycja\nw wierszu')
        self.EPDLC2Label.grid(row = 0, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # W1 - "Login"
        self.EPDLW1Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW1Label.config(style = 'label1.TLabel')
        self.EPDLW1Label.config(text = 'Login')
        self.EPDLW1Label.grid(row = 1, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja loginu (wiersz)
        self.EPDLLoginRowVar = TK.IntVar()
        self.EPDLLoginRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLoginRowSpinbox.config(textvariable = self.EPDLLoginRowVar)
        self.EPDLLoginRowSpinbox.config(from_ = 0)
        self.EPDLLoginRowSpinbox.config(to = 1000000)
        self.EPDLLoginRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLoginRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLoginRowSpinbox.grid(row = 1, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja loginu (pozycja w wierszu)
        self.EPDLLoginPosInRowVar = TK.IntVar()
        self.EPDLLoginPosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLoginPosInRowSpinbox.config(textvariable = self.EPDLLoginPosInRowVar)
        self.EPDLLoginPosInRowSpinbox.config(from_ = 0)
        self.EPDLLoginPosInRowSpinbox.config(to = 1000000)
        self.EPDLLoginPosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLoginPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLoginPosInRowSpinbox.grid(row = 1, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # W2 - "Imię"
        self.EPDLW2Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW2Label.config(style = 'label1.TLabel')
        self.EPDLW2Label.config(text = 'Imię')
        self.EPDLW2Label.grid(row = 2, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja imienia (wiersz)
        self.EPDLFnameRowVar = TK.IntVar()
        self.EPDLFnameRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLFnameRowSpinbox.config(textvariable = self.EPDLFnameRowVar)
        self.EPDLFnameRowSpinbox.config(from_ = 0)
        self.EPDLFnameRowSpinbox.config(to = 1000000)
        self.EPDLFnameRowSpinbox.config(state = TK.DISABLED)
        self.EPDLFnameRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLFnameRowSpinbox.grid(row = 2, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja imienia (pozycja w wierszu)
        self.EPDLFnamePosInRowVar = TK.IntVar()
        self.EPDLFnamePosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLFnamePosInRowSpinbox.config(textvariable = self.EPDLFnamePosInRowVar)
        self.EPDLFnamePosInRowSpinbox.config(from_ = 0)
        self.EPDLFnamePosInRowSpinbox.config(to = 1000000)
        self.EPDLFnamePosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLFnamePosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLFnamePosInRowSpinbox.grid(row = 2, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # W3 - "Nazwisko"
        self.EPDLW3Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW3Label.config(style = 'label1.TLabel')
        self.EPDLW3Label.config(text = 'Nazwisko')
        self.EPDLW3Label.grid(row = 3, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja nazwiska (wiersz)
        self.EPDLLnameRowVar = TK.IntVar()
        self.EPDLLnameRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLnameRowSpinbox.config(textvariable = self.EPDLLnameRowVar)
        self.EPDLLnameRowSpinbox.config(from_ = 0)
        self.EPDLLnameRowSpinbox.config(to = 1000000)
        self.EPDLLnameRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLnameRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLnameRowSpinbox.grid(row = 3, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja nazwiska (pozycja w wierszu)
        self.EPDLLnamePosInRowVar = TK.IntVar()
        self.EPDLLnamePosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLLnamePosInRowSpinbox.config(textvariable = self.EPDLLnamePosInRowVar)
        self.EPDLLnamePosInRowSpinbox.config(from_ = 0)
        self.EPDLLnamePosInRowSpinbox.config(to = 1000000)
        self.EPDLLnamePosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLLnamePosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLLnamePosInRowSpinbox.grid(row = 3, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # W4 - "Szkoła"
        self.EPDLW4Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW4Label.config(style = 'label1.TLabel')
        self.EPDLW4Label.config(text = 'Szkoła')
        self.EPDLW4Label.grid(row = 4, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja nazwiska (wiersz)
        self.EPDLSchoolRowVar = TK.IntVar()
        self.EPDLSchoolRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLSchoolRowSpinbox.config(textvariable = self.EPDLSchoolRowVar)
        self.EPDLSchoolRowSpinbox.config(from_ = 0)
        self.EPDLSchoolRowSpinbox.config(to = 1000000)
        self.EPDLSchoolRowSpinbox.config(state = TK.DISABLED)
        self.EPDLSchoolRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLSchoolRowSpinbox.grid(row = 4, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja nazwiska (pozycja w wierszu)
        self.EPDLSchoolPosInRowVar = TK.IntVar()
        self.EPDLSchoolPosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLSchoolPosInRowSpinbox.config(textvariable = self.EPDLSchoolPosInRowVar)
        self.EPDLSchoolPosInRowSpinbox.config(from_ = 0)
        self.EPDLSchoolPosInRowSpinbox.config(to = 1000000)
        self.EPDLSchoolPosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLSchoolPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLSchoolPosInRowSpinbox.grid(row = 4, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # W5 - "Klasa"
        self.EPDLW5Label = TKttk.Label(self.editingPresetDLFrame)
        self.EPDLW5Label.config(style = 'label1.TLabel')
        self.EPDLW5Label.config(text = 'Klasa')
        self.EPDLW5Label.grid(row = 5, column = 0, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        # Lokalizacja nazwiska (wiersz)
        self.EPDLClassRowVar = TK.IntVar()
        self.EPDLClassRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLClassRowSpinbox.config(textvariable = self.EPDLClassRowVar)
        self.EPDLClassRowSpinbox.config(from_ = 0)
        self.EPDLClassRowSpinbox.config(to = 1000000)
        self.EPDLClassRowSpinbox.config(state = TK.DISABLED)
        self.EPDLClassRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLClassRowSpinbox.grid(row = 5, column = 1, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])

        # Lokalizacja nazwiska (pozycja w wierszu)
        self.EPDLClassPosInRowVar = TK.IntVar()
        self.EPDLClassPosInRowSpinbox = TKttk.Spinbox(self.editingPresetDLFrame)
        self.EPDLClassPosInRowSpinbox.config(textvariable = self.EPDLClassPosInRowVar)
        self.EPDLClassPosInRowSpinbox.config(from_ = 0)
        self.EPDLClassPosInRowSpinbox.config(to = 1000000)
        self.EPDLClassPosInRowSpinbox.config(state = TK.DISABLED)
        self.EPDLClassPosInRowSpinbox.config(style = 'spinbox1.TSpinbox')
        self.EPDLClassPosInRowSpinbox.grid(row = 5, column = 2, padx = GUI.R()['EPDataLocalizationPadX'], pady = GUI.R()['EPDataLocalizationPadY'])
        
        ###############################

        #########################################

        ###################################################

        # (1) Separator 3 ###########################################

        self.formatSeparator3 = TKttk.Separator(self.formatFrame)
        self.formatSeparator3.config(style = 'separator1.TSeparator')
        self.formatSeparator3.config(orient = TK.HORIZONTAL)
        self.formatSeparator3.pack(fill = TK.X, expand = 1, pady = 6)

        #############################################################

        # (2) Przyciski #############################################

        self.editingPresetButtonsFrame = TKttk.Frame(self.formatFrame)
        self.editingPresetButtonsFrame.config(style = 'layoutFrame.TFrame')
        self.editingPresetButtonsFrame.pack(fill = TK.X, expand = 1, side = TK.BOTTOM)

        # Przycisk 'ZAPISZ'
        self.editingPresetSaveButton = TKttk.Button(self.editingPresetButtonsFrame)
        self.editingPresetSaveButton.config(command = self.editingPresetSaveButtonAction)
        self.editingPresetSaveButton.config(state = TK.DISABLED)
        self.editingPresetSaveButton.config(style = 'button1.TButton')
        self.editingPresetSaveButton.config(width = GUI.R()['editingPresetSaveButtonWidth'])
        self.editingPresetSaveButton.config(text = 'ZAPISZ')
        self.editingPresetSaveButton.pack(side = TK.LEFT, expand = 1)

        # Przycisk 'Anuluj'
        self.editingPresetCancelButton = TKttk.Button(self.editingPresetButtonsFrame)
        self.editingPresetCancelButton.config(command = self.editingPresetCancelButtonAction)
        self.editingPresetCancelButton.config(state = TK.DISABLED)
        self.editingPresetCancelButton.config(style = 'button1.TButton')
        self.editingPresetCancelButton.config(width = GUI.R()['editingPresetCancelButtonWidth'])
        self.editingPresetCancelButton.config(text = 'Anuluj')
        self.editingPresetCancelButton.pack(side = TK.RIGHT, expand = 1)

        #############################################################

        ######################################################################




        # TAB3 - Ustawienia ##################################################

        self.settingsTab = TKttk.Frame(self.mainMenu)
        self.settingsTab.config(style = "mainMenuTabFrame.TFrame")
        self.settingsTabImg = PLimg.open(GUI.R()['settingsTabIcon'])
        self.settingsTabImg = self.settingsTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
        self.settingsTabImg = PLitk.PhotoImage(self.settingsTabImg)
        self.mainMenu.add(self.settingsTab, image = self.settingsTabImg, state = TK.NORMAL)


        # Nagłówek
        self.settingsHeader = TKttk.Label(self.settingsTab)
        self.settingsHeader.config(style = 'tabHeader.TLabel')
        self.settingsHeader.config(text = 'USTAWIENIA')
        self.settingsHeader.pack(fill = TK.X)


        # Zawartość
        self.settingsFrame = TKttk.Frame(self.settingsTab)
        self.settingsFrame.config(style = 'tabFrame.TFrame')
        self.settingsFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])

        ######################################################################




        # TAB4 - O programie #################################################
        
        self.aboutTab = TKttk.Frame(self.mainMenu)
        self.aboutTab.config(style = "mainMenuTabFrame.TFrame")
        self.aboutTabImg = PLimg.open(GUI.R()['aboutTabIcon'])
        self.aboutTabImg = self.aboutTabImg.resize((GUI.R()['tabIconsSize'], GUI.R()['tabIconsSize']), PLimg.ANTIALIAS)
        self.aboutTabImg = PLitk.PhotoImage(self.aboutTabImg)
        self.mainMenu.add(self.aboutTab, image = self.aboutTabImg, state = TK.NORMAL)


        # Nagłówek
        self.aboutHeader = TKttk.Label(self.aboutTab)
        self.aboutHeader.config(style = 'tabHeader.TLabel')
        self.aboutHeader.config(text = 'O PROGRAMIE')
        self.aboutHeader.pack(fill = TK.X)


        # Zawartość
        self.aboutFrame = TKttk.Frame(self.aboutTab)
        self.aboutFrame.config(style = 'tabFrame.TFrame')
        self.aboutFrame.pack(fill = TK.BOTH, expand = 1, padx = GUI.R()['tabFramePadding'], pady = GUI.R()['tabFramePadding'])

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
                print('x')
        else:
            return
        
    # Akcje przycisków - TAB2

    def loadingButtonAction(self):
        formatFileContent = FMT.R(self.loadingList.get())
        self.loadingList['state'] = TK.DISABLED
        self.loadingButton['state'] = TK.DISABLED
        self.EPOSTypeVar.set(formatFileContent['student'])
        self.EPOSTypeStudentRadiobutton['state'] = TK.NORMAL
        self.EPOSTypeTeacherRadiobutton['state'] = TK.NORMAL
        self.EPOSPersonSeparatorEntry['state'] = TK.NORMAL
        self.EPOSPersonSeparatorVar.set(formatFileContent['personSeparator'])
        self.EPOSRowSeparatorEntry['state'] = TK.NORMAL
        self.EPOSRowSeparatorVar.set(formatFileContent['rowSeparator'])
        self.EPOSDataSeparatorText['state'] = TK.NORMAL
        self.EPOSDataSeparatorText.insert(TK.END, '\n'.join(formatFileContent['dataSeparators']))
        self.EPDLLoginRowSpinbox['state'] = TK.NORMAL
        self.EPDLLoginRowVar.set(formatFileContent['loginRow'])
        self.EPDLLoginPosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLLoginPosInRowVar.set(formatFileContent['loginPositionInRow'])
        self.EPDLFnameRowSpinbox['state'] = TK.NORMAL
        self.EPDLFnameRowVar.set(formatFileContent['fnameRow'])
        self.EPDLFnamePosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLFnamePosInRowVar.set(formatFileContent['fnamePositionInRow'])
        self.EPDLLnameRowSpinbox['state'] = TK.NORMAL
        self.EPDLLnameRowVar.set(formatFileContent['lnameRow'])
        self.EPDLLnamePosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLLnamePosInRowVar.set(formatFileContent['lnamePositionInRow'])
        self.EPDLSchoolRowSpinbox['state'] = TK.NORMAL
        self.EPDLSchoolRowVar.set(formatFileContent['schoolRow'])
        self.EPDLSchoolPosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLSchoolPosInRowVar.set(formatFileContent['schoolPositionInRow'])
        self.EPDLClassRowSpinbox['state'] = TK.NORMAL
        self.EPDLClassRowVar.set(formatFileContent['classRow'])
        self.EPDLClassPosInRowSpinbox['state'] = TK.NORMAL
        self.EPDLClassPosInRowVar.set(formatFileContent['classPositionInRow'])
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
        self.editingPresetSaveButton['state'] = TK.DISABLED
        self.editingPresetCancelButton['state'] = TK.DISABLED
        self.loadingList['values'] = tuple(FMT.getList())

    def editingPresetSave(self):
        formatFileContentToSave = {
            "student" : self.EPOSTypeVar.get(),
            "personSeparator" : self.EPOSPersonSeparatorEntry.get(),
            "rowSeparator" : self.EPOSRowSeparatorEntry.get(),
            "dataSeparators" : (self.EPOSDataSeparatorText.get("1.0", TK.END)).split('\n')[:-1],
            "loginRow" : int(self.EPDLLoginRowSpinbox.get()),
            "loginPositionInRow" : int(self.EPDLLoginPosInRowSpinbox.get()),
            "fnameRow" : int(self.EPDLFnameRowSpinbox.get()),
            "fnamePositionInRow" : int(self.EPDLFnamePosInRowSpinbox.get()),
            "lnameRow" : int(self.EPDLLnameRowSpinbox.get()),
            "lnamePositionInRow" : int(self.EPDLLnamePosInRowSpinbox.get()),
            "schoolRow" : int(self.EPDLSchoolRowSpinbox.get()),
            "schoolPositionInRow" : int(self.EPDLSchoolPosInRowSpinbox.get()),
            "classRow" : int(self.EPDLClassRowSpinbox.get()),
            "classPositionInRow" : int(self.EPDLClassPosInRowSpinbox.get()),
        }
        if not FMT.W(self.loadingList.get(), formatFileContentToSave):
            return
        self.editingPresetClear()

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




# Inicjacja okna
root = TK.Tk()
windowInit = mainWindow(root)
root.mainloop()