class Osoba:
    def __init__(self,ime,prezime,username,email,sifra):
        self.ime =ime;
        self.prezime =prezime;
        self.username = username;
        self.email =email;
        self.sifra = sifra;

class LoginOsoba(Osoba):
    def __init__(self,username,sifra,client_adress,client_socket):
        self.username=username;
        self.sifra=sifra;
        self.client_adress =client_adress;
        self.client_socket =client_socket;




def proveraImenaPrezimena(imePrezime):
    imePrezime = str(imePrezime);

    if (len(imePrezime) <= 2):
        return 0;
    for x in imePrezime:
        if (not (x.isalpha())):
            return 0;

    return 1;


def proveraUsername(username):
    username = str(username);
    if (len(username) < 5):
        return False;
    if (not (username[0].isalpha())):
        return False;

    return True;


def proveraEmail(email):
    email = str(email);
    b1 = 0;
    b2 = 0;
    indeks = -1
    for s in email:
        if (s == "@"):
            b1 += 1
    brojac = 0;

    if (b1 > 0):
        for s in email:
            brojac += 1;
            if (s == "@"):
                break;

        # ovo ne radi jos kada se vratis proveri
    else:
        return False;

    if (email[brojac:] != "gmail.com" and email[brojac:] != "hotmail.com" and email[brojac:] != "fon.bg.ac.rs"):
        return False;
    return True;


def proveraSifre(sifra):
    # mora imati makar jedno veliko slovo,
    # mora imati makar jedan broj
    # mora imati vise od 6
    sifra = str(sifra);
    brojacCifara = 0;
    brojacVelikog = 0;
    if (len(sifra) <= 6):
        return False;

    for x in sifra:
        if (x.isupper()):
            brojacVelikog += 1;
        if (x.isdigit()):
            brojacCifara += 1;
    if (brojacCifara == 0 or brojacVelikog == 0):
        return False;

    return True;

