import requests
import json
import time
import random

#Indirizzo dell'alphabot
host = 'http://192.168.0.118:5000/'

while True:
    #Api per la lettura dei sensori
    sens = requests.get(f'{host}/api/v1/sensors/obstacles')
    #Creazione di JSON della lettura dei sensori
    sensArr = sens.json()

    #Casistica dove entrambi i sensori rilevano un ostacolo. Sarà un ostacolo frontale
    if sensArr['right']!=1 and sensArr['left']!=1:
        #Abbiamo gestito un ostacolo frontale, con l'indietreggiamento dell'alphabot
        pot = requests.get(f'{host}/api/v1/motors/both?pwml=-27&pwmr=27&time=.1')
        #E abbiamo scelto di far ruotare il nostro alphabot randomicamente o a sinistra o a destra
        scelta=random.randint(0,1)
        if(scelta==0):
            pot = requests.get(f'{host}/api/v1/motors/both?pwml=-10&pwmr=23&time=.2')
        else:
            pot = requests.get(f'{host}/api/v1/motors/both?pwml=23&pwmr=10&time=.2')
    else:
        #Lettura di ostsacolo a sinistra dell'alphabot 
        if sensArr['left']!=1:
            #facciamo girare l'alphabot verso destra
            pot = requests.get(f'{host}/api/v1/motors/both?pwml=-10&pwmr=23&time=.3')
            print(f"Sinistra:{sensArr['left']}")
        #Lettura dell'ostacolo a detra dell'alphabot
        if sensArr['right']!=1:
            #Facciamo ruotare l'alphabot verso sinistra
            pot = requests.get(f'{host}/api/v1/motors/both?pwml=23&pwmr=10&time=.3')
            print(f"Destra: {sensArr['right']}")
    #Via libera, l'alphabot procede in avanti
    if sensArr['right']==1 and sensArr['left']==1:
        pot = requests.get(f'{host}/api/v1/motors/both?pwml=27&pwmr=-27&time=.3')
