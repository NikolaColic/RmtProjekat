import numpy as np;
from tabulate import tabulate;
from colorclass import *;
import time;
from socket import *
from threading import *
from osoba import *
from sqlite_demo import *;



matricaPocetna =np.array([[Color(u"{bgwhite}{black}{b}"+str(100)+"{/b}{/black}{/bgwhite}"),20,10,10,30,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),50],
                   [10,30,20,20,20,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),10],
                   [30,10,10,30,10,10,30],
                   [10,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),20,20,20,30,10],
                    [50,Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}"),30,10,10,20,Color(u"{bgwhite}{black}{b}"+str(100)+"{/b}{/black}{/bgwhite}")]]);

#Pravi se funkcija koja ce omoguci kretanje kroz matricu sa svim mogucim ogranicenjima 1.Gde zelim da se pomerim 2.Trenutna pozicija
#Mozda i matrica da se salje trenutna
def slanjeSvimIgracima(igraci,poruka):
    for x in igraci:
        x["igrac"].client_socket.send(poruka.encode());
def slanjePrvomIgracu(igraci,poruka):
    igraci[0]["igrac"].client_socket.send(poruka.encode());
def slanjeDrugomIgracu(igraci,poruka):
    igraci[1]["igrac"].client_socket.send(poruka.encode());
def slanjeIgracuBezPoteza(igraci,nekiIgrac,poruka):

    if(igraci[0]["brojIgraca"] == nekiIgrac["brojIgraca"]):
        igraci[1]["igrac"].client_socket.send(poruka.encode());
    else:
        igraci[0]["igrac"].client_socket.send(poruka.encode());


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
        if (mat[trenutnaPozicija["brojVrste"]][trenutnaPozicija["brojKolone"]-1] == Color(u"{bgblue}{black}{b}"+"   "+"{/b}{/black}{/bgblue}")):
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



def istekloVreme():
    pomocna["vrednost"]=True;



pomocna = {
        "vrednost": False
    }

def funkcijaObradaException(exc,igraci,bool):
    if (exc == igraci[0]["igrac"].client_socket):
        igraci[0]["igrac"].client_socket.send("Cestitamo. Vi ste pobedili".encode());
        azuriraj(igraci[0]["igrac"].username, skor["drugiIgracSkor"], 1)
        bool =True;
        return;

    else:
        igraci[1]["igrac"].client_socket.send("Cestitamo. Vi ste pobedili".encode());
        azuriraj(igraci[1]["igrac"].username, skor["drugiIgracSkor"], 1)
        bool =True;
        return;

