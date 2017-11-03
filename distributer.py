class Distributer:
    '''
    class that maintains all information needed to
    transfer fund to house account and distribute coins
    '''
    def __init__(self, house_account, max_wait_time):
        '''initialize a Distributer with a house account'''
        self.fund = house_account
        self.outaddrs = []
        self.expiretime = max_wait_time # in seconds
        self.rawamount = 0 
        self.prepared = False

    def prepare(self, deposit_addr, addrs):
        '''prepare distributor with necessary info'''
        self.deposit = deposit_addr
        self.outaddrs = addrs
        self.prepared = True

    def load_money(self, amount):
        '''assign the amount of balance to be transferred'''
        self.rawamount = amount

    def isprepared(self):
        '''used a hand check to prevent incomplete distributor to be used'''
        return True if self.prepared else False

    def get_info(self):
        '''convenient way to acces data for debug'''
        return (self.fund, self.deposit, self.outaddrs, self.rawamount)

    def print(self):
        '''convenient method for testing and debug'''
        print("deposit address: ", self.deposit, ", outaddrs: ", self.outaddrs, ", amount:", self.rawamount)

