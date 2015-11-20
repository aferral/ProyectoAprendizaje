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
    def __repr__(self):
        out = ''
        for elem in self.vals:
            out += '{0:.3f}'.format(elem)+', '
        return out
    def __setitem__(self, key, value):
        self.vals[key] = value
    def __mul__(self, y ):

        sum = 0
        x = self
        if len(x) != len(y):
            raise Exception("Error vector dimension")
        for inde,val in enumerate(y.vals):
            sum += (x[inde] * val)
        return sum

