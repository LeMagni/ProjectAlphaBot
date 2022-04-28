import socket as sck
import threading as thr
import logging
nick_ip_dict={}

logging.basicConfig(level=logging.DEBUG)        #fa stampare tutti i loggin.

def forward():
    logging.info(f"forward")

def stop():
    logging.info(f"stop")

def backward():
    logging.info(f"back")

def left(self, speed=30):
    logging.info(f"left:{speed}")

def right(speed=30):
    logging.info(f"right:{speed}")
    
def set_pwm_a(value):
    logging.info(f"pwm_a:{value}")

def set_pwm_b(value):
    logging.info(f"pwm_b:{value}")


class Client_Manager(thr.Thread):
    def __init__(self,connection,address):
        thr.Thread.__init__(self) #super di Java
        self.connection=connection
        self.address=address
        self.running=True
    def run(self):
        while self.running:
            data=self.connection.recv(4096)
            msg=data.decode()
            msg = msg.split(":")
            if msg[0] == "com" and msg[2] == "pot1" and msg[4] == "pot2":
                if msg[1] == "forward":
                    forward()
                if msg[1] == "stop":
                    stop()
                if msg[1] == "backward":
                    backward()
                if msg[1] == "right":
                    right()
                if msg[1] == "left": 
                    left()
                set_pwm_a(msg[3])
                set_pwm_b(msg[5])
                #self.connection.sendall("0:Sintassi corretta".encode())
            else:
                logging.debug("Errore di sintassi")
                """
                self.connection.sendall("1:Errore di sintassi".encode())
                data = self.connection.recv(4096)
                if data.decode() == 0:
                    logging.debug("Client ha capito l'errore")
                """

def main():
    s = sck.socket(sck.AF_INET,sck.SOCK_STREAM)
    s.bind(("0.0.0.0",5000))
    s.listen()

    while True:
        connection, address=s.accept()
        client=Client_Manager(connection,address)
        client.start()

if __name__=="__main__":
    main()