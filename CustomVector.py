__author__ = 'aferral'
def changeRef(newOr,actualPoint):
    return actualPoint - newOr

class VectorCustom:

    def __init__(self):
        self.vals = []
        pass
    def add(self,val):
        self.vals.append(val)
    def __mul__(self, y ):

        sum = 0
        x = self
        if len(x) != len(y):
            return None
        for inde in range(x.vals):
            sum += x[inde] * y[inde]
        return sum

