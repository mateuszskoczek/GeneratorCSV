"""
Generator plików csv dla office i losobolew
Mateusz Skoczek
Zespół Szkół Ponadgimnazjalnych im. T. Kościuszki w Sobolewie
luty 2019
"""




## Import bibliotek ##


import time as tm
import codecs as cd

######################




## Określanie kodowania plików ##


code = 'utf-8'

#################################




## Funkcje ##


# Konwertowanie liter #

def duze_na_male(text):
    # Funkcja zmienia duże litery na małe

    return text.lower()

def polskie_na_lacinskie(text):
    # Funkcja zamienia małe polskie litery na małe łacińskie litery
    # oraz duże polskie litery na małe łacińskie litery

    text1 = text.replace('ę', 'e')
    text2 = text1.replace('ó', 'o')
    text3 = text2.replace('ą', 'a')
    text4 = text3.replace('ś', 's')
    text5 = text4.replace('ł', 'l')
    text6 = text5.replace('ż', 'z')
    text7 = text6.replace('ź', 'z')
    text8 = text7.replace('ć', 'c')
    text9 = text8.replace('ń', 'n')
    text10 = text9.replace('Ę', 'e')
    text11 = text10.replace('Ó', 'o')
    text12 = text11.replace('Ą', 'a')
    text13 = text12.replace('Ś', 's')
    text14 = text13.replace('Ł', 'l')
    text15 = text14.replace('Ż', 'z')
    text16 = text15.replace('Ź', 'z')
    text17 = text16.replace('Ć', 'c')
    text = text17.replace('Ń', 'n')
    return text

def konwersja_liter(text):
    # Funkcja zamienia jednocześnie duże litery na małe oraz polskie na łacińskie
    # Wymaga funkcji: 'duze_na_male' i 'polskie_na_lacinskie'

    text = duze_na_male(text)
    text = polskie_na_lacinskie(text)
    return text


# Funkcje tworzące #

def inicjaly(imie, nazwisko):
    # Funkcja tworzy inicjały z podanego imienia i nazwiska

    nazwisko_tab = nazwisko.split(' ')
    nazwisko_inicjaly = ''
    for fragment_nazwiska in nazwisko_tab:
        nazwisko_inicjaly += fragment_nazwiska[0]
    return imie[0] + nazwisko_inicjaly


# Inne #

def ostrzezenie(czy_uczniowie):
    # Ostrzeżenie przed rozpoczęciem generowania plików

    if czy_uczniowie == True:
        print("Upewnij się, że w folderze 'pliki_zrodlowe' znajduje się plik 'lista.txt' z danymi uczniów")
    else:
        print("Upewnij się, że w folderze 'pliki_zrodlowe' znajduje się plik 'lista nauczycieli.txt' z danymi nauczycieli")
    print("Jeżeli w folderze 'pliki_wyjsciowe' znajdują się pliki 'konta.csv' i 'office.csv' zostaną one usunięte")
    print()
    czekaj = input('Naciśnij ENTER, gdy będziesz gotowy')

#############




## Komponenty ##

