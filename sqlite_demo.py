import sqlite3;
from osoba import *;
import random;

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
        c.execute("UPDATE igrac set brojMeceva +=:brojMeceva and ukupanBrojPoena +=:brojPoena and brojPobeda+=:pobeda where username =:username",
                  {'brojMeceva': 1,'brojPoena':brojPoena,'pobeda':pobeda,'username':username});
    conn.commit();


def prikaziStatistikuIgraca(username):
    print(c.execute("select * from igrac where username=:username",{'username':username}));

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
    for x in lista:
        for y in listaTacnihOdgovora:
            if(x[1]==y[1]):
                lista.remove(x);
                break;

    return random.choice(lista);




