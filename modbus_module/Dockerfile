FROM python:3.9-slim-buster

ARG UUID_SENDOR=none

WORKDIR /code

ADD  . /code/
RUN apt-get update && apt-get install -y build-essential default-mysql-client default-libmysqlclient-dev autoconf

RUN pip install -r requirements.txt  
CMD [ "python", "/code/manteiner.py" ]