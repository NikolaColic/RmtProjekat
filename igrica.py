
import numpy as np;
from tabulate import tabulate;
from colorclass import *;
import time;
import datetime;
import threading;
from multiprocessing import Process;






matricaPocetna =np.array([[Color(u"{bgwhite}{black}{b}"+str(100)+"{/b}{/black}{/bgwhite}"),20,10,10,30,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),Color((u"{bgyellow}{black}{b}"+str(50)+"{/b}{/black}{/bgyellow}"))],
                   [10,30,20,20,20,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),10],
                   [30,10,10,30,10,10,30],
                   [10,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),20,20,20,30,10],
                    [Color((u"{bgyellow}{black}{b}"+str(50)+"{/b}{/black}{/bgyellow}")),Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),30,10,10,20,Color(u"{bgwhite}{black}{b}"+str(100)+"{/b}{/black}{/bgwhite}")]]);











#Pravi se funkcija koja ce omoguci kretanje kroz matricu sa svim mogucim ogranicenjima 1.Gde zelim da se pomerim 2.Trenutna pozicija
#Mozda i matrica da se salje trenutna
def kretanjeMatrica(korak,trenutnaPozicija,mat,listaPosecenih):
    #trenutna se salje kao string sa brojem reda i kolone trenutna pozicija = [1,2] 1-broj reda a 2 broj kolone
    if(trenutnaPozicija["brojVrste"] >= len(mat) or trenutnaPozicija["brojKolone"] >= len(mat[1]) ):
        return False;


    if(korak=="napred"):
        if(trenutnaPozicija["brojVrste"]==0):
            return False;
        if(mat[trenutnaPozicija["brojVrste"]-1][trenutnaPozicija["brojKolone"]]==Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}")):
            return False;
        if(trenutnaPozicija["brojIgraca"]==1):
            for x in listaPosecenih[0]:
                if(x["brojVrste"] == trenutnaPozicija["brojVrste"]-1 and x["brojKolone"] == trenutnaPozicija["brojKolone"]):
                    return False;
        else:
            for x in listaPosecenih[1]:
                if(x["brojVrste"] == trenutnaPozicija["brojVrste"]-1 and x["brojKolone"] == trenutnaPozicija["brojKolone"]):
                    return False;

        trenutnaPozicija["brojVrste"]-=1;
        trenutnaPozicija["vrednostMatrice"]=mat[trenutnaPozicija["brojVrste"]][trenutnaPozicija["brojKolone"]]

        return True;
    if(korak=="desno"):
        if(trenutnaPozicija["brojKolone"]== len(mat[1])-1):
            return False;
        if (mat[trenutnaPozicija["brojVrste"]][trenutnaPozicija["brojKolone"]+1] == Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}")):
            return False;
        if (trenutnaPozicija["brojIgraca"] == 1):
            for x in listaPosecenih[0]:
                if (x["brojVrste"] == trenutnaPozicija["brojVrste"]  and x["brojKolone"] == trenutnaPozicija["brojKolone"]+1):
                    return False;
        else:
            for x in listaPosecenih[1]:
                if (x["brojVrste"] == trenutnaPozicija["brojVrste"] and x["brojKolone"] == trenutnaPozicija["brojKolone"]+1):
                    return False;
        trenutnaPozicija["brojKolone"]+=1;
        trenutnaPozicija["vrednostMatrice"] = mat[trenutnaPozicija["brojVrste"]][trenutnaPozicija["brojKolone"]]

        return True;
    if(korak == "levo"):
        if (trenutnaPozicija["brojKolone"] == 0):
            return False;
        if (mat[trenutnaPozicija["brojVrste"]][trenutnaPozicija["brojKolone"]] == Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}")):
            return False;
        if (trenutnaPozicija["brojIgraca"] == 1):
            for x in listaPosecenih[0]:
                if (x["brojVrste"] == trenutnaPozicija["brojVrste"]  and x["brojKolone"] == trenutnaPozicija["brojKolone"]-1):
                    return False;
        else:
            for x in listaPosecenih[1]:
                if (x["brojVrste"] == trenutnaPozicija["brojVrste"]  and x["brojKolone"] == trenutnaPozicija["brojKolone"]-1):
                    return False;
        trenutnaPozicija["brojKolone"] -= 1;
        trenutnaPozicija["vrednostMatrice"] = mat[trenutnaPozicija["brojVrste"]][trenutnaPozicija["brojKolone"]]

        return True;
    if(korak == "dole"):
        if (trenutnaPozicija["brojVrste"] == len(mat)-1):
            return False;
        if (mat[trenutnaPozicija["brojVrste"] +1][trenutnaPozicija["brojKolone"]] == Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}")):
            return False;
        if (trenutnaPozicija["brojIgraca"] == 1):
            for x in listaPosecenih[0]:
                if (x["brojVrste"] == trenutnaPozicija["brojVrste"] + 1 and x["brojKolone"] == trenutnaPozicija["brojKolone"]):
                    return False;
        else:
            for x in listaPosecenih[1]:
                if (x["brojVrste"] == trenutnaPozicija["brojVrste"] + 1 and x["brojKolone"] == trenutnaPozicija["brojKolone"]):
                    return False;
        trenutnaPozicija["brojVrste"] += 1;
        trenutnaPozicija["vrednostMatrice"] = mat[trenutnaPozicija["brojVrste"] ][trenutnaPozicija["brojKolone"]]

        return True;

