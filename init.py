from flask import Flask, jsonify, request, render_template
from queue import Queue
from os import path
from random_address import get_unique_addr
from parser import load_config
from log import get_logger

# Global Definitions
app = Flask(__name__, template_folder = path.abspath('./'))
proc_queue = Queue()
unique_addr = get_unique_addr()
# load global configs
cfg = load_config()
logger = get_logger(cfg['appname'], verbose = cfg['verbose'])
logger.info('Configurations read from file:' + str(cfg))

