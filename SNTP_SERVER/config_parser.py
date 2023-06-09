import configparser


def parse_config_data() -> tuple:
    config = configparser.ConfigParser()
    config.read('config.ini')
    delay = config.getint('DEFAULT', 'DELAY')
    host = config.get('DEFAULT', 'HOST')
    port = config.getint('DEFAULT', 'PORT')
    return delay, host, port
