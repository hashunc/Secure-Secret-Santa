from elGamal import ElGamal as eg
from Cryptodome.Random import random
from client import send, receive

groupSize = 3
partNum = 0
cipher = eg()
ip = "192.168.0.1"

send(cipher.y, ip)
pk = receive()
cipher.setPK(pk)
send(pk, ip)
receive()

vector = cipher.vector(groupSize)

derange = False
while not derange :
    cipher.shuffle(vector)
    send(vector, ip)
    shuffled = receive()

    quotient = cipher.divide(shuffled, vector)
    send(cipher.blindVector(quotient), ip)
    blinded = receive()
    send(blinded, ip)
    receive()

    decryptionShares = list()
    for ct in blinded :
        decryptionShares.append(cipher.decShare(ct))

    send(decryptionShares, ip)
    sInvVector = receive()
    for i in range(groupSize) :
        pt = (sInvVector[i] * blinded[i][1]) % cipher.p
        derange = pt != 1
        if not derange : break

send(None, ip) # indicates derangement success
receive()

blindFactor = random.randrange(1, cipher.p - 1)
encFactor = cipher.encrypt(blindFactor)
c1blind = (shuffled[partNum][0] * encFactor[0]) % cipher.p
c2blind = (shuffled[partNum][1] * encFactor[1]) % cipher.p
shuffled[partNum] = (c1blind, c2blind)
send(shuffled, ip)

assignments = receive()
send(assignments, ip)
receive()

assnDecShares = list()
for ct in assignments :
    assnDecShares.append(cipher.decShare(ct))
send(assnDecShares, ip)

plainAssignments = receive()
gRecipient = plainAssignments[partNum] // blindFactor
recipient = cipher.log(gRecipient)
send(plainAssignments, ip)
receive()
print(recipient)