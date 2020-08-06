# Oznaczenia zmiennych:
# K - Klasa
# N - Nazwisko
# I - Imie
# L - Login do librusa





import codecs as cd

def SprawdzKlasa(K):
    if len(K.split(' ')) != 2:                          # Wywołuje błąd jeżeli napis nie dzieli się w pożądanym formacie
        blad = int('x')                                 #

    for x in range(0,10):                               #
        if K[1:].find(str(x)) != -1:                    # Wywołuje bląd jeżeli w nazwie klasy (poza numerem klasy) znajduje się liczba
            blad = int('x')                             #

    numery_niedozwolone = [0,9,8,7,6,5,4]               # Określa numery klas które nie istnieją

    for x in numery_niedozwolone:                       #
        if K[0] == str(x):                              # Wywołuje błąd jeżeli numer klasy jest równy numerowi niedozwolonemu
            blad = int('x')                             #

    szkoly = ['BS', 'LO']                               # Określa istniejące szkoly

    if K.split(' ')[1] not in szkoly:                   # Wywołuje błąd jeżeli szkola nie należy do szkół istniejących
        blad = int('x')                                 #

    oddzialy = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'w', 'y', 'z']       # Określa istniejące oddzialy

    if K[1] not in oddzialy:                            # Wywołuje błąd jeżeli oddział nie należy do oddziałów istniejących
        blad = int('x')                                 #


def SprawdzNazwisko(N):
    for a in N:
        for x in range(0,10):                           #
            if a.find(str(x)) != -1:                    # Wywoluje blad jeżeli nazwisko zawiera liczbę
                blad = int('x')                         #


def SprawdzImie(I):
    for x in range(0,10):                               #
        if I.find(str(x)) != -1:                        # Wywoluje blad jeżeli imie zawiera liczbę
            blad = int('x')                             #


def SprawdzLogin(L, CzyUczen):
    if CzyUczen and L[-1] != 'u':                       # Wywoluje blad jeżeli login ucznia nie zawiera na końcu 'u'
        blad = int('x')                                 #

    if CzyUczen:                                        #
        blad = int(L[:-1])                              # Wywoluje blad jeżeli login (-'u' dla ucznia) nie jest liczbą
    else:                                               #
        blad = int(L)                                   #




def przetworz(dane):
    dane = dane.split('\n\n')                           # dzielenie danych na pojedyńcze osoby

    przetworzone = []                                   # tworzenie kontenera na przetworzone dane

    for osoba in dane:                                  #
        try:                                            #
            x = int(osoba[0])                           #
        except ValueError:                              # Sprawdza czy osoba jest nauczycielem czy uczniem
            CzyUczen = False                            #
        else:                                           #
            CzyUczen = True                             #

        # Dla uczniów
        if CzyUczen:
            K = osoba.split(', ')[0].split(' ')[:2]
            K = K[0] + ' ' + K[1]
            N = osoba.split(', ')[0].split(' ')[2:]
            I = osoba.split(', ')[1].split(' ')[0]
            L = osoba.split(', ')[1].split(' ')[2]

            # Sprawdzenie poprawności
            SprawdzKlasa(K)
            SprawdzNazwisko(N)
            SprawdzImie(I)
            SprawdzLogin(L, CzyUczen)

            dane = [K, N, I, L, CzyUczen]
            przetworzone.append(dane)
        # Dla nauczycieli
        else:
            N = osoba.split(', ')[0].split(' ')
            I = osoba.split(', ')[1].split(' ')[-4]
            L = osoba.split(', ')[1].split(' ')[-2]

            # Sprawdzenie poprawnosci
            SprawdzNazwisko(N)
            SprawdzImie(I)
            SprawdzLogin(L, CzyUczen)

            dane = [N, I, L, CzyUczen]
            przetworzone.append(dane)
    return przetworzone






# Legenda do części dokumentacji poniżej:
# X - Dane nieznaczące
# Q - Pusta linia


# Format danych dla uczniów:
# <Klasa> <Nazwisko>, <Imie> <X> <Login do librusa> <X>
# <Q>

# Przykład:
# 1a BS Nowak, Adam <NieznaczaceDane> 1234567u <NieznaczaceDane>
#


# Format danych dla nauczycieli:
# <Nazwisko>, <Imie> <X> <Login do Librusa> <X>
# <Q>

# Przykład:
# Nowak, Adam <NieznaczaceDane> 1234567 <NieznaczaceDane>
#




# Inne:
# - skrypt akceptuje prefix 'ks.', nieuwzględnia go w przetwarzaniu
# - skrypt akceptuje nazwiska holenderskie (typu 'van X', 'van der X' itp.) i uwzględnia je w przetwarzaniu
# - skrypt nie akceptuje nazwisk złożonych (np. Nowak-Kowalska)
# - skrypt wymaga kodowania ANSI
