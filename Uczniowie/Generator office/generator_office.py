"""
Program generujący plik do importu z danymi potrzebnymi do stworzenia kont office365
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



# START #

plik_konta = open('konta.csv')
plik_lista = open('lista.txt')
office = open('office.csv', 'w')

konta_tab = (plik_konta.read()).split('\n')
emaile = []

for konta_poj in konta_tab:
    poj_email = konta_poj.split(',')[0]
    emaile.append(poj_email)

lista_tab = (plik_lista.read()).split('\n\n')
plik_lista.close()

licznik = 0

for lista_poj in lista_tab:
    lista_poj_tab = lista_poj.split('\n')

    email = emaile[licznik]
    imie = ((lista_poj_tab[1]).split(', '))[1]
    nazwisko = ((lista_poj_tab[1]).split(', '))[0]
    nazwa = imie + ' ' + nazwisko
    stanowisko = 'uczeń'
    klasa = lista_poj_tab[0]
    kraj = 'Rzeczypospolita Polska'

    office.write(email + ',' + imie + ',' + nazwisko + ',' + nazwa + ',' + stanowisko + ',' + klasa + ',,,,,,,,,' + kraj + '\n')

    licznik += 1

office.close()