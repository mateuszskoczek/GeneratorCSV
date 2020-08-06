import dataprocess as MDdtp
import load_config as MDlcg
import dialog as MDdlg
import codecs as CD

I002 = ['Operacja zakończona pomyślnie', False]

def do(KontenerDanych, sciezkaExport):
    KontenerEmail = []
    KontenerOffice = []
    for osoba in KontenerDanych:
        if osoba[-1]:
            Klasa = osoba[0]
            Imie = osoba[2]
            Inicjaly = Imie[0]
            Nazwisko = ''
            NazwiskoDoEmaila = ''
            for x in osoba[1]:
                Nazwisko += x + ' '
                NazwiskoDoEmaila += ('.' + x)
                Inicjaly += x[0]
            Nazwisko = Nazwisko[:-1]
            ZnacznikKlasy = MDdtp.ctc(Klasa)
            Login = osoba[3]
            Adres = MDdtp.plr(Imie).lower() + MDdtp.plr(NazwiskoDoEmaila).lower() + ZnacznikKlasy + '@losobolew.pl'
            Email = Adres + ',' + Login + ':' + MDdtp.plr(Inicjaly) + ',500'
            Office = Adres + ',' + Imie + ',' + Nazwisko + ',' + Imie + ' ' + Nazwisko + ',uczeń,' + Klasa + ',,,,,,,,,Rzeczypospolita Polska'
            KontenerEmail.append(Email)
            KontenerOffice.append(Office)
        else:
            Imie = osoba[1]
            Inicjaly = Imie[0]
            Nazwisko = ''
            NazwiskoDoEmaila = ''
            for x in osoba[0]:
                Nazwisko += x + ' '
                NazwiskoDoEmaila += ('.' + x)
                Inicjaly += x[0]
            Nazwisko = Nazwisko[:-1]
            Login = osoba[2]
            Adres = MDdtp.plr(Imie).lower() + MDdtp.plr(NazwiskoDoEmaila).lower() + '@losobolew.pl'
            Email = Adres + ',' + Login + ':' + MDdtp.plr(Inicjaly) + ',500'
            Office = Adres + ',' + Imie + ',' + Nazwisko + ',' + Imie + ' ' + Nazwisko + ',nauczyciel,,,,,,,,,,Rzeczpospolita Polska'
            KontenerEmail.append(Email)
            KontenerOffice.append(Office)
    sciezkaEmail = sciezkaExport + '/email.csv'
    sciezkaOffice = sciezkaExport + '/office.csv'
    with CD.open(sciezkaEmail, 'w', MDlcg.read()[1]) as plikEmail:
        for x in KontenerEmail:
            plikEmail.writelines(x + '\n')
        plikEmail.close()
    with CD.open(sciezkaOffice, 'w', MDlcg.read()[1]) as plikOffice:
        for x in KontenerOffice:
            plikOffice.writelines(x + '\n')
        plikOffice.close()
    MDdlg.Inf(I002)