def odgovorObrada(odgovor,matrica,pocetnaPozicijaPrvog,pitanje,listaPosecenih,skor):
    korak = {
        1: "napred",
        2: "levo",
        3: "desno",
        4: "dole"
    }
    listaOdgovora = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']
    while (True):
        odgovor = input();
        izlazFor = 0;
        for x in listaOdgovora:
            if (odgovor == x):
                izlazFor = 1;
                break;
        if (izlazFor == 1):
            break;
        print("Pogresno ste uneli odgovor.Pokusajte ponovo")
    if (odgovor.upper() == pitanje["Tacan"]):
        while (True):
            print("Odgovor je tacan");
            if(pocetnaPozicijaPrvog["vrednostMatrice"] == Color(u"{bgred}{black}{b}" + str(skor["vrednostPitanja"])+ "{/b}{/black}{/bgred}")
            or pocetnaPozicijaPrvog["vrednostMatrice"] == Color(u"{bggreen}{black}{b}" + str(skor["vrednostPitanja"]) + "{/b}{/black}{/bggreen}")):
                matrica[pocetnaPozicijaPrvog["brojVrste"]][pocetnaPozicijaPrvog["brojKolone"]] = Color(
                    u"{bgyellow}{black}{b}" + str(skor["vrednostPitanja"])
                    + "{/b}{/black}{/bgyellow}");
            elif (pocetnaPozicijaPrvog["brojIgraca"]== 1):
                matrica[pocetnaPozicijaPrvog["brojVrste"]][pocetnaPozicijaPrvog["brojKolone"]] = Color(
                    u"{bgred}{black}{b}" + str(skor["vrednostPitanja"])
                    + "{/b}{/black}{/bgred}");
                posecenPrvi = {"brojVrste": pocetnaPozicijaPrvog["brojVrste"], "brojKolone": pocetnaPozicijaPrvog["brojKolone"]};
                listaPosecenih[0].append(posecenPrvi);
                skor["prviIgrac"] += skor["vrednostPitanja"];

            else:
                matrica[pocetnaPozicijaPrvog["brojVrste"]][pocetnaPozicijaPrvog["brojKolone"]] = Color(
                    u"{bggreen}{black}{b}" + str(skor["vrednostPitanja"])
                    + "{/b}{/black}{/bggreen}");
                posecenDrugi = {"brojVrste": pocetnaPozicijaPrvog["brojVrste"],
                               "brojKolone": pocetnaPozicijaPrvog["brojKolone"]};
                listaPosecenih[1].append(posecenDrugi);
                skor["drugiIgrac"] += skor["vrednostPitanja"];

            print("Trenutni rezultat je:\n Prvi igrac: "+str(skor["prviIgrac"])+"\n Drugi igrac: "+str(skor["drugiIgrac"]));
            listaPomeraja = [1, 2, 3, 4];
            pomeraj = input(
                "Gde zelite da se pomerite? Unesite broj od jedan do cetiri.\n 1.Napred \n 2.Levo \n 3.Desno \n 4.Dole ");
            izlazWhile = 0;
            for x in listaPomeraja:
                if (pomeraj == str(x)):
                    izlazWhile = 1;
                    break;
            if (izlazWhile == 0):
                print("Pogresno ste uneli broj na koji zelite da se pomerite")
                continue;
            nova = pocetnaPozicijaPrvog;


            bool = kretanjeMatrica(korak[int(pomeraj)], nova, matrica,listaPosecenih);

            matrica[pocetnaPozicijaPrvog["brojVrste"]][pocetnaPozicijaPrvog["brojKolone"]] = Color(
                u"{bgwhite}{black}{b}" + pocetnaPozicijaPrvog["vrednostMatrice"]
                + "{/b}{/black}{/bgwhite}");
            if(bool==False):
                print("Nije moguce se pomeriti ovde");
                continue; #bool uvek ostaje false zato sto prenos po vrednosti

            return matrica;
            break;
    else:
        print("Odgovor nije tacan");
        return matrica;



