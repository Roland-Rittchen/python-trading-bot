
class Position(object):
    def __init__(self):
        self.side = 'short' #long
        self.size = 100
        self.entry = 0.0000
        self.sl = 0.0000
        self.tp = 0.0000
        
    def calcVal(self, current):
        return (current)*self.size
    def calcRisk(self, current):
        return (current-self.sl)*self.size
