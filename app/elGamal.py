from Cryptodome.PublicKey import ElGamal as eg
from Cryptodome.Random import random


class ElGamal:
    def __init__(self) : # makes random sk and pk within group
        # TODO make 2048 bit modulus p and generator g
        # i used 512 bits because 2048 bit generation did not complete in ~20 minutes
        self.p = 11774363152266578095067526258816830539166139106121849415818805169740043699372268857521995275805757855836228222867569659145695568012997698531776585688862219
        self.g = 2534890524550132494481097005281920111219579664822426722657432332577436305162772648334556738057313044668101379845453788943682939971615935369166151340598061

        self.x = random.randrange(1, self.p - 1)
        self.y = pow(self.g, self.x, self.p)

    def setPK(self, pk) : # get pk for group
        self.pk = pk
        return
    
    def setSK(self, sk) : # for testing decryption, not for actual use
        self.x = sk
        self.pk = pow(self.g, sk, self.p)
        return

    
    def encrypt(self, message:int) : # ElGamal encryption
        y = random.randrange(1, self.p - 1) # random number y in group
        s = pow(self.pk, y, self.p)         # s is pk raised to y
        c1 = pow(self.g, y, self.p)         # c1 is g raised to y
        c2 = message * int(s)               # c2 is the message times s
        return (c1,c2)              # ciphertext is (c1,c2)

    def decrypt(self, ct) : # ElGamal encryption
        c1, c2 = ct
        s = pow(c1, int(self.x), self.p)
        sInv = pow(s, self.p-2, self.p) # inverting by raising to p - 2
        m = (c2 * sInv) % self.p
        return m

    def mult(self, factor, **kwargs) : # raise with given element, factor, and exponent
        element = kwargs.get('element', self.g)
        exp = kwargs.get('exp', self.x)
        return (factor * pow(int(element), int(exp), int(self.p))) % self.p
    
    def vector(self, size) :
        vector = list()
        for i in range(size) :
            vector.append(
                self.encrypt(
                    self.mult(1, element=self.pk, exp=i+1)))
        return vector
    
    def shuffle(self, vector:list[int]) : # re-encrypt and shuffle given vector
        for i in range(len(vector)) :
            y = random.randrange(1, self.p - 1)
            c1, c2 = vector[i]
            c1 = self.mult(c1, exp=y)
            c2 = self.mult(c2, element=self.pk, exp=y)
            vector[i] = (c1,c2)
        random.shuffle(vector)
        return
    
    def divide(self, vector, vectorShuffle) :
        quotient = list()
        for i in range(len(vector)):
            c1Vector, c2Vector = vector[i]
            c1Shuffle, c2Shuffle = vectorShuffle[i]
            c1inverse = pow(c1Shuffle, self.p-2, self.p)
            c2inverse = pow(c2Shuffle, self.p-2, self.p)
            c1 = (c1Vector * c1inverse) % self.p
            c2 = (c2Vector * c2inverse) % self.p
            quotient.append((c1,c2))
        return quotient
    
    def blind(self, ct, y) :
        c1, c2 = ct
        c1 = pow(c1, y, self.p)
        c2 = pow(c2, y, self.p)
        return (c1,c2)
    
    def blindVector(self, vector) :
        blinded = []
        for ct in vector :
            blinded.append(self.blind(ct, random.randrange(1, self.p-1)))
        return blinded
    
    def unblind(self, pt, y) : # unused
        return pow(pt, self.p-y-1, self.p)
    
    def decShare(self, ct) : # returns share of inverse of s for decryption
        c1 = pow(ct[0], self.x, self.p)
        return pow(c1, self.p-2, self.p)
    
    def log(self, gi) :
        participant = 1
        while gi != self.g :
            participant += 1
            gi = self.mult(gi, exp = self.p - 2)
        return participant

    
    
