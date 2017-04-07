FROM python:latest

MAINTAINER <mohamed@farghal.com>

ENV PORT=5555

RUN pip3 install numpy dill

RUN git clone https://github.com/medo/Cluster-Pandas.git

WORKDIR Cluster-Pandas

EXPOSE 5555

CMD echo "5od"
CMD echo $role

CMD python3 start_master.py
