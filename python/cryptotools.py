from asyncio.log import logger
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import os

logging_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
lhandler = logging.StreamHandler()
lhandler.setFormatter(logging_format)
logger.setLevel(logging.DEBUG)
logger.addHandler(lhandler)
logger.propagate = False

btc_rpc_port = os.environ['rpcport']
btc_ip = os.environ['btc_ip']
rpcpass = os.environ['rpcpass']
rpcuser = os.environ['rpcuser']
btc_rpc_url = "http://"+btc_ip+":"+btc_rpc_port+"/"
walleturl = "http://"+btc_ip+":"+btc_rpc_port+"/wallet/"
auth = HTTPBasicAuth(rpcuser, rpcpass)
btc_rpc_header = {
  'Content-Type': 'application/json'
}


btc_to_usd_api = "https://api.alternative.me/v1/ticker/bitcoin/?convert=USD"


# Get Current BTC Price
def get_current_price():
    resp = requests.request("GET", btc_to_usd_api)
    data = json.loads(resp.text)
    # Get the BTC Price
    btcprice = float(data[0]['price_usd'])
    logger.info("The Current BTC price is " + str(btcprice))
    return btcprice

# USD TO btc
def usd_to_btc(usd):
    btcp = get_current_price()
    return usd / btcp 

# Function to create BTC wallet
def create_wallet(walletname):
    payload = json.dumps({"jsonrpc": "1.0", "id": "create_wallet", "method": "createwallet", "params": {"wallet_name": walletname, "load_on_startup": True}})
    response = requests.request("POST", btc_rpc_url, auth=auth, headers=btc_rpc_header, data=payload)
    logger.info("Creating wallet status code {} for the wallet {}".format(response.status_code, walletname))
    logger.debug(response.text)
    return response.status_code

def send_btc(walletname, address, amount):
    payload = json.dumps({"jsonrpc": "1.0", "id": "transaction", "method": "sendtoaddress", "params": {"address": address, "amount": amount, "subtractfeefromamount": True,  "estimate_mode": "economical"}})
    response = requests.request("POST", walleturl+walletname, auth=auth, headers=btc_rpc_header, data=payload)
    logger.info("The wallet {} sent {} to the BTC address {} : The return code of the transaction is {}".format(walletname, amount, address, response.status_code))
    logger.info(response.json())
    if response.status_code == 200:
        new_send_opt = response.json()
        return True, new_send_opt['result']
    else:
        return False, response.json()

# Get wallet address
def wallet_addr(walletname):
    payload = json.dumps({"jsonrpc": "1.0", "id": "wallet", "method": "getnewaddress", "params": []})
    response = requests.request("POST", walleturl+walletname, auth=auth, headers=btc_rpc_header, data=payload)
    out = response.json()
    logger.info("The wallet {} new address is {}".format(walletname, out['result']))
    return out['result']

# Get User's wallet balance
def get_wallet_balance(walletname):
    payload = json.dumps({"jsonrpc": "1.0", "id": "wallet", "method": "getbalance", "params": []})
    response = requests.request("POST", walleturl+walletname, auth=auth, headers=btc_rpc_header, data=payload)
    logger.info(response.json())
    out_bal = response.json()
    if response.status_code == 200:
        logger.info("the wallet {} balance is {}".format(walletname, out_bal['result']))
        return float(out_bal['result'])
    else:
        return None


# Get each TxID for recieved amount
def get_n_valid_tx(walletname):
    data = []
    payload = json.dumps({"jsonrpc": "1.0", "id": "userwallet", "method": "listtransactions", "params": []})
    response = requests.request("POST", walleturl+walletname, auth=auth, headers=btc_rpc_header, data=payload)
    output = response.json()
    logger.info(output)
    if output['result'] == []:
        return False
    for item in output['result']:
        if item['amount'] > 0:
            a = {"wallet": walletname, "txid": item['txid'], "conf": item['confirmations'], "amount": item['amount']}
            data.append(a)
    logger.info({"wallet": walletname, "Data": data})
    return data

# Get all tx amount
def get_all_tx(walletname):
    data = []
    payload = json.dumps({"jsonrpc": "1.0", "id": "userwallet", "method": "listtransactions", "params": []})
    response = requests.request("POST", walleturl+walletname, auth=auth, headers=btc_rpc_header, data=payload)
    output = response.json()
    logger.info(output)
    if output['result'] == []:
        return False
    else:
        for item in output['result']:
            a = {"wallet": walletname, "txid": item['txid'], "conf": item['confirmations'], "amount": item['amount']}
            data.append(a)
    logger.info({"wallet": walletname, "Data": data})
    return data