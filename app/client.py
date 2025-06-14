# Echo client program
#import socket
from elGamal import ElGamal as eg
from Cryptodome.Random import random
import pickle
#from time import sleep

ciph = eg()
ciph.setPK(pow(ciph.g, random.randrange(1,ciph.p - 1), ciph.p))
ctVector = ciph.vector(5)

def send(data, s):
    s.sendall(pickle.dumps(data))
    data = s.recv(1024)
    print('Received', repr(data))

def receive(s, conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            #sleep(3)
            data = conn.recv(1024)
            if not data:
                break
            received_obj = pickle.loads(data)
            print('Received:', received_obj)
            return received_obj