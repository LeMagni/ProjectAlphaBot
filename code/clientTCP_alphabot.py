import socket as sck

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) #creazione del socket
    s.connect(('192.168.0.126',6000)) #nella connect inserisco l'indirizzo IP della scheda RaspberryPI dell'alphabot

    while True:
        print(" Inserire direzione e tempo di percorrenza:\nComandi Base:\nForeward: F    Backward: B\nLeft: L    Right: R\nComandi strutturati:\n -ZigZag   -InversioneU\n-Singhiozzo   -Sfondamento\n")
        #lista comandi disponibili sull'alphabot
        com = input("Inserisci comando:")
        s.sendall(com.encode()) #invio del comando al server


if __name__=="__main__":
    main()