FROM ubuntu

# https://github.com/bitcoin/bitcoin/tree/master/share/rpcauth
ARG rpcuser
ARG rpcauth
ARG rpc_creds
ARG rpcallowip
ARG rpcport
ARG rpcbind
ARG network

RUN apt-get update -y
RUN apt-get install wget curl bash python3 python3-pip -y
RUN useradd $rpcuser
RUN wget https://bitcoin.org/bin/bitcoin-core-22.0/bitcoin-22.0-x86_64-linux-gnu.tar.gz -P /home/
RUN cd /home && tar -xzf bitcoin-22.0-x86_64-linux-gnu.tar.gz
RUN install -m 0755 -o $rpcuser -g $rpcuser -t /usr/local/bin /home/bitcoin-22.0/bin/*
RUN mkdir -p /home/$rpcuser/.bitcoin
RUN chown -R $rpcuser:$rpcuser /home/$rpcuser/.bitcoin
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
USER $rpcuser
CMD ["/entrypoint.sh"]

#CMD bitcoind -testnet -prune=9536 -rpcauth=$rpcauth -rpcallowip=$rpcallowip -rpcport=$rpcport -rpcbind=$rpcbind -server -printtoconsole=1