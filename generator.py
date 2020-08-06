"""
# Generator CSV
# 4.0 Experimental
# by Mateusz Skoczek
# styczeń 2019 - luty 2020
# dla ZSP Sobolew

#
# Główny plik programu
#
"""





# -------------------- # Import bibliotek zewnętrznych # -------------------- #

# Biblioteki główne
import os as OS
import sys as SS
import time as TM



# Framework i inne biblioteki interfejsu graficznego
import tkinter as TK
from tkinter import ttk as TKttk
from tkinter import filedialog as TKfld

try:
    from PIL import ImageTk as PLitk
    from PIL import Image as PLimg
except ModuleNotFoundError:
    OS.system("python -m pip install pip")
    OS.system("python -m pip install Pillow")
    OS.system("cls")
    from PIL import ImageTk as PLitk
    from PIL import Image as PLimg





# ------------------ # Import plików składowych programu # ------------------ #

# Funkcja tworząca plik zawierający logi błędu
def excpt(filename, importingFilename, errorcode, exceptInfo):
    filepath = './crashlogs/crash_' + str(TM.localtime()[2]) + str(TM.localtime()[1]) + str(TM.localtime()[0]) + str(TM.localtime()[3]) + str(TM.localtime()[4]) + str(TM.localtime()[5]) + '.txt'
    try:
        OS.mkdir('./crashlogs')
    except:
        pass
    crashfile = open(filepath, 'w')
    crashfile.write('CRASH!\n')
    crashfile.write('An error occurred while loading the component file: %s\n' % importingFilename)
    crashfile.write('In file: %s\n' % filename)
    crashfile.write('%s\n' % exceptInfo)
    crashfile.write('Errorcode: %s' % errorcode)
    crashfile.close()
    SS.exit(0)



# vars.py
try:
    from src.vars import prgInfo as SCvar_inf
    from src.vars import guiVars as SCvar_gui
except Exception as exceptInfo:
    excpt('generator.py', 'variables.py', 'E000000', exceptInfo) #TODO Kod





# -------------------------------- # Okno # --------------------------------- #

