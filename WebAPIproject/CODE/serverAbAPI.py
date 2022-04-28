from flask import Flask, jsonify, request
import socket as sck
import threading as thr 
import time
import RPi.GPIO as GPIO
import time
#import alphabot

#Indirizzo alphabot
host = '192.168.0.118'
#Sensori di destra e di sinistra
DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

#Classe alphabot già sfrutatto nei codici precedenti dell'alphabot
class AlphaBot(object):
    
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
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
    
    #Settaggio dei motori in base ai valori passati attraverso API
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

Ab = AlphaBot()

app = Flask(__name__)
app.config["DEBUG"] = True

#Lettura dei sensori
@app.route('/api/v1/sensors/obstacles', methods=['GET'])
def sensori():
    #Per poi facilitare la traformazione dei dati in un JSON, inseriamo i valori letti in un dizionazrio 
    sensori={}
    sensori["left"] = GPIO.input(DL)
    sensori["right"] = GPIO.input(DR)

    return jsonify(sensori)

#Settaggio dei motori dell'alphabot in base ai moviemnti selezionati dal client 
@app.route('/api/v1/motors/both', methods=['GET'])
def motori():
    pwml = request.args['pwml']
    pwmr = request.args['pwmr']
    temp = request.args['time']

    AlphaBot.set_motor(Ab, int(pwml), int(pwmr))

    return f'{pwml},{pwmr}'

app.run(debug=True, host=host)

if __name__=="___main___":
    app.run()