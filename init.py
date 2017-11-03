from random_address import get_unique_addr
from flask import Flask, jsonify, request, render_template
from log import get_logger
from queue import Queue
import parser
import os

# Global Definitions
app = Flask(__name__, template_folder = os.path.abspath('./'))
proc_queue = Queue()
unique_addr = get_unique_addr()
# load global configs
cfg = parser.load_config()
logger = get_logger(cfg['appname'], verbose = cfg['verbose'])
logger.info('Configurations read from file:' + str(cfg))

