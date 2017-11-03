from threading import Thread
from flask import Flask, jsonify, request, render_template
from queue import Queue
from init import *
from distribute_fund import *
from utils import *


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

def main():
    # run flask thread on the background
    flask_thread = Thread(target = flaskThread, args = ())
    flask_thread.start()
    
    # start polling for mix requests
    prev_deposit = '' # for de-dup
    while True:
        next_task = poll_mix_request(
                partial(check_queue, proc_queue),
                timeout = int(cfg['maxtimeout']),
                granularity = int(cfg['pollinggranularity']))
        if next_task != None:
            if next_task.deposit == prev_deposit:
                continue
            prev_deposit = next_task.deposit
            Thread( target = MixRequestThread, args = (next_task,)).start()

    # wait until flaks thread finishes    
    flask_thread.join()

if __name__ == "__main__":
    main()

