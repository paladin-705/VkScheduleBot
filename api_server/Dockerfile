FROM python:3.6

LABEL maintainer="Sergey Kornev <paladin705@yandex.ru>"

RUN apt-get update
RUN apt-get install -y --no-install-recommends supervisor

RUN pip3 install gunicorn

COPY ./requirements.txt /api/requirements.txt

RUN pip3 install -r /api/requirements.txt

COPY supervisord.conf /etc/

COPY ./app /api/app

WORKDIR /api

CMD ["/usr/bin/supervisord"]
