FROM python:3.6-alpine

LABEL maintainer="Sergey Kornev <paladin705@yandex.ru>"

COPY ./requirements.txt /app/requirements.txt
COPY supervisord.conf /etc/
COPY ./app /app

RUN apk update \
    && apk upgrade \
    && apk add git build-base postgresql-dev supervisor \
    && pip3 install -r /app/requirements.txt

WORKDIR /app

CMD ["/usr/bin/supervisord"]
