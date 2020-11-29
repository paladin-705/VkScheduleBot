FROM python:3.6-alpine

LABEL maintainer="Sergey Kornev <paladin705@yandex.ru>"

ARG TZ

COPY ./requirements.txt /bot/requirements.txt
COPY supervisord.conf /etc/
COPY ./app /bot/app

RUN apk update \
    && apk upgrade \
    && apk add tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apk del tzdata \
    && apk add git build-base postgresql-dev supervisor \
    && pip3 install gunicorn \
    && pip3 install -r /bot/requirements.txt

WORKDIR /bot

CMD ["/usr/bin/supervisord"]
