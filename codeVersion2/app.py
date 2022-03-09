from flask import Flask, render_template, request, redirect, url_for,request, make_response
import socket as sck
import threading as thr 
import time
import RPi.GPIO as GPIO
import sqlite3
import string, random
from datetime import datetime

app = Flask(__name__)

class AlphaBot(object):                                     #classe dove sono definiti i movimenti dell'alphabot e le indiciazioni trasmesse ai motori
    
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

    def right(self,t=2,speed=23):                           #funzione per fare ruotare l'alphabot su se stesso verso destra
        self.PWMA.ChangeDutyCycle(speed)                    #t è il tempo in secondi in cui ruoterà, speed è impostato a 20 perchè,per il nostro alphabot, era la velocità con cui in 2 secondi ruotava circa di 90 gradi
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(t)                                       #con il time sleep prolunghiamo la durata del movimento per il valore di t
        self.stop()                                         #l'aphabot si ferma

    def stop(self):                                         #funzione che viene chiamata nelle altre funzioni per fermare l'alphabot
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self,t=2,speed=23):                            #analoga alla funzione right(), solamente che l'alphabot ruoterà su se stesso verso sinistra 
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(t)
        self.stop()

    def forward(self,t=2):                                  #funzione per far muovere l'alphabot in avanti. Abbiamo deciso di dare un boost iniziale al movimento, dando una velocità iniziale molto più alta rispetto alla velocità del resto del movimento
        speedInit=40                                        #velocità iniziale del boost
        speed=30                                            #velocità per il resto  movimento
                                                            #con questa if, se il tempo che viene inserito dall'utente è maggiore di 6 secondi, il tempo del boost sarà sempre uguale a 1,5 secondi
        if t/4>=1.5:                                        #appiamo fatto questa scelta perchè temavamo che inserendo determinate tempistiche, il booost durasse troppo, perdendo il suo effetto
            tInit=1.5
        else:                                               #nelle altre casistiche, il tempo del boost sarà sempre di un durata uguale ad un quartio del tempo inserito dall'utente
            tInit=t/4
        t=t-tInit
        self.PWMA.ChangeDutyCycle(speedInit-5)              #il -5 allo speedInit è stato inserito dopo alcuni test perchè abbiamo visto che l'alphabot andava più "dritto"
        self.PWMB.ChangeDutyCycle(speedInit)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(tInit)
        self.PWMA.ChangeDutyCycle(speed-2)                  #stesso discorso del -5 allo speedI
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(t)
        self.stop()

    def backward(self,t=2,speed=30):                        #Funzione per fare muovere l'alphabot all'indietro l'alphabot. Analogo alla funzione forward
        speedInit=40
        spped=30
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

def genToken():                                         #Generazione di un token per la sicurezza della pagina
    number_of_strings = 5
    length_of_string = 30
    for x in range(number_of_strings):
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    return token
 
token=genToken()

def validate(username, password):                       #Funzione per il controllo delle credenziali inserite nella pagina di login 
    completion = False
    con = sqlite3.connect('./Database.db')              #si crea un collegamento al database, dove c'è una tabella in cui e salvato l'elenco degli utenti e delle relative password 
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")                  #leggo il contenuto della tabella e assegno la lista degli utenti e della password a rows
    rows = cur.fetchall()
    for row in rows:                                    #controllo se c'è una corrispondenza delle credenziali inserite nella pagina di login e almeno una delle credenziali presenti nel database
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:                            #quando si trova una corrispondenza fra l'utente inserito e una credenziale, si va il controllo sulla password  
            completion=check_password(dbPass, password) 
    return completion                                   #completion avrà valore True se si è trovata una corrispondenza

def check_password(hashed_password, user_password):     #funzione per un semplice confronto fra la password inserita e quella presente all'interno del DB 
    return hashed_password == user_password

Ab=AlphaBot()                                           #istanza della classe alphabot

@app.route('/', methods=['GET', 'POST'])                #Gestione delle azioni pagina di login
def login():
    error = None        
    if request.method == 'POST':                        #slavataggio delle credenziali inserite quando si preme il pulsante 
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)       #controllo delle credenziali
        if completion == False:                         #se non esiste un utente nel database che corrisponde, bisognerà inserirne delle altre
            error = 'Invalid Credentials. Please try again.'
        else:                                           #viene creato il cookie con il nome utente inserito che verrà utilizzato successivamente per il salvataggio delle azioni eseguite dall'utente nel DB
            resp = make_response(redirect(url_for('index')))    #richiamo alla pagina di controllo dell'alphabot   
            resp.set_cookie('username', username)
            return resp
    return render_template('login.html', error=error)


@app.route(f'/{token}', methods=['GET', 'POST'])      #Gestione delle azioni nella pagina di controllo dell'alphabot  
def index():
    con=None
    con = sqlite3.connect('Database.db')              #si accede al database per salvare l'azione che l'utente eseguirà
    cur = con.cursor()
    u = request.cookies.get('username')
    now = datetime.now()                              #salvataggio di data e ora in cui è stato eseguito il comando
    data_str = now.strftime("%d/%m/%y %H:%M:%S")
    if request.method == 'POST':                      #gestione del controller con le freccie e dei comandi personalizzati inseriti nel box
        if request.form.get('forward') == 'forward':
            Ab.forward()
            comm="forward"
        if  request.form.get('backward') == 'backward':
            Ab.backward()
            comm="backward"
        if  request.form.get('left') == 'left':
            Ab.left()
            comm="left"
        if  request.form.get('right') == 'right':
            Ab.right()
            comm="right"
        if  request.form.get('conf') == 'conferma':
            comandoPersonalizzato(request.form['textcp'], Ab)
            comm=request.form['textcp']
                                                    #salvataggio nel db dell'azione richiesta dal utente
        cur.execute(f"INSERT INTO RegistroUserCommand (user,command,data) VALUES ('{request.cookies.get('username')}','{comm}','{data_str}')")
        cur.execute("commit")
    return render_template("index.html")

app.run(debug=True, host='0.0.0.0')