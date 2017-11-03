import time
import random
from math import ceil, floor

def main(transfer_amount):
    jobcoin_minunit = 0.001
    random.seed(time.time())
    outaddrs = [ 'address-%d' % i for i in range(random.randint(1, 5))]
    print('number of addresses in total:', len(outaddrs))
    num_times = random.randint(floor(transfer_amount * 0.7), ceil(transfer_amount * 1.2))
    print('total number of transfers: ', num_times)
    while num_times > 0 and transfer_amount > 0.0:
        print('round ', num_times)
        # determine an address to transfer jobcoin
        addr_idx = random.randint(0, len(outaddrs) - 1)
        print('send to :', outaddrs[addr_idx])
        if num_times != 1:
            if floor(transfer_amount/jobcoin_minunit) == 1:
                random_amount = transfer_amount # this means amount left is less than two times of min unit, empty
            elif floor(transfer_amount/jobcoin_minunit) == 0:
                break # does not make sense to let us loose money
            else:
                rand_amount = jobcoin_minunit * random.randrange(1, floor(transfer_amount / jobcoin_minunit), 1)
        else:
            rand_amount = transfer_amount # as this is the last transfer, we empty the transfer_amount
        #send_coins(base_url, distributer.fund, distributer.outaddrs[addr_idx], rand_amount)
        print('amount:', rand_amount)
        transfer_amount -= rand_amount
        print('amount left to be transferred: ', transfer_amount)
        num_times -= 1

if __name__ == "__main__":
    main(float(input()))