# Budowa okna
def gui():
    # Ustawienia okna
    root = TK.Tk()
    root.title(SCvar_inf.name + " " + SCvar_inf.version)
    root.resizable(width = SCvar_gui.other.windowWidthResize, height = SCvar_gui.other.windowHeightResize)
    root.configure(bg = SCvar_gui.color.mainBG)
    root.iconbitmap(SCvar_gui.image.programIcon)




    # Motyw
    TKttk.Style().theme_create("main", parent = "alt", settings = {
        "mainMenu.TNotebook":{
            "configure": {
                "background": SCvar_gui.color.mainBG,
                "tabposition": SCvar_gui.other.tabPosition,
                "borderwidth": SCvar_gui.dimension.tabWindowBorderWidth,
                }
            },
        "mainMenu.TNotebook.Tab":{
            "configure": {
                "background": SCvar_gui.color.unselectedTabBG,
                "borderwidth": SCvar_gui.dimension.borderTab,
                "padding": SCvar_gui.dimension.iconPaddingTab,
                },
            "map": {
                "background": [("selected", SCvar_gui.color.selectedTabBG), ("disabled", SCvar_gui.color.headerBG)],
                }
            }
        })
    TKttk.Style().theme_use("main")




    # Menu główne
    mainMenu = TKttk.Notebook(root)
    mainMenu.config(style = "mainMenu.TNotebook")
    mainMenu.grid(row = 1)
        
    # TAB1 - Ikona
    iconTab = TK.Frame(mainMenu)
    iconTab.config(background = SCvar_gui.color.mainBG)
    iconTabImg = PLimg.open(SCvar_gui.image.iconTab)
    iconTabImg = iconTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    iconTabImg = PLitk.PhotoImage(iconTabImg)
    mainMenu.add(iconTab, image = iconTabImg, state = TK.DISABLED)

    # TAB2 - Generowanie plików
    generateTab = TK.Frame(mainMenu)
    generateTab.config(background = SCvar_gui.color.mainBG)
    generateTabImg = PLimg.open(SCvar_gui.image.generateTab)
    generateTabImg = generateTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    generateTabImg = PLitk.PhotoImage(generateTabImg)
    mainMenu.add(generateTab, image = generateTabImg)

    # TAB3 - Dołącz do pliku
    linkTab = TK.Frame(mainMenu)
    linkTab.config(background = SCvar_gui.color.mainBG)
    linkTabImg = PLimg.open(SCvar_gui.image.linkTab)
    linkTabImg = linkTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    linkTabImg = PLitk.PhotoImage(linkTabImg)
    mainMenu.add(linkTab, image = linkTabImg)

    # TAB4 - Łączenie plików
    mergeTab = TK.Frame(mainMenu)
    mergeTab.config(background = SCvar_gui.color.mainBG)
    mergeTabImg = PLimg.open(SCvar_gui.image.mergeTab)
    mergeTabImg = mergeTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    mergeTabImg = PLitk.PhotoImage(mergeTabImg)
    mainMenu.add(mergeTab, image = mergeTabImg)

    # TAB5 - Ustawienia
    settingsTab = TK.Frame(mainMenu)
    settingsTab.config(background = SCvar_gui.color.mainBG)
    settingsTabImg = PLimg.open(SCvar_gui.image.settingsTab)
    settingsTabImg = settingsTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    settingsTabImg = PLitk.PhotoImage(settingsTabImg)
    mainMenu.add(settingsTab, image = settingsTabImg)

    # TAB6 - Informacje
    infoTab = TK.Frame(mainMenu)
    infoTab.config(background = SCvar_gui.color.mainBG)
    infoTabImg = PLimg.open(SCvar_gui.image.infoTab)
    infoTabImg = infoTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    infoTabImg = PLitk.PhotoImage(infoTabImg)
    mainMenu.add(infoTab, image = infoTabImg)




    # TAB2
    tab2Label = TK.Label(generateTab)
    tab2Label.config(text = 'GENEROWANIE PLIKÓW CSV')
    tab2Label.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    tab2Label.config(bg = SCvar_gui.color.headerBG)
    tab2Label.config(fg = SCvar_gui.color.headerText)
    tab2Label.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    tab2Label.config(width = SCvar_gui.dimension.tabHeaderWidth)
    tab2Label.grid(row = 0)




    # TAB3
    tab3Label = TK.Label(linkTab)
    tab3Label.config(text = 'DOŁĄCZANIE DO PLIKU CSV')
    tab3Label.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    tab3Label.config(bg = SCvar_gui.color.headerBG)
    tab3Label.config(fg = SCvar_gui.color.headerText)
    tab3Label.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    tab3Label.config(width = SCvar_gui.dimension.tabHeaderWidth)
    tab3Label.grid(row = 0)




    # TAB4
    tab4Label = TK.Label(mergeTab)
    tab4Label.config(text = 'ŁĄCZENIE PLIKÓW CSV')
    tab4Label.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    tab4Label.config(bg = SCvar_gui.color.headerBG)
    tab4Label.config(fg = SCvar_gui.color.headerText)
    tab4Label.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    tab4Label.config(width = SCvar_gui.dimension.tabHeaderWidth)
    tab4Label.grid(row = 0)




    # TAB5
    tab5Label = TK.Label(settingsTab)
    tab5Label.config(text = 'USTAWIENIA')
    tab5Label.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    tab5Label.config(bg = SCvar_gui.color.headerBG)
    tab5Label.config(fg = SCvar_gui.color.headerText)
    tab5Label.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    tab5Label.config(width = SCvar_gui.dimension.tabHeaderWidth)
    tab5Label.grid(row = 0)




    # TAB6
    tab6Label = TK.Label(infoTab)
    tab6Label.config(text = 'INFORMACJE')
    tab6Label.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    tab6Label.config(bg = SCvar_gui.color.headerBG)
    tab6Label.config(fg = SCvar_gui.color.headerText)
    tab6Label.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    tab6Label.config(width = SCvar_gui.dimension.tabHeaderWidth)
    tab6Label.grid(row = 0)

    # Separator1
    separator1 = TK.Label(infoTab)
    separator1.config(bg = SCvar_gui.color.mainBG)
    separator1.config(height = SCvar_gui.dimension.separator1Height)
    separator1.grid(row = 1)
    
    # Ikona
    programIcon = PLimg.open(SCvar_gui.image.programIconOther)
    programIcon = programIcon.resize((SCvar_gui.dimension.programIconInInfo, SCvar_gui.dimension.programIconInInfo), PLimg.ANTIALIAS)
    programIcon = PLitk.PhotoImage(programIcon)
    programIconPlace = TK.Label(infoTab)
    programIconPlace.config(image = programIcon)
    programIconPlace.config(background = SCvar_gui.color.mainBG)
    programIconPlace.config(height = SCvar_gui.dimension.programIconInInfoPlace)
    programIconPlace.grid(row = 2)

    # Nazwa programu
    programName = TK.Label(infoTab)
    programName.config(text = SCvar_inf.name)
    programName.config(font = (SCvar_gui.fonts.info1[0], SCvar_gui.fonts.info1[1]))
    programName.config(background = SCvar_gui.color.mainBG)
    programName.config(foreground = SCvar_gui.color.headerText)
    programName.grid(row = 3)

    # Wersja programu
    programVersion = TK.Label(infoTab)
    programVersion.config(text = 'Wersja ' + SCvar_inf.version)
    programVersion.config(font = (SCvar_gui.fonts.info1[0], SCvar_gui.fonts.info1[2]))
    programVersion.config(background = SCvar_gui.color.mainBG)
    programVersion.config(foreground = SCvar_gui.color.headerText)
    programVersion.grid(row = 4)

    # Separator2
    separator2 = TK.Label(infoTab)
    separator2.config(bg = SCvar_gui.color.mainBG)
    separator2.config(height = SCvar_gui.dimension.separator2Height)
    separator2.grid(row = 5)

    # Copyright
    copyrightInfo = TK.Label(infoTab)
    copyrightInfo.config(text = '© ' + SCvar_inf.years)
    copyrightInfo.config(font = (SCvar_gui.fonts.info1[0], SCvar_gui.fonts.info1[3]))
    copyrightInfo.config(background = SCvar_gui.color.mainBG)
    copyrightInfo.config(foreground = SCvar_gui.color.headerText)
    copyrightInfo.grid(row = 6)

    # Autorzy
    authors = ''
    for x in SCvar_inf.authors:
        authors += (x + '\n')
    authors += ('dla ' + SCvar_inf.school)
    authorsInfo = TK.Label(infoTab)
    authorsInfo.config(text = authors)
    authorsInfo.config(font = (SCvar_gui.fonts.info1[0], SCvar_gui.fonts.info1[4]))
    authorsInfo.config(background = SCvar_gui.color.mainBG)
    authorsInfo.config(foreground = SCvar_gui.color.headerText)
    authorsInfo.grid(row = 7)

    # Separator3
    separator3 = TK.Label(infoTab)
    separator3.config(bg = SCvar_gui.color.mainBG)
    separator3.config(height = SCvar_gui.dimension.separator3Height)
    separator3.grid(row = 8)
    



    # Mainloop
    root.mainloop()


# Inicjacja okna
gui()