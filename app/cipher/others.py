from elGamal import ElGamal as eg
from Cryptodome.Random import random
from client import send, receive
import socket

groupSize = 3
partNum = 2
cipher = eg()
HOST = "172.20.10.6"
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(1)
print("Server started, listening for connections...")
conn, addr = s.accept()

t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t.connect((HOST, PORT))


pkShare = receive(s, conn, addr)
send(cipher.mult(pkShare), t)
pk = receive(s, conn, addr)
cipher.setPK(pk)
send(pk, t)

vector = receive(s, conn, addr)
while vector != None :
    cipher.shuffle(vector)
    send(vector, t)

    quotient = receive(s, conn, addr)
    send(cipher.blindVector(quotient), t)
    blinded = receive(s, conn, addr)
    send(blinded, t)

    decryptionShares = receive(s, conn, addr)
    sendShares = list()
    for i in range(groupSize) :
        decShare = cipher.decShare(blinded[i])
        sendShares.append((decShare * decryptionShares[i]) % cipher.p)
    
    send(sendShares, t)
    vector = receive(s, conn, addr)
send(None, t)

shuffled = receive(s, conn, addr)
blindFactor = random.randrange(1, cipher.p - 1)
encFactor = cipher.encrypt(blindFactor)
c1blind = (shuffled[partNum][0] * encFactor[0]) % cipher.p
c2blind = (shuffled[partNum][1] * encFactor[1]) % cipher.p
shuffled[partNum] = (c1blind, c2blind)
send(shuffled, t)

assignments = receive(s, conn, addr)
send(assignments, t)

assnDecShares = receive(s, conn, addr)
for i in range(groupSize) :
    share = cipher.decShare(assignments[i])
    assnDecShares[i] = (assnDecShares[i] * share) % cipher.p

send(assnDecShares, t)
plainAssignments = receive(s, conn, addr)
gRecipient = plainAssignments[partNum] // blindFactor
recipient = cipher.log(gRecipient)
send(plainAssignments, t)
print(recipient)