def tipPitanja(pozicija):
    listaDeset = ["10", Color(u"{bgred}{black}{b}"+str(100)+"{/b}{/black}{/bgred}"), Color(u"{bggreen}{black}{b}" + str(100)+ "{/b}{/black}{/bggreen}"),
                  Color(u"{bgred}{black}{b}"+str(10)+"{/b}{/black}{/bgred}"), Color(u"{bggreen}{black}{b}" + str(10)+ "{/b}{/black}{/bggreen}"),
                  Color(u"{bgwhite}{black}{b}" + str(10)+ "{/b}{/black}{/bgwhite}"),Color(u"{bgwhite}{black}{b}" + str(100)+ "{/b}{/black}{/bgwhite}")];
    listaDvadeset =["20", Color(u"{bgred}{black}{b}"+str(20)+"{/b}{/black}{/bgred}"), Color(u"{bggreen}{black}{b}" + str(20)+ "{/b}{/black}{/bggreen}"),Color(u"{bgwhite}{black}{b}" + str(20)+ "{/b}{/black}{/bgwhite}")];
    listaTrideset =["30", Color(u"{bgred}{black}{b}"+str(30)+"{/b}{/black}{/bgred}"), Color(u"{bggreen}{black}{b}" + str(30)+ "{/b}{/black}{/bggreen}"),Color(u"{bgwhite}{black}{b}" + str(30)+ "{/b}{/black}{/bgwhite}")];
    listaPedeset =["50",Color(u"{bgyellow}{black}{b}"+str(30)+"{/b}{/black}{/bgyellow}"),Color(u"{bgwhite}{black}{b}" + str(50)+ "{/b}{/black}{/bgwhite}")];
    for x in listaDeset:
        if(pozicija["vrednostMatrice"] == x):
            return 10;

    for x in listaDvadeset:
        if (pozicija["vrednostMatrice"] == x):
            return 20;
    for x in listaTrideset:
        if (pozicija["vrednostMatrice"] == x):
            return 30;
    for x in listaPedeset:
        if (pozicija["vrednostMatrice"] == x):
            return 50;

