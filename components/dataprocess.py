import time as TM

def plr(text):
    text1 = text.replace('ę', 'e')
    text2 = text1.replace('ó', 'o')
    text3 = text2.replace('ą', 'a')
    text4 = text3.replace('ś', 's')
    text5 = text4.replace('ł', 'l')
    text6 = text5.replace('ż', 'z')
    text7 = text6.replace('ź', 'z')
    text8 = text7.replace('ć', 'c')
    text9 = text8.replace('ń', 'n')
    text10 = text9.replace('Ę', 'E')
    text11 = text10.replace('Ó', 'O')
    text12 = text11.replace('Ą', 'A')
    text13 = text12.replace('Ś', 'S')
    text14 = text13.replace('Ł', 'L')
    text15 = text14.replace('Ż', 'Z')
    text16 = text15.replace('Ź', 'Z')
    text17 = text16.replace('Ć', 'C')
    text = text17.replace('Ń', 'N')
    return text

def ctc(Klasa):
    czas = TM.localtime()
    miesiac = czas[1]
    if miesiac >= 9:
        rokpodst = czas[0]
    else:
        rokpodst = czas[0] - 1
    nrklasy = int(Klasa[0])
    literaklasy = Klasa[1]
    szkola = Klasa.split(' ')[1]
    if szkola == 'BS':
        znacznik = str((4 - nrklasy) + rokpodst) + szkola
    else:
        znacznik = str((5 - nrklasy) + rokpodst) + literaklasy
    return znacznik