import json
import requests
import threading

import parser
from flask import Flask, jsonify, request
from urllib.parse import urlparse
from log import get_logger
from random_address import get_unique_addr
from distribute_fund import *
from queue import Queue
from utils import *

# Global Definitions
app = Flask(__name__)
proc_queue = Queue()
unique_addr = get_unique_addr()
cfg = {}
no_data_response = {
        'message': "Error: parameter 'addresses' not found or data not in json type"
        }
bad_data_response = {
        'message': "Error: parameter 'addresses' should be a non-empty list of addresses"
        }

@app.route('/sendmoney/', methods=['POST'])
def issue_deposit_addr():
    print('inside post method')
    try:
        values = request.get_json()
        addresses = values.get('addresses')
    except:
        return jsonify(no_data_response), 400
    try:
        assert isinstance(addresses, list)
        assert len(addresses) > 0
    except:
        return jsonify(bad_data_response), 400

    # now we has the data in hand
    deposit_addr = next(unique_addr)
    distributer = Distributer(cfg['houseaccount'], cfg['maxfundwaittime'])
    distributer.prepare(deposit_addr, addresses)
    proc_queue.put(distributer)
    response = {
        'address': addresses,
        'deposit_address': deposit_addr,
        'expiry time': cfg['maxfundwaittime']
    }
    # add to global queue
    proc_queue.put(distributer)
    return jsonify(response), 200

@app.route('/testget/', methods=['GET'])
def testget():
    # global users
    # values = request.get_json()
    # addresses = values.get('addresses')
    
    deposit_address = next(unique_addr)

    # response = {
    #     'deposit_address': deposit_address,
    #     'expire_time': 10
    # }

    # d = Distributer(house_account, max_wait_time)
    # d.prepare(deposit_address, addresses)
    # users.append(d)
    deposit_addr = next(unique_addr)
    distributer = Distributer(cfg['houseaccount'], cfg['maxfundwaittime'])
    distributer.prepare(next(unique_addr), ['test1','test2'])
    handle_mix_request(distributer).then(success, fail) 
    response = {
        'deposit_address': deposit_addr,
        'expiry time': cfg['maxfundwaittime']
    }

    return jsonify(response), 200

def flaskThread(host, port):
    print('in the flaskThread')
    app.run(host = host, port = port, threaded = True)
    

if __name__ == "__main__":
    # _thread.start_new_thread(flaskThread, ())
    # app.run(host='0.0.0.0', port=5000)
    cfg = parser.load_config()
    print('cfg:', cfg)
    logger = get_logger(cfg['appname'], verbose = cfg['verbose'])
    logger.info('test logger')

    flask_thread = threading.Thread(target = flaskThread, args = (cfg['host'], cfg['port']))
    flask_thread.start()
    
    # test
    for i in range(10):
        distributer = Distributer(cfg['houseaccount'], cfg['maxfundwaittime'])
        distributer.prepare(next(unique_addr), ['test1','test2'])
        handle_mix_request(distributer).then(success, fail)
    
    print(66666666)

    flask_thread.join()


