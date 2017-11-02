class Distributer:
    '''
    class that maintains all information needed to
    transfer fund to house account and distribute coins
    '''
    def __init__(self, house_account, max_wait_time):
        # initialize a Distributer with a house account
        self.fund = house_account
        self.outaddrs = []
        self.expiretime = max_wait_time # in seconds
        self.rawamount = 0 
        self.prepared = False

    def prepare(self, deposit_addr, addrs):
        self.deposit = deposit_addr
        self.outaddr = addrs

    def load_money(self, amount):
        self.rawamount = amount

    def isprepared(self):
        return True if self.prepared else False

    def get_info(self):
        return (self.fund, self.deposit, self.outaddrs, self.rawamount)
