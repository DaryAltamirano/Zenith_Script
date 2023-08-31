FROM darypte/python3.9-slim-buster-mysql:latest

WORKDIR /code

ADD  . /code/

RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get clean

CMD [ "python", "/code/main.py" ]