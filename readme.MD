# Bitcoin-Simple-API
This self hosted API will allow you to run bitcoin core to send and recieve bitcoins. 

The application is running on 3 docker containers. nginx, python and bitcoin containers.

You have the option to deploy to the test or main network. 

## Table of Contents
- [Bitcoin-Simple-API](#bitcoin-simple-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Deployment](#deployment)
    - [env Table](#env-table)
    - [RPC Auth Creds](#rpc-auth-creds)
    - [Configure ENV File](#configure-env-file)
    - [Application Deployment](#application-deployment)
  - [API DOCS](#api-docs)
    - [CURL Examples](#curl-examples)
  - [Troubleshooting](#troubleshooting)
  - [Helpful Docs](#helpful-docs)

## Features
- Create wallet
- Generate new wallet address
- Recieve BTC
- Check Balance
- Check Transactions
- Send BTC

## Requirements
- docker-compose v2.15.1 or greater
- docker version 20.10.22 or greater

## Deployment

Once you clone the repo please configure the .env variables 


### env Table
| .env variable | Description |
|:------------|:--------------:|
|subnet|The subnet for the docker network. Example: 172.26.0.0/24|
|hostname|Hostname for nginx configuration Example: localhost|
|nginx_ip|IP of the nginx Container|
|python_ip|IP of the python Container|
|btc_ip|IP of the bitcoin container|
|rpcuser|Username for the bitcoin RPC commands|
|rpcpass|Password for the RPC Commands|
|rpcauth|see [RPC Auth Creds](#rpc-auth-creds) |
|rpcport|Port for Bitcoin Core RPC calls|
|api_key|API key for API calls to python|
|network|testnet or mainnet|



### RPC Auth Creds
To obtain the rpcauth credentials 

```
curl -s https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/rpcauth/rpcauth.py | python3 - <rpcuser> <rpcpass>
```

### Configure ENV File
`cp .example.env .env`


### Application Deployment
`docker-compose up -d`


## API DOCS
Once the application is deployed seccessfully the API Documentation can be reached at `http://<hostname>/docs/`

### CURL Examples

- Create wallet

```
curl --location --request POST 'http://0.0.0.0/create_wallet/' --header 'Authorization: <api_key>' --header 'Content-Type: application/json' --data-raw '{
  "walletname": "testing"
}'
```

- Check Funds

```
curl --location --request POST 'http://0.0.0.0/funds/' --header 'Authorization: <api_key>' --header 'Content-Type: application/json' --data-raw '{
  "walletname": "testing"
}'
```

- Get new Wallet Address

```
curl --location --request POST 'http://0.0.0.0/new_address/' --header 'Authorization: <api_key>' --header 'Content-Type: application/json' --data-raw '{
  "walletname": "testing"
}'
```

- Send BTC to Another Wallet

```
curl --location --request POST 'http://0.0.0.0/send/' --header 'Authorization: <api_key>' --header 'Content-Type: application/json' --data-raw '{
  "address": "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB",
  "amount": 0.16,
  "walletname": "testing"
}'
```

- Check the Wallets Transactions

```
curl --location --request POST 'http://0.0.0.0/tx/' --header 'Authorization: <api_key>' --header 'Content-Type: application/json' --data-raw '{
  "walletname": "testing"
}'
```

## Troubleshooting

To check logs 

`docker logs <container_name>`

Please allow time for bitcoin node to sync with blockchain.

Perform a docker system prune to switch networks. 

## Helpful Docs 

Bitcoin core config - https://jlopp.github.io/bitcoin-core-config-generator

Bitcoin RPC Documentation - https://bitcoincore.org/en/doc/22.0.0/

Running bitcoin node - https://bitcoin.org/en/full-node
