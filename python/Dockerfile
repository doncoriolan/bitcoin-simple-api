FROM ubuntu
ARG rpcuser

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN useradd $rpcuser
RUN apt-get update -y && apt -y install locales && locale-gen en_US.UTF-8
RUN apt-get install python3 python3-pip curl -y
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN pip3 install -r requirements.txt
RUN chown -R $rpcuser:$rpcuser /usr/src/app
RUN ln -sf /proc/1/fd/1 /usr/src/app/api.log
EXPOSE 8084
USER $rpcuser
CMD [ "/usr/local/bin/uwsgi", "/usr/src/app/uwsgi.ini"]