def odgovorObrada(odgovor,matrica,pocetnaPozicijaPrvog,pitanje,listaPosecenih,skor,igraci,listaTacnihOdgovora):
    korak = {
        1: "napred",
        2: "levo",
        3: "desno",
        4: "dole"
    }
    bool = False;
    def novaTimer():
        try:
            pocetnaPozicijaPrvog["igrac"].client_socket.send("TimeOut".encode());

        except Exception as exc:
            # funkcijaObradaException(exc,igraci,bool);
            print("nije okej")

    listaOdgovora = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']

    odgovor ="";

    pomocna["vrednost"]=False;
    timer = Timer(15.0,istekloVreme);

    timer.start();
    while (True):

        if(pomocna["vrednost"]==True):
            pocetnaPozicijaPrvog["igrac"].client_socket.send("Niste na vreme odgovorili".encode());
            slanjeIgracuBezPoteza(igraci,pocetnaPozicijaPrvog,"Protivnik nije na vreme odgovorio");
            time.sleep(2);
            return matrica;
        noviTimer = Timer(2.0,novaTimer);
        noviTimer.start();

        odgovor = pocetnaPozicijaPrvog["igrac"].client_socket.recv(4096).decode(); #ovako mora da ne bi zabolo zbog timera

        if (bool == True):
            return;

        if(odgovor=="TimeOut"):

            continue;
        noviTimer.cancel();

        izlazFor = 0;
        for x in listaOdgovora:
            if (odgovor == x):
                izlazFor = 1;
                break;
        if (izlazFor == 1):
            timer.cancel();
            break;
        pocetnaPozicijaPrvog["igrac"].client_socket.send("Pogresno ste uneli odgovor.Pokusajte ponovo".encode());
        time.sleep(0.5)
    if (odgovor.upper() == pitanje[6]):
        while (True):
            listaTacnihOdgovora.append(pitanje[1]);

            pocetnaPozicijaPrvog["igrac"].client_socket.send("Odgovor je tacan".encode());

            if(bool==True):
                return;

            time.sleep(1);
            slanjeIgracuBezPoteza(igraci,pocetnaPozicijaPrvog,"Protivnik je tacno odgovorio. Njegov odgovor je "+odgovor+ "Uskoro ste Vi na potezu");
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

                skor["prviIgracSkor"] += skor["vrednostPitanja"];

            else:
                matrica[pocetnaPozicijaPrvog["brojVrste"]][pocetnaPozicijaPrvog["brojKolone"]] = Color(
                    u"{bggreen}{black}{b}" + str(skor["vrednostPitanja"])
                    + "{/b}{/black}{/bggreen}");
                posecenDrugi = {"brojVrste": pocetnaPozicijaPrvog["brojVrste"],
                               "brojKolone": pocetnaPozicijaPrvog["brojKolone"]};
                listaPosecenih[1].append(posecenDrugi);
                skor["drugiIgracSkor"] += skor["vrednostPitanja"];

            slanjeSvimIgracima(igraci,"Trenutni rezultat je:\n Prvi igrac: "+str(skor["prviIgracSkor"])+"\n Drugi igrac: "+str(skor["drugiIgracSkor"])+"\n");
            time.sleep(1);


            listaPomeraja = [1, 2, 3, 4];

            while(True):

                izlazwhile = 0;
                while(True):
                    pocetnaPozicijaPrvog["igrac"].client_socket.send("Gde zelite da se pomerite? Unesite broj od jedan do cetiri.\n 1.Napred \n 2.Levo \n 3.Desno \n 4.Dole ".encode());
                    pomeraj = pocetnaPozicijaPrvog["igrac"].client_socket.recv(4096).decode();

                    for x in listaPomeraja:
                        if (pomeraj == str(x)):
                           izlazwhile = 1;
                           break;

                    if(izlazwhile == 1):
                        break;

                    pocetnaPozicijaPrvog["igrac"].client_socket.send("Pogresno ste uneli broj na koji zelite da se pomerite".encode())
                    time.sleep(0.5);

                nova = pocetnaPozicijaPrvog;
                bool = kretanjeMatrica(korak[int(pomeraj)], nova, matrica,listaPosecenih);


                if(bool==False):
                    pocetnaPozicijaPrvog["igrac"].client_socket.send("Nije moguce se pomeriti ovde".encode());
                    time.sleep(0.5)
                    continue; #bool uvek ostaje false zato sto prenos po vrednosti

                matrica[pocetnaPozicijaPrvog["brojVrste"]][pocetnaPozicijaPrvog["brojKolone"]] = Color(
                    u"{bgwhite}{black}{b}" + pocetnaPozicijaPrvog["vrednostMatrice"]
                    + "{/b}{/black}{/bgwhite}");
                break;
            return matrica;

    else:

        pocetnaPozicijaPrvog["igrac"].client_socket.send("Odgovor nije tacan\n".encode());
        slanjeIgracuBezPoteza(igraci,pocetnaPozicijaPrvog,"Protivnik je netacno odgovorio. Sada ste vi na potezu\n")
        time.sleep(2);
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



