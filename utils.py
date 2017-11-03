import requests
import time


# useful definitions
MILLISECOND_FACTOR = 1000.0
no_data_response = {
        'message': "Error: parameter 'addresses' not found or data not in json type"
}
bad_data_response = {
        'message': "Error: parameter 'addresses' should be a non-empty list of addresses"
}

def send_coin(url, fromaddr, toaddr, amount):
    '''
    send jobcoins from one address to another
    url: api url
    fromaddr: address to subtract fund from
    toaddr: address to send fund into
    amount: amount of jobcoin in string format
    '''
    return requests.post(url, {
            'fromAddress': fromaddr,
            'toAddress': toaddr,
            'amount': amount
        }
    )

def check_balance(url, addr):
    return float((requests.get(url + '/api/addresses/' + addr).json())['balance'])



def success(distributer):
    distributer.print()
    print('success')
    

def fail(distributer):
    distributer.print()
    print('fail')


def poll_mix_request(condition, timeout, granularity= 300):
    end_time = time.time() + timeout / MILLISECOND_FACTOR   # compute the maximal end time
    (status, retval) = condition()               # first condition check, no need to wait if condition already True
    while not status and time.time() < end_time:    # loop until the condition is false and timeout not exhausted
        time.sleep(granularity / MILLISECOND_FACTOR)        # release CPU cycles
        (status, retval) = condition()               # first condition check, no need to wait if condition already True
    return retval if status else None 

def check_queue(q):
    try:
        retval = q.get_nowait()
        return (True, retval)
    except:
        return (False, None) 

