FROM python:3.9-slim-buster

WORKDIR /code

ADD  . /code/
RUN apt-get update && apt-get install -y build-essential default-mysql-client default-libmysqlclient-dev

RUN pip install -r requirements.txt  
CMD [ "python", "/code/main.py" ]