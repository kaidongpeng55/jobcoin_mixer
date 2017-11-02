import requests

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

def success(a):
    print('success')

def fail(a):
    print('fail')

