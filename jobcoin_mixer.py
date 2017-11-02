from time import time
import json
import hashlib
from hashlib import sha256
from uuid import uuid4

from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests

import parser
from log import get_logger
from random_address import get_unique_addr
from distribute_fund import *

from queue import Queue

def success(a):
    print('success')

def fail(a):
    print('fail')

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
    response = {
        'address': addresses,
        'deposit_address': deposit_addr,
        'expiry time': cfg['maxfundwaittime']
    }
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


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    cfg = parser.load_config()
    print('cfg:', cfg)
    logger = get_logger(cfg['appname'], verbose = cfg['verbose'])
    logger.info('test logger')
    
    # test
    for i in range(10):
        distributer = Distributer(cfg['houseaccount'], cfg['maxfundwaittime'])
        distributer.prepare(next(unique_addr), ['test1','test2'])
        handle_mix_request(distributer).then(success, fail)
    
    app.run(host='0.0.0.0', port=5001)



