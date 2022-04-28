#tcp
#f"!list" -> f"list:{dict.keys()}"

import socket as sck

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(('localhost',5000))

    while True:
        com = input("Inserisci comando:")
        pot1 = input("Inserisi potenza motore A:")
        pot2 = input("Inserisi potenza motore B:")
        s.sendall(f"com:{com}:pot1:{pot1}:pot2:{pot2}".encode())

        """
        data = s.recvfrom(4096)
        data = data.decode()
        data = data.split(":")

        if data[0] == 0:
            print("Ho fatto bene")
        elif data[1] == 1:
            print("Ho sbagliato")
            ris = input("Hai capito l'errore:")   #devo dire si --> 0 || no --> 1
            s.sendall(ris.decode())
        """


if __name__=="__main__":
    main()