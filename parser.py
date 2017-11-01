import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('jobcoin_mixer.cfg')
    d = dict(config['DEFAULT'])
    for s in config.sections():
        d = {**d, **dict(config[s])}
    return d


