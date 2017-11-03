import logging
import os
import errno
from datetime import datetime

def mkdir_p(path):
    '''
    check if the directory that used to store log files already exists;
    if not, create the directory
    '''
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def get_logger(app, verbose = False):
    ''' return logger object ready for use '''
    logger = logging.getLogger(app)
    mkdir_p(os.path.dirname('logs/')) 
    # use timestamp as the name of the logfile
    logging.basicConfig(
            format = '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s',
	    handlers = [
                logging.FileHandler('logs/' + app + datetime.now().strftime('%Y%m%d%H%M%S') + '.log'),
                logging.StreamHandler()
    ])
    logger.setLevel(logging.INFO if verbose == 'True' else logging.WARNING)
    return logger


