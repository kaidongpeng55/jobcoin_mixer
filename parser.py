import configparser

def load_config():
    '''
    small wrapper to read all the configs from the config file
    combine all sections together and return as a single dictionary
    '''
    config = configparser.ConfigParser()
    config.read('jobcoin_mixer.cfg')
    d = dict(config['DEFAULT'])
    for s in config.sections():
        d = {**d, **dict(config[s])}
    return d

