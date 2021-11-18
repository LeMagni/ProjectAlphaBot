import socket as sck
import threading as thr 
import logging
import time
import RPi.GPIO as GPIO
import sqlite3

class AlphaBot(object):                         #classe dove sono definiti i movimenti dell'alphabot e le indiciazioni trasmesse ai motori
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 25
        self.PB  = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def right(self,t,speed=20):                     #funzione per fare ruotare l'alphabot su se stesso verso destra
                                                    #t è il tempo in secondi in cui ruoterà, speed è impostato a 20 perchè,per il nostro alphabot, era la velocità con cui in 2 secondi ruotava circa di 90 gradi 
        self.PWMA.ChangeDutyCycle(speed)            
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)             
        time.sleep(t)                               #con il time sleep prolunghiamo la durata del movimento per il valore di t
        self.stop()                                 #l'aphabot si ferma

    def stop(self):                                 #funzione che viene chiamata nelle altre funzioni per fermare l'alphabot
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def stopSinghiozzo(self,t):                     #funzione utile solo quando l'utente decide di eseguire il comando struturato singhiozzo
                                                    #è diverso dall'altro stop perchè, in questo caso, l'alphabot deve rimanere fermo per un determinato t per poi ripartire, che è una tipologia di movimento che viene utilizzato solo in singhiozzo 
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(t)

    def left(self,t,speed=20):                      #analoga alla funzione right(), solamente che l'alphabot ruoterà su se stesso verso sinistra 
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(t)
        self.stop()

    def forward(self,t):                            #funzione per far muovere l'alphabot in avanti. Abbiamo deciso di dare un boost iniziale al movimento, dando una velocità iniziale molto più alta rispetto alla velocità del resto del movimento
        speedInit=40                                #velocità iniziale del boost            
        speed=30                                    #velocità per il resto  movimento 
        
                                                    #con questa if, se il tempo che viene inserito dall'utente è maggiore di 6 secondi, il tempo del boost sarà sempre uguale a 1,5 secondi
        if t/4>=1.5:                                #appiamo fatto questa scelta perchè temavamo che inserendo determinate tempistiche, il booost durasse troppo, perdendo il suo effetto
            tInit=1.5
        else:                                       #nelle altre casistiche, il tempo del boost sarà sempre di un durata uguale ad un quartio del tempo inserito dall'utente
            tInit=t/4
        t=t-tInit
        self.PWMA.ChangeDutyCycle(speedInit-5)      #il -5 allo speedInit è stato inserito dopo alcuni test perchè abbiamo visto che l'alphabot andava più "dritto"
        self.PWMB.ChangeDutyCycle(speedInit)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(tInit)
        self.PWMA.ChangeDutyCycle(speed-2)          #stesso discorso del -5 allo speedI
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(t)
        self.stop()

    def backward(self,t):
        speedInit=40
        speed=30
        if t/4>=1.5:
            tInit=1.5
        else:
            tInit=t/4
        t=t-tInit
        self.PWMA.ChangeDutyCycle(speedInit)
        self.PWMB.ChangeDutyCycle(speedInit)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(tInit)
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(t)
        self.stop()

class Client_Manager(thr.Thread):                       #thread per la gestione del client 
    def __init__(self,connection,address):
        thr.Thread.__init__(self)                       
        self.connection=connection
        self.address=address
        self.alpha=AlphaBot()
        self.running=True
    
    def run(self): 
        while self.running:
            msg=self.connection.recv(4096).decode()     #I messaggi del client sono composti dal l'iniziale del movimento e la durata in secondi del movimento
                                                        #msg[0] contiene l'iniziale e msg[1:]contiene la durata
            print(msg[0], msg[1:])
            if msg[0]== "F":                            #richiamo alla funzione forward
                self.alpha.forward(int(msg[1:]))
            elif msg[0] == "B":
                self.alpha.backward(int(msg[1:]))       #richiamo alla funzione backward
            elif msg[0]== "R":
                self.alpha.right(int(msg[1:]))          #richiako alla funzione right
            elif msg[0] == "L": 
                self.alpha.left(int(msg[1:]))           #richiamo alla funzione left
            else:
                comandoPersonalizzato(msg, self.alpha)  #quando il messaggio dell'utente non contiene un iniziale e la durata ma un comando strutturato, viene richiamata la funzione comandoPersonalizzato

def comandoPersonalizzato(msg, Ab):                     #funzione per la gestione dei comandi strutturati
    con = sqlite3.connect('./Database.db')              #collegamento al database dove sono definiti i comunadi strutturati e l'insieme dei movimenti singoli di cui sono composti

    cur= con.cursor()                                   #viene selezionato il comando dalla table del database e viene restituito l'insime dei singoli movimenti che appartengono al comando strutturato 
    msg = str(cur.execute(f"SELECT sequenza FROM ALPHABOT WHERE Nome = '{msg}'").fetchall())

    msg = msg[3:-4]                                     #vengono rimosse le parentesi che vengono restutite con il comando precedente, facendo così che msg contenga solamente i comandi

    if len(msg) != 0:                           
        print(msg)
        msg = msg.split('-')                            #con la split la stringa, msg diventa una lista con tutti i movimenti distinti fra loro

        for i in msg:                                   #ciclando msg per i, i rappresenta per ogni ciclo un singolo comando del comando strutturato, con iniziale del movimento e durata del movimento
            print(i)                                    #richiamo alle funzioni dei movimenti dell'alphabot 
            if (i[0] == "F"):                           
                Ab.forward(int(i[1:]))
            elif (i[0] == "R"):
                Ab.right(int(i[1:]))
            elif (i[0] == "L"):
                Ab.left(int(i[1:]))
            elif (i[0] == "B"):
                Ab.backward(int(i[1:]))
            elif (i[0]== "S"):
                Ab.stop()
            elif (i[0] == "T"):
                Ab.stopSinghiozzo(int(i[1:]))
                
def main():
    s=sck.socket(sck.AF_INET,sck.SOCK_STREAM)       #creazione del socket
    s.bind(("192.168.0.126",6000))                  #indirizzo della scheda raspberry pi presente sull'alphabot 
    s.listen()                                      #si mette in ascolto dei comandi che arrivaranno dal client 

    while True:
        connection, address=s.accept()   
        client=Client_Manager(connection,address)   #creazione del thread
        print(address)                              #facciamo una print per capire quando avviene la connessione con il client 
        client.start()                              #il thread parte 

if __name__=="__main__":
    main()
