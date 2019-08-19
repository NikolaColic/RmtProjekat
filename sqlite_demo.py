import sqlite3;
from osoba import *;
import random;
from colorclass import *;

conn = sqlite3.connect("igraci.db",check_same_thread=False);


c = conn.cursor();

#--------------------------------------------------------------Registracija------------------------------------------------------
#c.execute("""CREATE TABLE registrovaniIgraci (
         #   ime text,
         #   prezime text,
         #   username text,
          #  email text,
           # sifra text
          #  )""");



conn.commit();

def ubacivanjeRegistrovanog(oso):
    with conn:
        c.execute("INSERT into registrovaniIgraci VALUES (?,?,?,?,?)",
                  (oso.ime, oso.prezime, oso.username, oso.email, oso.sifra));
    conn.commit();
#provera username

def istiUsernameEmail(username,email):
    c.execute("Select * from registrovaniIgraci where username=:username or email=:email",{'username':username, 'email':email});
    lista = c.fetchall();
    if(len(lista)==0):
        return True;
    else:
        return False;

def proveraLogin2(usernameEmail,sifra,broj):
    if (broj == 0): #email
        c.execute("Select username from registrovaniIgraci where sifra=:sifra and email=:email",{'sifra':sifra, 'email':usernameEmail});
        lista = c.fetchall();

        if (len(lista) ==1):

            return lista[0];
    else:
        c.execute("Select username from registrovaniIgraci where sifra=:sifra and username=:username",
                  {'sifra': sifra, 'username': usernameEmail});
        lista = c.fetchall();

        if (len(lista) == 1):
            return lista[0];
    return False;

#----------------------------------------------------------------------------------------------------------
#c.execute("""CREATE TABLE igrac (
       #     username text,
       #     brojMeceva int,
        #    ukupanBrojPoena int,
        #    brojPobeda int
       #     )""");
#conn.commit();


def ubaciIgraca(username):
    with conn:
        c.execute("Select * from igrac where username=:username ",{'username':username });
        lista = c.fetchall();
        if (len(lista) == 0 ):
            c.execute("INSERT into igrac VALUES (?,?,?,?)",
                      (username,0,0,0));

    conn.commit();


def azuriraj(username,brojPoena,pobeda):
    with conn:
        c.execute("select brojMeceva from igrac where username=:username",{'username':username});
        ranijeBrojMeceva = list(c.fetchone())[0];

        c.execute("select ukupanBrojPoena from igrac where username=:username", {'username': username});
        ranijeBrojPoena = list(c.fetchone())[0];

        c.execute("select brojPobeda from igrac where username=:username", {'username': username});
        ranijeBrojPobeda = list(c.fetchone())[0];
        c.execute("DELETE FROM igrac where username=:username", {'username': username});

        c.execute("INSERT into igrac VALUES (?,?,?,?)",
                  (username, ranijeBrojMeceva+1, ranijeBrojPoena+brojPoena, ranijeBrojPobeda+pobeda));

    conn.commit();

def prikaziRangListu(username):
    c.execute("select * from igrac");
    listaPrva = list(c.fetchall());

    listaPrva.sort(key=lambda listaPrva: listaPrva[3],reverse=True);
    brojac=1;

    rangLista ="Username igraca\tBroj pobeda\n";
    for x in listaPrva:
        if(x[0]==username):

            rangLista+=Color(u"{green}{b}" +"\n"+str(brojac)+".\t" +x[0]+"\t"+str(x[3]) + "{/b}{/green}");
            brojac+=1;
            continue;

        rangLista+="\n"+str(brojac)+".\t"+x[0]+"\t"+str(x[3]);
        brojac+=1;
    return rangLista;


#azuriraj("jovanpetrovic97",110,1);


def prikaziStatistikuIgraca(username):
    c.execute("select * from igrac where username=:username",{'username':username});

    lista = list(c.fetchall());
    if(len(lista)==0):
        return False;


    return lista;

kaoLista=prikaziStatistikuIgraca("jovanpetrovic97");

#------------------------------------------------------------------------------------------------------------------------------

#c.execute("""CREATE TABLE pitanja(
  #         redniBroj int,
   #        nazivPitanja text,
  #         A text,
   #        B text,
    #       C text,
    #       D text,
    #       tacanOdgovor text,
    #       kategorija int
     #     )""");
#conn.commit();




def dodajPitanje(redniBroj,pitanje,a,b,c,d,tacanOdgovor,kategorija):
    with conn:
        print("nik");
        c.execute("INSERT into pitanja VALUES (?,?,?,?,?,?,?,?)",(redniBroj,pitanje, a, b, c, d, tacanOdgovor,kategorija));
    conn.commit();

def randomPitanje(kategorija,listaTacnihOdgovora):
    #ovde moze da se salje i pitanja koji su prosli
    c.execute("select * from pitanja where kategorija =:kategorija",{'kategorija':kategorija});
    lista =list(c.fetchall());
    novaLista=[]

    for x in lista:
        brojac = 0;
        for y in listaTacnihOdgovora:
            if((x[1])==y):
                brojac+=1;
        if(brojac==0):
            novaLista.append(x);

    return random.choice(novaLista);





