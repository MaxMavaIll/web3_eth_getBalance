import datetime
import logging
import toml

from web3 import Web3
from logging.handlers import RotatingFileHandler


config_toml = toml.load('config.toml')

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log_s = logging.StreamHandler()
log_s.setLevel(logging.INFO)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_s.setFormatter(formatter2)

log_f = RotatingFileHandler(f"logs/{__name__}.log",
    maxBytes=config_toml['logging']['max_log_size'] * 1024 * 1024, 
    backupCount=config_toml['logging']['backup_count'])
log_f.setLevel(logging.DEBUG)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_f.setFormatter(formatter2)

log.addHandler(log_s)
log.addHandler(log_f)





def runtime_check(times: str) -> bool:
    time_now = datetime.datetime.now().utcnow().time()
    log.info(f"Get {times} now time {time_now}")

    if times == '':
        return True
    
    elif times != '':
        
        for time in times.split(','):
            time = time.split(":")
            
            if len(time) != 2:
                time.append(0)
                
            log.info(f"{datetime.timedelta()} <= {datetime.timedelta(hours=time_now.hour, minutes=time_now.minute) - datetime.timedelta(hours=int(time[0]), minutes=int(time[1]))} < {datetime.timedelta(seconds=config_toml['time_sleep'])}")
            
            if datetime.timedelta() <= datetime.timedelta(hours=time_now.hour, minutes=time_now.minute) - datetime.timedelta(hours=int(time[0]), minutes=int(time[1]))  < datetime.timedelta(seconds=config_toml['time_sleep']):
                log.info(f"Get True")
                return True
    
    log.info(f"Get False")
    return False

def make_request_rpc(
        address: str,
        eth_rpc: str
):
    web3 = Web3(Web3.HTTPProvider(eth_rpc))

    balance_wei = web3.eth.get_balance(address)
    balance_eth = web3.from_wei(balance_wei, 'ether')

    log.info(f"Баланс гаманця {balance_eth} ETH")