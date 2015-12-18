__author__ = 'aferral'
def changeRef(newOr,actualPoint):
    return actualPoint - newOr

class VectorCustom:

    def __init__(self):
        self.vals = {}
        pass
    def add(self,name,val):
        self.vals[name] = val
    def __len__(self):
        return len(self.vals)
    def __getitem__(self, item):
        return self.vals[item]
    def __setitem__(self, key, value):
        self.vals[key] = value
    def __repr__(self):
        out = ''
        for elem in self.vals:
            out += str(elem)+' {0:.3f}'.format(self.vals[elem])+' | '
        return out

    def __mul__(self, y ):

        sum = 0
        x = self
        if len(x) != len(y):
            raise Exception("Error vector dimension",len(x),len(y))
        for val in y.vals:
            sum += (x[val] * y[val])
        return sum

