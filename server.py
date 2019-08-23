from socket import *
from threading import *
from osoba import *
from igrica2 import *
import time;
from sqlite_demo import *;



class ClientHandler(Thread):




    def __init__(self, cl_sock, cl_address):
        self.sock = cl_sock
        self.address = cl_address



        # Append thread to all clients

        # Calling a constructor of 'Thread' class
        super().__init__()
        # self.start() essentially runs the run() method below
        self.start()

    def run(self):
        self.sock.send("Dobrodosli na nas forum".encode())
        izlaz = 0;
        uspesanLogin = False;

        #Ovo je metoda da proveri da li postoji vec registrovan  sa istim mejlom ili usernamom

        def proveraRegistracije(klijent):

            brojacUsername=0;
            brojacEmail=0;
            for x in clients:

                if(x.username  == klijent.username):
                    brojacUsername +=1;
                if(x.email == klijent.email):
                    brojacEmail +=1;

            if(brojacEmail>0 and brojacUsername>0):
                return 1;
            elif(brojacEmail>0):
                return 2;
            elif(brojacUsername>0):
                return 3;

            return 0;



        def proveraLogin(usernameEmail,sifra,broj):
            usernameEmail = str(usernameEmail);
            sifra = str(sifra);

            if(broj ==0):
                for x in clients:
                    if(x.email == usernameEmail and x.sifra == sifra):
                        return x.username;
            else:
                for x in clients:
                    if(x.username == usernameEmail and x.sifra == sifra):
                        return x.username;
            return False;
        username = "";

        while True:
            try:
                # Receive message from this client

                self.sock.send("\nOvo je pocetni meni.\n 1.Registrujte se \n 2.Login \n "
                               "3.Pravila koriscenja \n 4. Pokreni igricu \n 5. Napusti".encode());
                izborMenija = self.sock.recv(4096).decode();



                if (izborMenija == "1"):

                    while(True):
                        self.sock.send("Ako zelite da se vratite u glavni meni napisite 'Napusti'\n".encode());

                        self.sock.send("Unesite ime".encode());
                        imeRegistracija = self.sock.recv(4096).decode()
                        if(imeRegistracija.lower()=="napusti"):
                            break; #za povratak u glavni meni

                        if(proveraImenaPrezimena(imeRegistracija)== False):

                            self.sock.send("Pogresno ste uneli ime".encode());
                            continue;
                        self.sock.send("Unesite prezime".encode());
                        prezimeRegistracija = self.sock.recv(4096).decode()
                        if (prezimeRegistracija.lower() == "napusti"):
                            print("jeste")
                            break;  # za povratak u glavni meni
                        if (proveraImenaPrezimena(prezimeRegistracija) == False ):
                            self.sock.send("Pogresno ste uneli prezime".encode());
                            continue;
                        self.sock.send("Unesite username".encode());
                        usernameRegistracija = self.sock.recv(4096).decode()
                        if (usernameRegistracija.lower() == "napusti"):
                            break;  # za povratak u glavni meni
                        if(proveraUsername(usernameRegistracija) == False):
                            self.sock.send("Pogresno ste uneli username".encode());
                            continue;

                        self.sock.send("Unesite email".encode());
                        emailRegistracija = self.sock.recv(4096).decode()
                        if (emailRegistracija.lower() == "napusti"):
                            break;  # za povratak u glavni meni
                        if(proveraEmail(emailRegistracija)==False):
                            self.sock.send("Pogresno ste uneli email".encode());
                            continue;


                        self.sock.send("Unesite sifru".encode());
                        sifraRegistracija = self.sock.recv(4096).decode()
                        if (sifraRegistracija.lower() == "napusti"):
                            break;  # za povratak u glavni meni
                        if (proveraSifre(sifraRegistracija) == False or str(imeRegistracija).isupper()== "NAPUSTI"):
                            self.sock.send("Pogresno ste uneli sifru. "
                                           "Sifra mora imati jedno veliko slovo,makar jedan broj i mora imati duzinu najmanje 7".encode());
                            continue;

                        if(istiUsernameEmail(usernameRegistracija,emailRegistracija)==False):
                            self.sock.send(
                                "Osoba sa datim emailom ili korisnickim imenom postoji vec.Molim Vas unesite neku drugu vrednost".encode())
                            continue;

                        osoba = Osoba(imeRegistracija,prezimeRegistracija,usernameRegistracija, emailRegistracija,sifraRegistracija);


                        self.sock.send("Uspesno ste se registrovali".encode());
                        ubacivanjeRegistrovanog(osoba);
                        clients.append(osoba);
                        time.sleep(2);
                        break;
                elif(izborMenija == "2"):
                    if (uspesanLogin == True):
                        self.sock.send("Vec ste se ulogovali".encode());
                        continue; #ovo je da ne ide neko login 5 puta
                    while(True):

                        self.sock.send("Ako zelite da se vratite u glavni meni napisite 'Napusti'\n".encode());
                        self.sock.send("Unesite username ili email".encode());
                        usernameEmailLogin = self.sock.recv(4096).decode();
                        br=-1;
                        if (usernameEmailLogin.lower() == "napusti"):
                            break;  # za povratak u glavni meni
                        if(proveraEmail(usernameEmailLogin)== True):
                            br=0;
                        else:
                            br=1;
                        self.sock.send("Unesite sifru".encode());
                        sifraLogin = self.sock.recv(4096).decode();
                        if (sifraLogin.lower() == "napusti"):
                            break;  # za povratak u glavni meni
                        username = "";
                        if(proveraLogin2(usernameEmailLogin,sifraLogin,br)==False):
                            if(br==0):
                                self.sock.send("Pogresno ste uneli sifru ili email".encode());
                            else:
                                self.sock.send("Pogresno ste uneli username ili sifru".encode());
                            continue;
                        else:
                            username= proveraLogin2(usernameEmailLogin,sifraLogin,br);
                            username=str(username);
                            username=username[2:len(username)-3]; #da se izdvoji samo ime
                        prom = 0;
                        for x in loginClients: #ako pokrenem 5 klijenata i da se vise njih loguje na istu osobu
                             if(x.username==username):
                                 prom=1;
                                 break;
                        if(prom==1):
                            self.sock.send("Uneti korisnik se vec ulogovan".encode());
                            continue;

                        self.sock.send("Uspesno ste se login".encode());
                        loginKlijent = LoginOsoba(username,sifraLogin,self.address,self.sock);

                        uspesanLogin =True;
                        time.sleep(2);
                        loginClients.append(loginKlijent);
                        #da ga izbacim ako izadje
                        break;
                elif(izborMenija=="4"):
                    if(uspesanLogin==False):
                        self.sock.send("Niste se ulogovali i ne mozete da igrate igricu".encode());
                        time.sleep(2);
                        continue;
                    while(True):
                        self.sock.send("\nDobrodosli u igricu.\n 1.Igrajte igricu \n 2.Vasa statistika \n "
                                       "3.Rang Lista (brojPoena/brojMeceva) \n 4.Vratite se u glavni meni".encode());
                        try:
                            izborIgrica = self.sock.recv(4096).decode();
                        except:
                            print("pukao");
                        if(izborIgrica=="1"):
                            self.sock.send("Trazimo vase protivnika molim vas sacekajte".encode());
                            osoba = LoginOsoba("","","","");
                            print(username);
                            for x in loginClients:
                                #if(x.client_adress == self.address and x.client_socket == self.sock):

                                if(x.username==username):
                                    #ovde je problem zato sto su i thread1 i thread2 na istom socketu i istoj adresi i on vec nadje taj isti
                                    cekajuClients.append(x);
                                    print(len(cekajuClients));
                                    osoba = x;
                                    break;



                            print("Osoba je" + osoba.username) #ako se login preko mejla pokazuje mail
                            napustanjeWhile=0;
                            brojac=-1;

                            prviIgrac = LoginOsoba("","","","");
                            drugiIgrac = LoginOsoba("","","","");
                            while True:

                                i=0;
                                if len(cekajuClients)==0:
                                    break;

                                #ovde je bio brojac;
                                while brojac < len(cekajuClients):
                                    # ovde puca kod kada se pokrene thread 2 pa thread 1- kaze out of range

                                    if (cekajuClients[i].username == osoba.username):
                                        brojac = i;  # poziciju u listi nalazi
                                        break;
                                    i += 1;
                                if (brojac == -1):
                                    break;


                                if(brojac%2==0):
                                    for x in cekajuClients:
                                        if (x.username != osoba.username):
                                            # x.client_socket.send("Vas protivnik je  "+osoba.username.encode())
                                            pro1 ="Vas protivnik je "+str(osoba.username);
                                            x.client_socket.send(pro1.encode());
                                            print("vas" + x.username);
                                            print("vas" + osoba.username);
                                            prviIgrac=osoba;
                                            drugiIgrac=x;


                                            pro2 ="Vas protivnik je "+str(x.username);
                                            osoba.client_socket.send(pro2.encode())
                                            cekajuClients.remove(x);
                                            cekajuClients.remove(osoba);

                                            napustanjeWhile = 1;
                                            break;
                                    if(napustanjeWhile==1):
                                        break;
                                else:
                                    time.sleep(10) #ovo mozda ali i ne treba
                            if(brojac%2==0):
                                time.sleep(2);
                                ubaciIgraca(prviIgrac.username);
                                ubaciIgraca(drugiIgrac.username); #ubacivanje u bazu
                                prviIgrac.client_socket.send("Dobrodosli u igricu".encode());
                                drugiIgrac.client_socket.send("Dobrodosli u igricu".encode());
                                time.sleep(3);
                                listaMeceva.append(prviIgrac);
                                listaMeceva.append(drugiIgrac);
                                igrica(matricaPocetna,prviIgrac,drugiIgrac);
                                time.sleep(1);
                                listaMeceva.remove(prviIgrac);
                                listaMeceva.remove(drugiIgrac);

                            else:
                                while brojac==1:
                                   brojac=0;
                                   for x in listaMeceva:
                                        if(x.client_socket == self.sock and x.client_adress == self.address):
                                            brojac=1;
                                            break;

                                   time.sleep(3);


                        elif(izborIgrica=="2"):

                            if(prikaziStatistikuIgraca(username)==False):
                                self.sock.send("Niste jos uvek nijednom pokrenuli igricu".encode());
                                time.sleep(1);
                                continue;
                            else:
                                stat = prikaziStatistikuIgraca(username);

                            statistika = "Vasa statistika je:\n Broj odigranih meceva: "+str(stat[0][1])+ "\n Broj pobeda: " +str(stat[0][3]) \
                                         +"\n Ukupan broj poena: "+str(stat[0][2]);
                            self.sock.send(statistika.encode());
                            time.sleep(3);
                        elif(izborIgrica=="4"):
                            break;
                            time.sleep(1);
                        elif(izborIgrica=="3"):
                           if (prikaziStatistikuIgraca(username) == False):
                                self.sock.send("Niste jos uvek nijednom pokrenuli igricu".encode());
                                time.sleep(1);
                                continue;
                           rangLista= prikaziRangListu(username);
                           self.sock.send(rangLista.encode());
                           time.sleep(3);
                        else:
                            self.sock.send("Pogresno ste uneli broj".encode());

                elif(izborMenija=="5"):
                    self.sock.send("Dovidjenja".encode());
                else:
                    self.sock.send("Pogresno ste uneli broj".encode());
            except Exception:
                # ConnectionResetError

                try:
                    listaMeceva.remove(prviIgrac);
                    listaMeceva.remove(drugiIgrac)
                except Exception:
                    print("nema ga u listi");

                for x in loginClients:
                    if(x.client_socket ==self.sock and x.client_adress == self.address):
                        loginClients.remove(x);
                        break;

                self.sock.close()
                # Break out of the infinite loop so the thread can finish
                break;

#Liste koje su mi potrebne
clients =[];
loginClients=[];
cekajuClients =[];
listaMeceva =[];

server_address = 'localhost';
server_port =8090;

srv_socket = socket(AF_INET,SOCK_STREAM)

srv_socket.bind((server_address,server_port))

srv_socket.listen(5)

print('Waiting for connections');
i=0;

while True:

    client_socket, client_adress = srv_socket.accept();
    print(client_adress)

    client = ClientHandler(client_socket, client_adress);