def igrica(matrica): #mora metoda da se pozove koja postavlja pitanje i proverava odgovore i prenos(preko one kategorije i vrednosti
    pitanjePrva = {
        "NazivPitanja": "Koje godine je partizan bio prvak evrope",
        "A": 1991,
        "B": 1992,
        "C": 1993,
        "D": 1994,
        "Tacan": "B",
        "Kategorija": 10}
    pitanjeDruga = {
        "NazivPitanja": "Koliko poena je dao Bogdan bogdanovic u finalnoj seriji za 4 utakmice",
        "A": 121,
        "B": 122,
        "C": 123,
        "D": 124,
        "Tacan": "C",
        "Kategorija": 10}
    pitanjeTreca = {
        "NazivPitanja": "Koji od bivsih kosarkasa Partizana nema jedan prst",
        "A": "Bertans",
        "B": "Lovernj",
        "C": "Westerman",
        "D": "Landale",
        "Tacan": "A",
        "Kategorija": 10}
    timeout = 60 * 15  # [seconds]
    timeout_start = time.time()
    pocetnaPozicijaPrvog = {"brojVrste": 0,
                            "brojKolone": 0,
                            "vrednostMatrice": matrica[0][0],
                            "brojIgraca": 1}
    pocetnaPozicijaDrugog = {"brojVrste": 4,
                            "brojKolone": 6,
                            "vrednostMatrice": matrica[4][6],
                            "brojIgraca": 2}
    listaPosecenihPrvi =[{"brojVrste": pocetnaPozicijaPrvog["brojVrste"],"brojKolone": pocetnaPozicijaPrvog["brojKolone"]}];
    listaPosecenihDrugi=[{"brojVrste": pocetnaPozicijaDrugog["brojVrste"],"brojKolone": pocetnaPozicijaDrugog["brojKolone"]}];
    listaPosecenih =[listaPosecenihPrvi,listaPosecenihDrugi]
    igrac = [pocetnaPozicijaPrvog,pocetnaPozicijaDrugog];
    i=0;
    skor = {"prviIgrac": 0,
            "drugiIgrac": 0}
    while time.time() < timeout_start+timeout: #Ovo je vreme igrice 15 min
        print(tabulate(matrica, tablefmt="fancy_grid"))
        if(i==0):
            print("Na potezu je prvi igrac");
        else:
            print("Na potezu je drugi igrac");
        vremeOdgovora=15;
        vremeStart= time.time();

        while time.time() < vremeStart+vremeOdgovora: #Ovo je vreme za svako pitanje i pomeraj
            pitanje ="";
            if(tipPitanja(igrac[i])==10):
                print(str(pitanjePrva["NazivPitanja"])+"\n A)"+str(pitanjePrva["A"])+"\n B)"+str(pitanjePrva["B"])+"\n C)"+str(pitanjePrva["C"])
                      +"\n D)"+str(pitanjePrva["D"])+"\n Molim Vas odgovorite sa A,B,C,D");
                pitanje = pitanjePrva;
            elif(tipPitanja(igrac[i])==30):
                print(str(pitanjeTreca["NazivPitanja"]) + "\n A)" + str(pitanjeTreca["A"]) + "\n B)" + str(
                    pitanjeTreca["B"]) + "\n C)" + str(pitanjeTreca["C"])
                      + "\n D)" + str(pitanjeTreca["D"]) + "\n Molim Vas odgovorite sa A,B,C,D");
                pitanje = pitanjeTreca;

            elif (tipPitanja(igrac[i]) == 20):
                print(str(pitanjeDruga["NazivPitanja"]) + "\n A)" + str(pitanjeDruga["A"]) + "\n B)" + str(
                    pitanjeDruga["B"]) + "\n C)" + str(pitanjeDruga["C"])
                      + "\n D)" + str(pitanjeDruga["D"]) + "\n Molim Vas odgovorite sa A,B,C,D");
                pitanje = pitanjeDruga;
            elif (tipPitanja(igrac[i]) == 50):
                print(str(pitanjeTreca["NazivPitanja"]) + "\n A)" + str(pitanjeTreca["A"]) + "\n B)" + str(
                    pitanjeTreca["B"]) + "\n C)" + str(pitanjeTreca["C"])
                      + "\n D)" + str(pitanjeTreca["D"]) + "\n Molim Vas odgovorite sa A,B,C,D");
                pitanje = pitanjeTreca;
            skor["vrednostPitanja"] = int(tipPitanja(igrac[i]));
            odgovor =""
            matrica =odgovorObrada(odgovor,matrica,igrac[i],pitanje,listaPosecenih,skor);
            if(i==0):
                i+=1;
            elif(i==1):
                i-=1;


            break;
        if(igrac[0]["brojVrste"]== 4 and igrac[0]["brojKolone"] ==6):
            break;
        if(igrac[1]["brojVrste"]== 0 and igrac[1]["brojKolone"] ==0):
            break;
    if(skor["prviIgrac"]>skor["drugiIgrac"]):
        print("Pobednik je prvi igrac");
    elif(skor["prviIgrac"]<skor["drugiIgrac"]):
        print("Pobednik je drugi igrac");
    else:
        print("Nereseno")

#igrica(matricaPocetna);



#Ovo su dole funkcije sto sam pokusavao za vreme


def vremeIgre():
    prom =datetime.time(0, 15, 0);

    while True:

        print(prom.strftime("%H:%M:%S"));


        if(prom.second == 0):
            prom= datetime.time(0,prom.minute -1,59);
        else:
            prom = datetime.time(0, prom.minute, prom.second-1);
        time.sleep(1);


def vremeOdgovora():
    prom =datetime.time(0, 0, 20);

    while True:

        print(prom.strftime("%H:%M:%S"));



        if(prom.second == 0):
            break;
        else:
            prom = datetime.time(0, prom.minute, prom.second-1);
        time.sleep(1);


def runInParallel(*fns):
      proc = []
      for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
      for p in proc:
            p.join()

#runInParallel(vremeOdgovora(),vremeIgre());
def fun(fun1,fun2):
    fun1=Process(target=fun1);
    fun2 =Process(target=fun2);
    pom = {"bool":False};
    fun1.start(pom);
    if(fun1["bool"]==True):
        fun2.start();

    fun1.join();
    fun2.join();




def izlaz():
    # here goes some long calculation
    global result;
    result=False;
    time.sleep(5)

    # when the calculation is done, the result is stored in a global variable

    result = True



#ovo je za izlaz posle 5 sek
def kao():
    thread = threading.Thread(target=izlaz())
    thread.start()
    #while result ==False:
    while True:
        print("Dobro dosli u igricu")
        time.sleep(1);


