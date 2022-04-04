import decimal

class Portfolio(object):
    def calcVal(self):
        pass
    def calcRisk(self):
        pass
    def listPositions(self):
        pass
    def posSizing(self):
        pass
    

class Cash(object):
    def ___init__(self, currency, val, sim):
        self.currency = currency
        self.val = val
        self.unrealised_pnl = decimal.Decimal('0.00')
        self.realised_pnl = decimal.Decimal('0.00')
        self.sim = sim

    def calcVal(self, conv):
        if self.sim:
            return self.val*conv
        else:
            return #get cash value from broker

    def payIn(self, val):
        self.val+=val

    def payOut(self, val):
        self.val-=val