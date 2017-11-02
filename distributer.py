class Distributer:
    def __init__(self, house_account, deposit_addr):
        # initialize a Distributer with a house account
        self.fund = house_account
        self.deposit = deposit_addr
        self.outaddr = []
        self.rawamount = 0 

    def prepare(self, addrs):
        self.outaddr = addrs

