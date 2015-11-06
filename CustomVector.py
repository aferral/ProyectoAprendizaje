__author__ = 'aferral'
def changeRef(newOr,actualPoint):
    return actualPoint - newOr

class VectorCustom:

    def __init__(self):
        self.vals = []
        pass
    def add(self,val):
        self.vals.append(val)
    def __len__(self):
        return len(self.vals)
    def __getitem__(self, item):
        return self.vals[int(item)]
    def __mul__(self, y ):

        sum = 0
        x = self
        if len(x) != len(y):
            return None
        for inde,val in enumerate(x.vals):
            sum += x[int(inde)] * val
        return sum

