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

    # Generowanie plików
    generateTab = TK.Frame(mainMenu)
    generateTab.config(background = SCvar_gui.color.mainBG)
    generateTabImg = PLimg.open(SCvar_gui.image.generateTab)
    generateTabImg = generateTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    generateTabImg = PLitk.PhotoImage(generateTabImg)
    mainMenu.add(generateTab, image = generateTabImg)

    # Dołączanie do pliku
    linkTab = TK.Frame(mainMenu)
    linkTab.config(background = SCvar_gui.color.mainBG)
    linkTabImg = PLimg.open(SCvar_gui.image.linkTab)
    linkTabImg = linkTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    linkTabImg = PLitk.PhotoImage(linkTabImg)
    mainMenu.add(linkTab, image = linkTabImg)

    # Łączenie plików
    mergeTab = TK.Frame(mainMenu)
    mergeTab.config(background = SCvar_gui.color.mainBG)
    mergeTabImg = PLimg.open(SCvar_gui.image.mergeTab)
    mergeTabImg = mergeTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    mergeTabImg = PLitk.PhotoImage(mergeTabImg)
    mainMenu.add(mergeTab, image = mergeTabImg)

    # Ustawienia
    settingsTab = TK.Frame(mainMenu)
    settingsTab.config(background = SCvar_gui.color.mainBG)
    settingsTabImg = PLimg.open(SCvar_gui.image.settingsTab)
    settingsTabImg = settingsTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    settingsTabImg = PLitk.PhotoImage(settingsTabImg)
    mainMenu.add(settingsTab, image = settingsTabImg)

    # Format danych
    formatTab = TK.Frame(mainMenu)
    formatTab.config(background = SCvar_gui.color.mainBG)
    formatTabImg = PLimg.open(SCvar_gui.image.formatTab)
    formatTabImg = formatTabImg.resize((SCvar_gui.dimension.iconTab, SCvar_gui.dimension.iconTab), PLimg.ANTIALIAS)
    formatTabImg = PLitk.PhotoImage(formatTabImg)
    mainMenu.add(formatTab, image = formatTabImg)

    # Informacje
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




    # SETTINGSTAB
    settingsTabLabel = TK.Label(settingsTab)
    settingsTabLabel.config(text = 'USTAWIENIA')
    settingsTabLabel.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    settingsTabLabel.config(bg = SCvar_gui.color.headerBG)
    settingsTabLabel.config(fg = SCvar_gui.color.headerText)
    settingsTabLabel.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    settingsTabLabel.config(width = SCvar_gui.dimension.tabHeaderWidth)
    settingsTabLabel.grid(row = 0)




    # FORMATTAB
    formatTabLabel = TK.Label(formatTab)
    formatTabLabel.config(text = 'FORMAT DANYCH')
    formatTabLabel.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    formatTabLabel.config(bg = SCvar_gui.color.headerBG)
    formatTabLabel.config(fg = SCvar_gui.color.headerText)
    formatTabLabel.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    formatTabLabel.config(width = SCvar_gui.dimension.tabHeaderWidth)
    formatTabLabel.grid(row = 0)


    # Labelframe - Pliki wejściowe
    inFilesLabelFrame = TK.LabelFrame(formatTab)
    inFilesLabelFrame.config(text = ' Pliki wejściowe ')
    inFilesLabelFrame.config(bg = SCvar_gui.color.mainBG)
    inFilesLabelFrame.config(fg = SCvar_gui.color.lfText)
    inFilesLabelFrame.config(bd = SCvar_gui.dimension.lfBorderwidth)
    inFilesLabelFrame.grid(row = 1, pady = SCvar_gui.dimension.framePadY)

    # UczniowieLABEL
    inStudentsLABEL = TK.Label(inFilesLabelFrame)
    inStudentsLABEL.config(text = 'Uczniowie')
    inStudentsLABEL.config(bg = SCvar_gui.color.mainBG)
    inStudentsLABEL.config(fg = SCvar_gui.color.label1)
    inStudentsLABEL.grid(row = 0, column = 0)

    # Uczniowie inFormatInput
    inStudentsFormatInput = TK.Text(inFilesLabelFrame)
    inStudentsFormatInput.config(bg = SCvar_gui.color.textboxBG)
    inStudentsFormatInput.config(fg = SCvar_gui.color.textboxText)
    inStudentsFormatInput.config(bd = SCvar_gui.dimension.tbBorderwidth)
    inStudentsFormatInput.config(width = SCvar_gui.dimension.tbWidth)
    inStudentsFormatInput.config(height = SCvar_gui.dimension.tbHeight)
    inStudentsFormatInput.grid(row = 1, column = 0, padx = SCvar_gui.dimension.tbPad, pady = SCvar_gui.dimension.tbPad)

    # NauczycieleLABEL
    inTeachersLABEL = TK.Label(inFilesLabelFrame)
    inTeachersLABEL.config(text = 'Nauczyciele')
    inTeachersLABEL.config(bg = SCvar_gui.color.mainBG)
    inTeachersLABEL.config(fg = SCvar_gui.color.label1)
    inTeachersLABEL.grid(row = 0, column = 1)

    # Nauczyciele inFormatInput
    inTeachersFormatInput = TK.Text(inFilesLabelFrame)
    inTeachersFormatInput.config(bg = SCvar_gui.color.textboxBG)
    inTeachersFormatInput.config(fg = SCvar_gui.color.textboxText)
    inTeachersFormatInput.config(bd = SCvar_gui.dimension.tbBorderwidth)
    inTeachersFormatInput.config(width = SCvar_gui.dimension.tbWidth)
    inTeachersFormatInput.config(height = SCvar_gui.dimension.tbHeight)
    inTeachersFormatInput.grid(row = 1, column = 1, padx = SCvar_gui.dimension.tbPad, pady = SCvar_gui.dimension.tbPad)


    # Labelframe - Pliki wejściowe
    outFilesLabelFrame = TK.LabelFrame(formatTab)
    outFilesLabelFrame.config(text = ' Pliki wyjściowe ')
    outFilesLabelFrame.config(bg = SCvar_gui.color.mainBG)
    outFilesLabelFrame.config(fg = SCvar_gui.color.lfText)
    outFilesLabelFrame.config(bd = SCvar_gui.dimension.lfBorderwidth)
    outFilesLabelFrame.grid(row = 2, pady = SCvar_gui.dimension.framePadY)

    # UczniowieLABEL
    outStudentsLABEL = TK.Label(outFilesLabelFrame)
    outStudentsLABEL.config(text = 'Uczniowie')
    outStudentsLABEL.config(bg = SCvar_gui.color.mainBG)
    outStudentsLABEL.config(fg = SCvar_gui.color.label1)
    outStudentsLABEL.grid(row = 0, column = 0)

    # Uczniowie outFormatInput
    outStudentsFormatInput = TK.Entry(outFilesLabelFrame)
    outStudentsFormatInput.config(bg = SCvar_gui.color.textboxBG)
    outStudentsFormatInput.config(fg = SCvar_gui.color.textboxText)
    outStudentsFormatInput.config(bd = SCvar_gui.dimension.tbBorderwidth)
    outStudentsFormatInput.config(width = SCvar_gui.dimension.tbWidth2)
    outStudentsFormatInput.grid(row = 1, column = 0, padx = SCvar_gui.dimension.tbPad, pady = SCvar_gui.dimension.tbPad)

    # NauczycieleLABEL
    outTeachersLABEL = TK.Label(outFilesLabelFrame)
    outTeachersLABEL.config(text = 'Nauczyciele')
    outTeachersLABEL.config(bg = SCvar_gui.color.mainBG)
    outTeachersLABEL.config(fg = SCvar_gui.color.label1)
    outTeachersLABEL.grid(row = 0, column = 1)

    # Nauczyciele outFormatInput
    outTeachersFormatInput = TK.Entry(outFilesLabelFrame)
    outTeachersFormatInput.config(bg = SCvar_gui.color.textboxBG)
    outTeachersFormatInput.config(fg = SCvar_gui.color.textboxText)
    outTeachersFormatInput.config(bd = SCvar_gui.dimension.tbBorderwidth)
    outTeachersFormatInput.config(width = SCvar_gui.dimension.tbWidth2)
    outTeachersFormatInput.grid(row = 1, column = 1, padx = SCvar_gui.dimension.tbPad, pady = SCvar_gui.dimension.tbPad)


    # Frame - Przyciski
    formatButtonsFrame = TK.Frame(formatTab)
    formatButtonsFrame.config(bg = SCvar_gui.color.mainBG)
    formatButtonsFrame.grid(row = 3, pady = SCvar_gui.dimension.framePadY)

    # Zapisz
    saveFormatButton = TK.Button(formatButtonsFrame)
    saveFormatButton.config(text = 'ZAPISZ')
    saveFormatButton.config(bg = SCvar_gui.color.buttonBG)
    saveFormatButton.config(fg = SCvar_gui.color.buttonText)
    saveFormatButton.config(relief = TK.FLAT)
    saveFormatButton.config(activebackground = SCvar_gui.color.buttonBG)
    saveFormatButton.config(activeforeground = SCvar_gui.color.buttonText)
    saveFormatButton.config(height = SCvar_gui.dimension.bnHeight)
    saveFormatButton.config(width = SCvar_gui.dimension.bnWidth)
    saveFormatButton.grid(row = 0, column = 0, padx = 5)

    # Pomoc
    def saveFormatButtonCommand():
        try:
            x = open('format_readme.txt')
        except FileNotFoundError:
            print('x')
        except:
            print('x')
        else:
            OS.system("notepad format_readme.txt")
    instructionFormatButton = TK.Button(formatButtonsFrame)
    instructionFormatButton.config(text = 'POMOC')
    instructionFormatButton.config(bg = SCvar_gui.color.buttonBG)
    instructionFormatButton.config(fg = SCvar_gui.color.buttonText)
    instructionFormatButton.config(relief = TK.FLAT)
    instructionFormatButton.config(activebackground = SCvar_gui.color.buttonBG)
    instructionFormatButton.config(activeforeground = SCvar_gui.color.buttonText)
    instructionFormatButton.config(height = SCvar_gui.dimension.bnHeight)
    instructionFormatButton.config(width = SCvar_gui.dimension.bnWidth2)
    instructionFormatButton.config(command = saveFormatButtonCommand)
    instructionFormatButton.grid(row = 0, column = 1, padx = 5)




    # INFOTAB
    infoTabLabel = TK.Label(infoTab)
    infoTabLabel.config(text = 'INFORMACJE')
    infoTabLabel.config(font = (SCvar_gui.fonts.tabHeader[0], SCvar_gui.fonts.tabHeader[1]))
    infoTabLabel.config(bg = SCvar_gui.color.headerBG)
    infoTabLabel.config(fg = SCvar_gui.color.headerText)
    infoTabLabel.config(bd = SCvar_gui.dimension.tabHeaderHeight)
    infoTabLabel.config(width = SCvar_gui.dimension.tabHeaderWidth)
    infoTabLabel.grid(row = 0)

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
    authorsInfo = TK.Label(infoTab)
    authorsInfo.config(text = SCvar_inf.authors + '\ndla ' + SCvar_inf.school)
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