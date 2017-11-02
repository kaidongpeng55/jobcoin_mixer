from async_promises import Promise
from distributer import Distributer
from functools import partial

def _distribute_fund():
    #  logic for determing 
    pass

def _handle_mix_request(distributer, resolve, reject):
    # this function will be called after deposit address
    # has been sent to user already
    # poll for funds on the deposit address with a expire time
    has_money = True
    amount = 10
    # condition check if money is not deposited, log error and
    # terminate the handler
    if has_money and amount != 0:
        distributer.load_money(amount)
        return resolve(distributer)
    else:
        return reject(distributer)

def handle_mix_request(distributer):
    '''
    returns a Promise object
    '''
    return Promise(partial(_handle_mix_request, distributer))
