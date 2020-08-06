"""
Program generujący plik do importu z danymi potrzebnymi do stworzenia kont email
Mateusz Skoczek
luty 2019
LO im. T. Kościuszki w Sobolewie
"""



# Funkcje konwertujące litery #

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

    text = duze_na_male(text)
    text = polskie_na_lacinskie(text)
    return text

################################



# Funkcja do tworzenia inicjałów #

def inicjaly(imie, nazwisko):
    nazwisko_tab = nazwisko.split(' ')
    nazwisko_inicjaly = ''
    for fragment_nazwiska in nazwisko_tab:
        nazwisko_inicjaly += fragment_nazwiska[0]
    return imie[0] + nazwisko_inicjaly

##################################



# START #

lista = open('lista.txt')
lista_do_importu_write = open('konta.csv', 'w')


try:
	zawartosc = lista.read()
finally:
	lista.close()

dane_osob = zawartosc.split('\n\n')


for ciag_danych in dane_osob:
    dane = ciag_danych.split('\n')

    klasa = dane[0]
    imie = ((dane[1]).split(', '))[1]
    nazwisko = ((dane[1]).split(', '))[0]
    login = dane[3]

    imie_male = konwersja_liter(imie)
    nazwisko_male = konwersja_liter(nazwisko).replace(' ', '.')

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

    dane_do_konta = imie_male + '.' + nazwisko_male + znacznik_klasy + '@losobolew.pl,' + haslo + ',500\n'

    # <email>,<hasło (login do librusa)>,500

    # email:
    # LO: <imie>.<nazwisko>(<rok_ukończenia_szkoły><litera_klasy>)@losobolew.pl
    # BS: <imie>.<nazwisko>(<rok_ukończenia_szkoły>bs)@losobolew.pl
    # ZSZ: <imie>.<nazwisko>(<rok_ukończenia_szkoły>zsz)@losobolew.pl
    # LOD: <imie>.<nazwisko>(<rok_ukończenia_szkoły>lod)@losobolew.pl

    lista_do_importu_write.write(dane_do_konta)

lista_do_importu_write.close()