from elGamal import ElGamal as eg
from Cryptodome.Random.random import randrange
from copy import deepcopy

# testing elgamal class functions

# encryption, decryption test
message = 12345678910
cipher = eg()
cipher.setPK(cipher.y) # set group pk to individual pk for testing
ct = cipher.encrypt(message)
result = cipher.decrypt(ct)
print(result)
print(message == result)

# secret key share test
shares = []
ciphers = []
groupSize = 5

pkGen = 1
for i in range(groupSize) :
    cipher = eg()
    pkGen = cipher.mult(pkGen)
    shares.append(int(cipher.x))
    ciphers.append(cipher)

sk = sum(shares) % (cipher.p -1)
pk = pow(cipher.g, sk, cipher.p)

#print(pow(cipher.g, cipher.p, cipher.p))
#print(pow(cipher.g, 1, cipher.p))
print(f'Real key is {"not" if pk!=pkGen else ""}equal to generated key.\nReal:\n{pk}\nGenerated:\n{pkGen}')

# re-encryption shuffle test
master = eg()
master.setSK(sk)

for ciph in ciphers :
    ciph.setPK(pk)
vector = master.vector(groupSize)


originalVector = deepcopy(vector)
for ciph in ciphers :
    ciph.shuffle(vector)

quotient = master.divide(originalVector,vector)
quotient = master.blindVector(quotient)
for i in range(groupSize) :
    vector[i] = master.decrypt(vector[i])
    originalVector[i] = master.decrypt(originalVector[i])
    quotient[i] = master.decrypt(quotient[i])

print("Quotients of original vector divided by vector (if working, should sometimes include a 1):")
print(quotient)

# blinding, unblinding test
number = 12345678910111213141516
y = randrange(1, master.p-1)
c1Num,c2Num = master.encrypt(number)
c1Y, c2Y = master.encrypt(pow(master.g, y, master.p))
c1 = (c1Num * c1Y) % master.p
c2 = (c2Num * c2Y) % master.p
unblinded = master.decrypt((c1,c2))

print(number)
print((unblinded * pow(master.g, master.p-y-1, master.p)) % master.p)

# small log test
exponent = 5
number = pow(master.g, exponent, cipher.p)
print(master.log(number))