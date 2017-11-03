# jobcoin_mixer
a jobcoin mixer that enhances anonymity of cryptocurrency 

## Installation
```
chmod u+x configure
./configure
python3 jobcoin_mixer.py
```
## Configurations
Please refer to `jobcoin_mixer.cfg` for details and parameter modifications

## Overview
Once started, the program will spawn a Flask thread to render a server with
host and post read from the configuration file. The flask server is very light-weight,
and it provides a simple UI at `/` for user to supply a list of addresses and
the retrieve a one-time unique deposit address. UI will send HTTP POST to `/sendmoney`
with the addresses and the response will return the deposit address along with an expiry
time. This is because we will only handle requests from people who transfer money in a 
timely manner: the `MaxFundWaitTime` in the configuration file specifies the expiry time
for each deposit address. Then the POST handler will assemble the information and push it
into the request queue, which is thread safe.The main thread of the program will poll for
any new mix requets from users. This is done by checking whether there are elements in the
shared queue. Once there are new requests, new threads will be spawned to process them parallelly.
This is because we allow for an expiry time (currently ~30s) for user to transfer fund into the 
deposit address, which can make processing of one mix request to be slow. Therefore, it would not
make sense to let one block all the others, as other requests may already have fund ready.
Then once the funds are ready in the deposit address, they are transferred into the house account
(specified by the `HouseAccount` parameter in the configuration file), Then a fee (rate determined by
the parameter `FeeRate` in the configuration file) will be deducted, and the rest of the funds will
be splitted into random number of portions, each portion sent to one random address from the list
provided by the user. That way, it is hard for other people to detect by the amount of funds as
well as the number of transactions.

## Component Breakdown
#### configure
Script to install python3 package dependencies
#### distribute_funds.py
File that contains logics about checking balance and transferring funds randomly
#### distributer.py
Contains the definition of `Class Distributer` which contains relevant information
about jobcoin transfer such as deposit address, list of user address and jobcoin amount.
#### init.py
Initialize global objects, such as logger, configurations, uuid generator object and flask app.
#### jobcoin_mixer.cfg
Configuration file that contains values of various Application parameters.
#### jobcoin_mixer.py
Main File/Entry Point of the project. It contains the controllers for the flask sever
(web interface, POST api) and the definition of main function.
#### log.py
Specifiy logging behavriors. Print log into file as well as stdout stream.
#### parser.py
Configuration file parser and combiner.
#### random_address.py
A generator function that generates uuid as string every time it yields.
#### test.py
Simple utility to test distribute fund logic
#### utils.py
Contains common utilities such as POST/GET wrappers and useful constants.






