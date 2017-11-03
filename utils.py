import requests
from time import sleep, time as Time
from init import *

# useful definitions
MILLISECOND_FACTOR = 1000.0
ZERO_COIN = 0.0
no_data_response = { 'message': "Error: parameter 'addresses' not found or data not in json type" }
bad_data_response = { 'message': "Error: parameter 'addresses' should be a non-empty list of addresses" }
SUCCESS_CODE = 200
BAD_REQUEST = 400
NOTFOUND = 404
INTERNALERR = 500

def send_coins(fromaddr, toaddr, amount):
    '''
    send jobcoins from one address to another
    url: api url
    fromaddr: address to subtract fund from
    toaddr: address to send fund into
    amount: amount of jobcoin in string format
    '''
    logger.info('Sent %f from %s to %s' % (amount, fromaddr, toaddr))
    return requests.post(cfg['baseurl'] + '/api/transactions', {
            'fromAddress': fromaddr,
            'toAddress': toaddr,
            'amount': amount
        }
    )

def check_balance(addr):
    ''' return balance of given address in float number '''
    return float((requests.get(cfg['baseurl'] + '/api/addresses/' + addr).json())['balance'])

def success(distributer):
    logger.info('Successfully sent from deposit address %s amount %f' % (distributer.deposit, distributer.rawamount))
    
def fail(distributer):
    logger.warning('Failed to sent from deposit address %s amount %f' % (distributer.deposit, distributer.rawamount))

def poll_mix_request(condition):
    '''poll for any pending requests with a timeout and granularity'''
    end_time = Time() + int(cfg['maxtimeout']) / MILLISECOND_FACTOR   # compute the maximal end time
    (status, retval) = condition()               # first condition check, no need to wait if condition already True
    while not status and Time() < end_time:    # loop until the condition is false and timeout not exhausted
        sleep(int(cfg['pollinggranularity']) / MILLISECOND_FACTOR)        # release CPU cycles
        (status, retval) = condition()               # first condition check, no need to wait if condition already True
    return retval if status else None 

def check_queue(q):
    '''helper method of poll_mix_request to check if there are pending requests'''
    try:
        retval = q.get_nowait()
        return (True, retval)
    except:
        return (False, None) 

