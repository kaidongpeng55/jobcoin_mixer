from random import seed, randint, randrange
from time import sleep, time as Time
from math import floor, ceil
from functools import partial
from distributer import Distributer
from utils import *
from init import *

def flaskThread():
    logger.info('Flask thread spawned')
    app.run(host = cfg['host'], port = cfg['port'], threaded = True)

def MixRequestThread(next_task):
    logger.info('New MixRequest thread spawned')
    handle_mix_request(next_task, distribute_fund, fail)

def calculate_fee(rawamount):
    '''
    Although this percent way of calculating fee is simple
    and probably does not worth a function, this is left to
    provide support to more complexed fee and rebate scheme
    '''
    return rawamount * float(cfg['feerate']) # 10 bps 

def distribute_fund(distributer):
    '''
    logic for determing how to distribute the funds
    first transfer to house account
    '''
    logger.info('Distributing fund from %s with amount %f' % (distributer.deposit, distributer.rawamount))
    r = send_coins(distributer.deposit, distributer.fund, distributer.rawamount)
    # error checking
    if r.status_code != SUCCESS_CODE or "error" in r.json():
        # log error
        logger.error('HTTP POST ERROR: %d: when trying to send %f from %s to %s; Reason: %s'
                % (r.status_code, distributer.rawamount, distributer.deposit, distributer.fund, r.reason))
        return
    transfer_amount = distributer.rawamount - calculate_fee(distributer.rawamount)
    # randomly generate numbe of times to transfer the amount ~ 1 time per 1 jobcoin
    jobcoin_minunit = float(cfg['jobcoinminunit'])
    seed(Time())
    num_times = randint(floor(transfer_amount * 0.7), ceil(transfer_amount * 1.2))
    while num_times > 0 and transfer_amount > ZERO_COIN:
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
        send_coins(distributer.fund, distributer.outaddrs[addr_idx], rand_amount)
        transfer_amount -= rand_amount
        num_times -= 1
    # in case there are some leftovers, check again and 
    # transfer everything to fund before we release this deposit address
    amount = check_balance(distributer.deposit)
    if amount > ZERO_COIN:
        send_coins(distributer.deposit, distributer.fund, amount)
    # log success
    return success(distributer)

def handle_mix_request(distributer, resolve, reject):
    '''
    this function will be called after deposit address
    has been sent to user already
    poll for funds on the deposit address with a expire time
    '''
    logger.info('Handling mix request for deposit address %s' %  distributer.deposit)
    end_time = Time() + int(cfg['maxfundwaittime']) # compute the maximal end time
    amount = check_balance(distributer.deposit)
    hasmoney = amount > ZERO_COIN
    while not hasmoney and Time() < end_time:    # loop until the condition is false and timeout not exhausted
        sleep(float(cfg['pollinggranularity']) / MILLISECOND_FACTOR)        # release CPU cycles
        amount = check_balance(distributer.deposit)
        hasmoney = amount > ZERO_COIN
    # one last check
    amount = check_balance(distributer.deposit)
    hasmoney = amount > ZERO_COIN
    # condition check if money is not deposited, log error and
    # terminate the handler
    if hasmoney and amount != 0:
        distributer.load_money(amount)
        return resolve(distributer)
    else:
        return reject(distributer)