def igrica(matrica,prviIgrac,drugiIgrac): #mora metoda da se pozove koja postavlja pitanje i proverava odgovore i prenos(preko one kategorije i vrednosti

        timeout = 60 * 15  # [seconds]
        timeout_start = time.time()
        pocetnaPozicijaPrvog = {"brojVrste": 0,
                                "brojKolone": 0,
                                "vrednostMatrice": matrica[0][0],
                                "brojIgraca": 1,
                                "igrac": prviIgrac}
        pocetnaPozicijaDrugog = {"brojVrste": 4,
                                "brojKolone": 6,
                                "vrednostMatrice": matrica[4][6],
                                "brojIgraca": 2,
                                "igrac": drugiIgrac}

        listaPosecenihPrvi =[{"brojVrste": pocetnaPozicijaPrvog["brojVrste"],"brojKolone": pocetnaPozicijaPrvog["brojKolone"]}];
        listaPosecenihDrugi=[{"brojVrste": pocetnaPozicijaDrugog["brojVrste"],"brojKolone": pocetnaPozicijaDrugog["brojKolone"]}];
        listaPosecenih =[listaPosecenihPrvi,listaPosecenihDrugi]

        listaTacnihOdgovora=[];
        igrac = [pocetnaPozicijaPrvog,pocetnaPozicijaDrugog];
        i=0;
        def slanjePrvom(): #ovo su funcije da rese problem ako tokom igre jednog igraca drugi posalje poruku i obrunuto
            try:
                igrac[0]["igrac"].client_socket.send("TimeOut".encode());
            except:
                print("otisao igrac")
        def slanjeDrugom():
            try:
                igrac[1]["igrac"].client_socket.send("TimeOut".encode());
            except:
                print("otisao igrac")

        skor = {"prviIgracSkor": 0,
                "drugiIgracSkor": 0}

        while time.time() < timeout_start+timeout: #Ovo je vreme igrice 15 min

            slanjeSvimIgracima(igrac,tabulate(matrica, tablefmt="fancy_grid"));
            time.sleep(1);
            if(i==0):
                slanjeSvimIgracima(igrac,"Na potezu je: "+igrac[0]["igrac"].username);

                noviTimer = Timer(1.0, slanjePrvom);
                noviTimer.start();
                odg1 = igrac[0]["igrac"].client_socket.recv(4096).decode()
                if(odg1 == "TimeOut"):
                    print("okej")
                noviTimer.cancel()

            else:
                slanjeSvimIgracima(igrac,"Na potezu je: "+igrac[1]["igrac"].username);
                noviTimer = Timer(1.0, slanjeDrugom);
                noviTimer.start();
                odg2=igrac[1]["igrac"].client_socket.recv(4096).decode()
                noviTimer.cancel();
            vremeOdgovora=15;
            vremeStart= time.time();

            while time.time() < vremeStart+vremeOdgovora: #Ovo je vreme za svako pitanje i pomeraj


                pitanje ="";
                if(tipPitanja(igrac[i])==10):

                    randomPitanjePostavlenoDeset = randomPitanje(10,listaTacnihOdgovora);

                    porukaDeset = str(randomPitanjePostavlenoDeset[1])+"\n A)"+str(randomPitanjePostavlenoDeset[2])+"\n B)"+str(randomPitanjePostavlenoDeset[3]) +"\n C)"+str(randomPitanjePostavlenoDeset[4])+"\n D)"+str(randomPitanjePostavlenoDeset[5])+"\n Molim Vas odgovorite na pitanje";

                    igrac[i]["igrac"].client_socket.send(porukaDeset.encode());
                    slanjeIgracuBezPoteza(igrac, igrac[i],
                        str(randomPitanjePostavlenoDeset[1])+"\n A)"+str(randomPitanjePostavlenoDeset[2])+"\n B)"+str(randomPitanjePostavlenoDeset[3]) +"\n C)"+str(randomPitanjePostavlenoDeset[4])+"\n D)"+str(randomPitanjePostavlenoDeset[5])+"\n Sacekajte da Vas protivnik odgovori na pitanje");
                    pitanje = randomPitanjePostavlenoDeset;
                elif(tipPitanja(igrac[i])==30):
                    randomPitanjePostavlenoDvadeset =randomPitanje(30,listaTacnihOdgovora);
                    poruka30= str(randomPitanjePostavlenoDvadeset[1])+"\n A)"+str(randomPitanjePostavlenoDvadeset[2])+"\n B)"\
                              +str(randomPitanjePostavlenoDvadeset[3]) +"\n C)"+str(randomPitanjePostavlenoDvadeset[4])+"\n D)"+str(randomPitanjePostavlenoDvadeset[5])+ "\n Molim Vas odgovorite sa A,B,C,D";
                    igrac[i]["igrac"].client_socket.send(poruka30.encode());
                    slanjeIgracuBezPoteza(igrac, igrac[i], str(randomPitanjePostavlenoDvadeset[1])+"\n A)"+str(randomPitanjePostavlenoDvadeset[2])+"\n B)"\
                              +str(randomPitanjePostavlenoDvadeset[3]) +"\n C)"+str(randomPitanjePostavlenoDvadeset[4])+"\n D)"+str(randomPitanjePostavlenoDvadeset[5])+ "\n Sacekajte da Vas protivnik odgovori na pitanje");

                    pitanje = randomPitanjePostavlenoDvadeset;

                elif (tipPitanja(igrac[i]) == 20):
                    randomPitanjePostavlenoTrideset = randomPitanje(20,listaTacnihOdgovora);
                    poruka20 = str(randomPitanjePostavlenoTrideset[1]) + "\n A)" + str(
                        randomPitanjePostavlenoTrideset[2]) + "\n B)" \
                               + str(randomPitanjePostavlenoTrideset[3]) + "\n C)" +str(randomPitanjePostavlenoTrideset[4])+"\n D)"+str(randomPitanjePostavlenoTrideset[5])+ "\n Molim Vas odgovorite sa A,B,C,D";
                    igrac[i]["igrac"].client_socket.send(poruka20.encode());
                    slanjeIgracuBezPoteza(igrac, igrac[i], str(randomPitanjePostavlenoTrideset[1]) + "\n A)" + str(
                        randomPitanjePostavlenoTrideset[2]) + "\n B)" \
                                          + str(randomPitanjePostavlenoTrideset[3]) + "\n C)" + str(randomPitanjePostavlenoTrideset[4])+"\n D)"+str(randomPitanjePostavlenoTrideset[5]) + "\n Sacekajte da Vas protivnik odgovori na pitanje");

                    pitanje = randomPitanjePostavlenoTrideset;
                elif (tipPitanja(igrac[i]) == 50):
                    randomPitanjePostavlenoDvadeset = randomPitanje(30,listaTacnihOdgovora);
                    poruka30 = str(randomPitanjePostavlenoDvadeset[1]) + "\n A)" + str(
                        randomPitanjePostavlenoDvadeset[2]) + "\n B)" \
                               + str(randomPitanjePostavlenoDvadeset[3]) + "\n C)" + \
                               str(randomPitanjePostavlenoDvadeset[4])+"\n D)"+str(randomPitanjePostavlenoDvadeset[5])+ "\n Molim Vas odgovorite sa A,B,C,D";
                    igrac[i]["igrac"].client_socket.send(poruka30.encode());
                    slanjeIgracuBezPoteza(igrac, igrac[i], str(randomPitanjePostavlenoDvadeset[1]) + "\n A)" + str(
                        randomPitanjePostavlenoDvadeset[2]) + "\n B)" \
                            + str(randomPitanjePostavlenoDvadeset[3]) + "\n C)" +str(randomPitanjePostavlenoDvadeset[4])+"\n D)"+str(randomPitanjePostavlenoDvadeset[5])+ "\n Sacekajte da Vas protivnik odgovori na pitanje");

                    pitanje = randomPitanjePostavlenoDvadeset;

                skor["vrednostPitanja"] = int(tipPitanja(igrac[i]));
                odgovor ="";
                matrica =odgovorObrada(odgovor,matrica,igrac[i],pitanje,listaPosecenih,skor,igrac,listaTacnihOdgovora);
                if(i==0):
                    i+=1;
                elif(i==1):
                    i-=1;


                break;
            if(igrac[0]["brojVrste"]== 4 and igrac[0]["brojKolone"] ==6):
                break;
            if(igrac[1]["brojVrste"]== 0 and igrac[1]["brojKolone"] ==0):
                break;

        if(skor["prviIgracSkor"]>skor["drugiIgracSkor"]):
            igrac[0]["igrac"].client_socket.send("Cestitamo! Vi ste pobedili".encode());
            igrac[1]["igrac"].client_socket.send("Nazalost izgubili ste. Vise sredje sledeci put!".encode());
            azuriraj(igrac[0]["igrac"].username,skor["prviIgracSkor"],1)
            azuriraj(igrac[1]["igrac"].username, skor["drugiIgracSkor"], 0)



            time.sleep(5);
        elif(skor["prviIgracSkor"]<skor["drugiIgracSkor"]):
            igrac[1]["igrac"].client_socket.send("Cestitamo! Vi ste pobedili".encode());
            igrac[0]["igrac"].client_socket.send("Nazalost izgubili ste. Vise sredje sledeci put!".encode());
            azuriraj(igrac[1]["igrac"].username, skor["drugiIgracSkor"], 1)
            azuriraj(igrac[0]["igrac"].username, skor["prviIgracSkor"], 0)


        else:
            slanjeSvimIgracima(igrac,"Nereseno je!")
            time.sleep(5);
            azuriraj(igrac[1]["igrac"].username, skor["drugiIgracSkor"], 0)
            azuriraj(igrac[0]["igrac"].username, skor["prviIgracSkor"], 0)