def uczniowie():
    ostrzezenie(True)


    try:
        listatxt = open('pliki_zrodlowe/lista.txt')
    except FileNotFoundError:
        print()
        print("BŁĄD! Plik 'lista.txt' nie został znaleziony")
        print()
        print()
        print('############################')
        print()
        print()

        uczniowie()


    try:
        zawartosc_lista = listatxt.read()
    finally:
        listatxt.close()

    kontacsv = cd.open('pliki_wyjsciowe/konta.csv', 'w', code)
    officecsv = cd.open('pliki_wyjsciowe/office.csv', 'w', code)

    ciagi_danych_lista = zawartosc_lista.split('\n\n')

    for ciag_danych in ciagi_danych_lista:
        dane = ciag_danych.split('\n')

        klasa = dane[0]
        imie = ((dane[1]).split(', '))[1]
        nazwisko = ((dane[1]).split(', '))[0]
        login = dane[3]

        imie_male = konwersja_liter(imie)
        nazwisko_male = konwersja_liter(nazwisko).replace(' ', '.')

        rok = tm.localtime()[0]
        nr_klasy = klasa[0]
        lit_klasy = klasa[1]
        szkola = klasa.split(' ')[1]

        if klasa[3:] == 'LO':
            numer_klasy = int(klasa[0])

            if numer_klasy == 1:
                rok_ukoncz = '2021'
            elif numer_klasy == 2:
                rok_ukoncz = '2020'
            elif numer_klasy == 3:
                rok_ukoncz = '2019'

            znacznik_klasy = rok_ukoncz + klasa[1]
        elif klasa[3:] == 'BS':
            numer_klasy = int(klasa[0])

            if numer_klasy == 1:
                rok_ukoncz = '2021'
            elif numer_klasy == 2:
                rok_ukoncz = '2020'
            elif numer_klasy == 3:
                rok_ukoncz = '2019'

            znacznik_klasy = rok_ukoncz + 'bs'
        elif klasa[3:] == 'ZSZ':
            znacznik_klasy = '2019zsz'
        elif klasa[3:] == 'LOD':
            numer_klasy = int(klasa[0])

            if numer_klasy == 3:
                rok_ukoncz = '2020'
            elif numer_klasy == 5:
                rok_ukoncz = '2019'

            znacznik_klasy = rok_ukoncz + 'lod'

        haslo = login + ':' + inicjaly(imie, nazwisko)

        email = imie_male + '.' + nazwisko_male + znacznik_klasy + '@losobolew.pl'

        dane_do_konta = email + ',' + haslo + ',500\n'

        # <email>,<hasło (login do librusa)>,500

        # email:
        # LO: <imie>.<nazwisko>(<rok_ukończenia_szkoły><litera_klasy>)@losobolew.pl
        # BS: <imie>.<nazwisko>(<rok_ukończenia_szkoły>bs)@losobolew.pl
        # ZSZ: <imie>.<nazwisko>(<rok_ukończenia_szkoły>zsz)@losobolew.pl
        # LOD: <imie>.<nazwisko>(<rok_ukończenia_szkoły>lod)@losobolew.pl

        kontacsv.write(dane_do_konta)


        ##############


        nazwa = imie + ' ' + nazwisko
        stanowisko = 'uczeń'
        kraj = 'Rzeczpospolita Polska'

        officecsv.write(email + ',' + imie + ',' + nazwisko + ',' + nazwa + ',' + stanowisko + ',' + klasa + ',,,,,,,,,' + kraj + '\n')
    kontacsv.close()
    officecsv.close()

    print()
    print()
    print('############################')
    print()
    print()

    print('Pliki zostały wygenerowane pomyślnie')
    print()
    czekaj = input('Naciśnij ENTER aby wyjść')

def nauczyciele():
    ostrzezenie(False)


    try:
        listatxt = open('pliki_zrodlowe/lista nauczycieli.txt')
    except FileNotFoundError:
        print()
        print("BŁĄD! Plik 'lista nauczycieli.txt' nie został znaleziony")
        print()
        print()
        print('############################')
        print()
        print()

        nauczyciele()


    try:
        zawartosc_lista = listatxt.read()
    finally:
        listatxt.close()

    kontacsv = cd.open('pliki_wyjsciowe/konta.csv', 'w', code)
    officecsv = cd.open('pliki_wyjsciowe/office.csv', 'w', code)

    ciagi_danych_lista = zawartosc_lista.split('\n\n')

    for ciag_danych in ciagi_danych_lista:
        ciag_danych = ciag_danych.strip('*')
        nazwisko_i_reszta = ciag_danych.split(', ')
        nazwisko = nazwisko_i_reszta[0]
        nazwisko_male = konwersja_liter(nazwisko).replace(' ', '.')
        reszta = nazwisko_i_reszta[1].split(' ')
        imie = reszta[-4]
        imie_male = konwersja_liter(imie)
        haslo = reszta[-2] + ':' + inicjaly(imie, nazwisko)
        email = imie_male + '.' + nazwisko_male + '@losobolew.pl'

        kontacsv.write(email + ',' + haslo + ',500\n')


        #################


        nazwa = imie + ' ' + nazwisko
        stanowisko = 'nauczyciel'
        kraj = 'Rzeczpospolita Polska'

        officecsv.write(email + ',' + imie + ',' + nazwisko + ',' + nazwa + ',' + stanowisko + ',,,,,,,,,,' + kraj + '\n')
    kontacsv.close()
    officecsv.close()

    print()
    print()
    print('############################')
    print()
    print()

    print('Pliki zostały wygenerowane pomyślnie')
    print()
    czekaj = input('Naciśnij ENTER aby wyjść')

################




## START ##

print('### GENERATOR PLIKÓW CSV ###')
print()
print('1 - Uczniowie')
print('2 - Nauczyciele')
print()
wybor = input('Wybór: ')
print()
print()
print('############################')
print()
print()

if wybor == '1':
    uczniowie()
else:
    nauczyciele()