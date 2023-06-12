#!/bin/bash

if [ "$network" = "testnet" ]; then
    echo "Running Bitcoind on the Test Network"
    bitcoind -testnet -prune=9536 -rpcauth=$rpcauth -rpcallowip=$rpcallowip -rpcport=$rpcport -rpcbind=$rpcbind -server -printtoconsole=1
elif [ "$network" = "mainnet" ]; then
    echo "Running Bitcoind on the Main Network"
    bitcoind -prune=9536 -rpcauth=$rpcauth -rpcallowip=$rpcallowip -rpcport=$rpcport -rpcbind=$rpcbind -server -printtoconsole=1
else
    echo "Wrong Option Please choose mainnet or testnet!! example network=testnet"
    env
fi