import time
from random import seed, randint, randrange
from math import floor, ceil
from functools import partial
from distributer import Distributer
from utils import *

def flaskThread(app, host, port):
    app.run(host = host, port = port, threaded = True)

def MixRequestThread(url, max_wait_time, next_task):
    handle_mix_request(url, max_wait_time, next_task, distribute_fund, fail)

def calculate_fee(rawamount):
    '''
    Although this percent way of calculating fee is simple
    and probably does not worth a function, this is left to
    provide support to more complexed fee and rebate scheme
    '''
    return rawamount * 0.001 # 10 bps 

def distribute_fund(distributer, base_url):
    '''
    logic for determing how to distribute the funds
    first transfer to house account
    '''
    r = send_coins(base_url, distributer.deposit, distributer.fund, distributer.rawamount)
    # error checking
    if r.status_code != 200 or "error" in r.json():
        # log error
        return fail(distributer)# abort, no fund can be transferred from deposit
    transfer_amount = distributer.rawamount - calculate_fee(distributer.rawamount)
    # randomly generate numbe of times to transfer the amount ~ 1 time per 1 jobcoin
    jobcoin_minunit = 0.001
    seed(time.time())
    num_times = randint(floor(transfer_amount * 0.7), ceil(transfer_amount * 1.2))
    while num_times > 0 and transfer_amount > 0.0:
        # determine an address to transfer jobcoin
        addr_idx = randint(0, len(distributer.outaddrs) - 1)
        if num_times != 1:
            if floor(transfer_amount / jobcoin_minunit) == 1:
                random_amount = transfer_amount # this means amount left is less than two times of min unit, empty
            elif floor(transfer_amount / jobcoin_minunit) == 0:
                break # does not make sense to let us loose money
            else:
                rand_amount = jobcoin_minunit * randrange(1, floor(transfer_amount / jobcoin_minunit), 1)
        else:
            rand_amount = transfer_amount
        send_coins(base_url, distributer.fund, distributer.outaddrs[addr_idx], rand_amount)
        transfer_amount -= rand_amount
        num_times -= 1
    # in case there are some leftovers, check again and 
    # transfer everything to fund before we release this deposit address
    amount = check_balance(base_url, distributer.deposit)
    if amount > 0.0:
        send_coins(base_url, distributer.deposit, distributer.fund, amount)
    # log success
    return success(distributer)

def handle_mix_request(base_url, max_wait_time, distributer, resolve, reject):
    '''
    this function will be called after deposit address
    has been sent to user already
    poll for funds on the deposit address with a expire time
    '''
    end_time = time.time() + max_wait_time # compute the maximal end time
    print('in handle_mix_request', 'address:', distributer.deposit)
    print('before check balance')
    amount = check_balance(base_url, distributer.deposit)
    hasmoney = amount > 0.0
    while not hasmoney and time.time() < end_time:    # loop until the condition is false and timeout not exhausted
        time.sleep(0.3)        # release CPU cycles
        amount = check_balance(base_url, distributer.deposit)
        hasmoney = amount > 0.0
    # one last check
    amount = check_balance(base_url, distributer.deposit)
    hasmoney = amount > 0.0
    # condition check if money is not deposited, log error and
    # terminate the handler
    print('after checking amount, amount is: ', amount, ', hasmoney is ', 'true' if hasmoney else 'false')
    if hasmoney and amount != 0:
        distributer.load_money(amount)
        return resolve(distributer, base_url)
    else:
        return reject(distributer)

