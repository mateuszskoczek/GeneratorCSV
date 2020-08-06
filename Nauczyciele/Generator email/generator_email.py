"""
Program generujący plik do importu z danymi potrzebnymi do stworzenia kont email (nauczyciele)
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

###############################



# Funkcja do tworzenia inicjałów #

def inicjaly(imie, nazwisko):
    nazwisko_tab = nazwisko.split(' ')
    nazwisko_inicjaly = ''
    for fragment_nazwiska in nazwisko_tab:
        nazwisko_inicjaly += fragment_nazwiska[0]
    return imie[0] + nazwisko_inicjaly

##################################



# START #

lista = open('lista nauczycieli.txt')
lista_do_importu_write = open('konta.csv', 'w')


try:
	zawartosc = lista.read()
finally:
	lista.close()


dane_osob = zawartosc.split('\n\n')


for ciag_danych in dane_osob:
    ciag_danych = ciag_danych.strip('*')
    nazwisko_i_reszta = ciag_danych.split(', ')
    nazwisko = nazwisko_i_reszta[0]
    nazwisko_male = konwersja_liter(nazwisko).replace(' ', '.')
    reszta = nazwisko_i_reszta[1].split(' ')
    imie = reszta[-4]
    imie_male = konwersja_liter(imie)
    haslo = reszta[-2] + ':' + inicjaly(imie, nazwisko)

    lista_do_importu_write.write(imie_male + '.' + nazwisko_male + '@losobolew.pl,' + haslo + ',500\n')

lista_do_importu_write.close()
