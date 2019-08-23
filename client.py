from socket import *
from time import sleep
from threading import *


class ListenThread(Thread):
    tekstProvera = "";
    def __init__(self, sock):
        self.sock = sock
        # Calling a constructor of 'Thread' class
        super().__init__()
        # self.start() essentially runs the run() method below
        self.start()

    def run(self):

        # Just keeps receiving messages as they come and prints them
        while True:
            try:
                tekst= self.sock.recv(4096).decode();
                tekstZaProveru = tekst;
                if (tekst == "TimeOut"):
                    cl_socket.send("TimeOut".encode());
                    continue;

                if(tekst == "napusti123."):
                    cl_socket.send("napusti123".encode());
                    continue;

                print(tekst);

                if(tekst=="Dovidjenja"):

                    return;
            except ConnectionResetError:
                print("ne mozete da se povezete na server")
                sleep(5);



server_adress = 'localhost';
server_port = 8090;


while True:
    try:
        cl_socket = socket(AF_INET,SOCK_STREAM);

        cl_socket.connect((server_adress,server_port));


        listener = ListenThread(cl_socket);
        break;
    except:
        print("ne mozete da se povezete na server")
        sleep(5);


while True:
    try:
        message = input()

        # Send it to the server
        cl_socket.send(message.encode())
        if(message == "5"):
            break;
    except:
        print("ne mozete da se povezete na server")
        sleep(5);



