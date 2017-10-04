# Support class for base_class

class PRNG:
    def __init__(self,index):
        self.prime = 4294967291
        self.index = index
        self.seed = 1234
    
    def _nextRandom(self):
        if self.index >= self.prime:
            return self.index
        res = self.index**2 % self.prime
        if self.index<= self.prime/2:
            return res
        else:
            return self.prime-res

    def nextRandom(self):
        self.index = self._nextRandom()+self.seed
        retval = self._nextRandom()^123456789
        return retval
