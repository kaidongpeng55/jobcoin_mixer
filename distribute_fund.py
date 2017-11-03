from distributer import Distributer
from functools import partial
from utils import send_coin, check_balance
import time

def _distribute_fund():
    #  logic for determing 
    pass

def handle_mix_request(url, max_wait_time, distributer, resolve, reject):
    # this function will be called after deposit address
    # has been sent to user already
    # poll for funds on the deposit address with a expire time
    end_time = time.time() + max_wait_time # compute the maximal end time
    print('in handle_mix_request', 'address:', distributer.deposit)
    print('before check balance')
    amount = check_balance(url, distributer.deposit)
    hasmoney = amount > 0.0
    while not hasmoney and time.time() < end_time:    # loop until the condition is false and timeout not exhausted
        time.sleep(0.3)        # release CPU cycles
        amount = check_balance(url, distributer.deposit)
        hasmoney = amount > 0.0
    # one last check
    amount = check_balance(url, distributer.deposit)
    hasmoney = amount > 0.0
    # condition check if money is not deposited, log error and
    # terminate the handler
    print('after checking amount, amount is: ', amount, ', hasmoney is ', 'true' if hasmoney else 'false')
    if hasmoney and amount != 0:
        distributer.load_money(amount)
        return resolve(distributer)
    else:
        return reject(distributer)

