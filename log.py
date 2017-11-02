import logging
import os
import errno
from datetime import datetime

# check if the directory that used to store log files already exists;
# if not, create the directory
def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

# return logger object ready for use
def get_logger(app, verbose = False):
    logger = logging.getLogger(app)
    mkdir_p(os.path.dirname('logs/')) 
    # use timestamp as the name of the logfile
    hdlr = logging.FileHandler('logs/' + app + datetime.now().strftime('%Y%m%d%H%M%S') + '.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO if verbose == 'True' else logging.WARNING)
    return logger
