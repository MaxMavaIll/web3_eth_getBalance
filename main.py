import toml
import time
import logging
import requests

from logging.handlers import RotatingFileHandler
from function import runtime_check, make_request_rpc
from bot_tg.bot import send_message

config = toml.load("config.toml")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log_s = logging.StreamHandler()
log_s.setLevel(logging.INFO)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_s.setFormatter(formatter2)

log_f = RotatingFileHandler(
    f"logs/main.log",
    maxBytes=config['logging']['max_log_size'] * 1024 * 1024, 
    backupCount=config['logging']['backup_count'])
log_f.setLevel(logging.DEBUG)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_f.setFormatter(formatter2)

log.addHandler(log_s)
log.addHandler(log_f)

def main():
    
    while True:
        
        tmp1 = 1
        for addr_url in config['list_wallet_rpc']:
            log.info(f"------ {tmp1}. {addr_url[0]} ------")
            try:
                make_request_rpc(address=addr_url[0], eth_rpc=addr_url[1])
            except requests.exceptions.HTTPError: 
                log.exception(f"{tmp1}. url: {addr_url[1]} get:\n")
            tmp1 += 1
        
        if config['tg_bot']['lighthouse']['enable'] and runtime_check(config['tg_bot']['lighthouse']['time']):
            send_message(config['tg_bot']['lighthouse']['message'])
        
        log.info(f"Wait {config['time_sleep']} sec")
        time.sleep(config['time_sleep'])



if __name__ == "__main__":
    main()