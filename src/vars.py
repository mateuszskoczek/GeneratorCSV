"""
# Generator CSV
# 4.0 Experimental
# by Mateusz Skoczek
# styczeń 2019 - luty 2020
# dla ZSP Sobolew

#
# Zmienne
#
"""





# ----------------------- # Informacje o programie # ------------------------ #

class prgInfo:
    name = 'Generator CSV'  # Nazwa programu
    school = 'ZSP Sobolew'  # Nazwa szkoły
    version = '4.0 Experimental'  # Wersja programu
    years = '2019 - 2020'  # Lata pracy na programem
    authors = ['Mateusz Skoczek']  # Autorzy





# ------------------- # Zmienne środowiska graficznego # -------------------- #

class guiVars:
    # Wymiary
    class dimension:
        # Karty
        iconTab = 20  # Wielkość ikon w kartach
        borderTab = 0  # Szerokość ramki kart
        iconPaddingTab = 8  # Margines kart
        tabWindowBorderWidth = 0  # Szerokość ramki okna kart

        # Nagłówki kart
        tabHeaderHeight = 8  # Wysokość nagłówka
        tabHeaderWidth = 80  # Szerokość nagłówka

        # Informacje
        programIconInInfo = 100  # Szerokość/wysokość ikony
        programIconInInfoPlace = 150  # Wysokość kontrolki zawierającej ikonę
        separator1Height = 2  # Wysokość separator1
        separator2Height = 1  # Wysokość separator2
        separator3Height = 4  # Wysokość separator3


    # Kolory
    class color:
        # Głowne
        mainBG = '#21242D'  # Głowne tło

        # Karty
        unselectedTabBG = '#21242D'  # Niewybrana karta 
        selectedTabBG = '#333842'  # Wybrana karta

        # Nagłowki kart
        headerBG = '#282C34'  # Tło
        headerText = '#C0C0C0'  # Tekst


    # Grafika
    class image:
        # Ikona programu
        programIcon = 'assets/icon.ico'
        programIconOther = 'assets/other_images/icon.png'

        # Ikony kart
        iconTab = 'assets/tab_icons/icon.png'
        generateTab = 'assets/tab_icons/generate.png'
        linkTab = 'assets/tab_icons/link.png'
        mergeTab = 'assets/tab_icons/merge.png'
        settingsTab = 'assets/tab_icons/settings.png'
        infoTab = 'assets/tab_icons/info.png'
    

    # Czcionki
    class fonts:
        # Główne
        tabHeader = ['Segoe UI', 12]  # Nagłowki

        # Informacje
        info1 = ['Segoe UI']  # Czcionka
        info1.append(20)  # Wielkość tekstu - Nazwa programu
        info1.append(10)  # Wielkość tekstu - Wersja programu
        info1.append(8)  # Wielkość tekstu - Copyright
        info1.append(8)  # Wielkość tekstu - Autorzy


    # Inne
    class other:
        # Ustawienia okna
        windowHeightResize = False  # Rozszerzanie okna w pionie
        windowWidthResize = False  # Rozszerzanie okna w poziomie

        # Ustawienia kart
        tabPosition = 'wn'  # Pozycja kart