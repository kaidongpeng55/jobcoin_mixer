import parser
from log import get_logger
from random_adress import get_unique_addr


def main():
    cfg = parser.load_config()
    print('cfg:', cfg)
    logger = get_logger(cfg['appname'], verbose = cfg['verbose'])
    logger.info('test logger')



if __name__ == "__main__":
    main()

