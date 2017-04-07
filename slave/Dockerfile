FROM python:latest

MAINTAINER <mohamed@farghal.com>

ENV CL_MASTER_HOST='127.0.0.1:5555'

RUN pip3 install numpy dill
RUN git clone https://github.com/medo/Cluster-Pandas.git

WORKDIR Cluster-Pandas

CMD python3 start_slave.py
