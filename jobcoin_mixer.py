import json
import requests
import threading
import os

import parser
from flask import Flask, jsonify, request, render_template
from urllib.parse import urlparse
from log import get_logger
from random_address import get_unique_addr
from distribute_fund import *
from queue import Queue
from utils import *

# Global Definitions
app = Flask(__name__, template_folder = os.path.abspath('./'))
proc_queue = Queue()
unique_addr = get_unique_addr()
cfg = {}

@app.route('/', methods=['GET'])
def ui():
    return render_template('ui/index.html')

@app.route('/sendmoney/', methods=['POST'])
def issue_deposit_addr():
    try:
        values = request.get_json()
        addresses = values.get('addresses')
    except:
        print('no  addresses')
        return jsonify(no_data_response), 400
    try:
        assert isinstance(addresses, list)
        assert len(addresses) > 0
    except:
        print('addresses is', addresses)
        return jsonify(bad_data_response), 400

    # now we has the data in hand
    deposit_addr = next(unique_addr)
    distributer = Distributer(cfg['houseaccount'], cfg['maxfundwaittime'])
    distributer.prepare(deposit_addr, addresses)
    response = {
        'addresses': addresses,
        'deposit_address': deposit_addr,
        'expiry_time': cfg['maxfundwaittime']
    }
    # add to global queue
    proc_queue.put(distributer)
    return jsonify(response), 200

@app.route('/testget/', methods=['GET'])
def testget():
    deposit_address = next(unique_addr)
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

def MixRequestThread(url, max_wait_time, next_task):
    handle_mix_request(url, max_wait_time, next_task, distribute_fund, fail)

if __name__ == "__main__":
    # load global configs
    cfg = parser.load_config()
    print('cfg:', cfg)
    logger = get_logger(cfg['appname'], verbose = cfg['verbose'])
    logger.info('test logger')

    # run flask thread on the background
    flask_thread = threading.Thread(target = flaskThread, args = (cfg['host'], cfg['port']))
    flask_thread.start()
    
    # start polling for mix requests
    prev_deposit = '' # for de-dup
    while True:
        print('new loop')
        next_task = poll_mix_request(
                partial(check_queue, proc_queue),
                timeout = int(cfg['maxtimeout']),
                granularity = int(cfg['pollinggranularity']))
        if next_task != None:
            if next_task.deposit == prev_deposit:
                continue
            prev_deposit = next_task.deposit
            threading.Thread(
                    target = MixRequestThread,
                    args = (cfg['baseurl'], int(cfg['maxfundwaittime']), next_task)).start()

    # wait until flaks thread finishes    
    flask_thread.join()


