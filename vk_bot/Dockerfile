FROM python:3.6

LABEL maintainer="Sergey Kornev <paladin705@yandex.ru>"

RUN apt-get update
RUN apt-get install -y --no-install-recommends supervisor

RUN pip3 install gunicorn

COPY ./requirements.txt /bot/requirements.txt

RUN pip3 install -r /bot/requirements.txt

COPY supervisord.conf /etc/

COPY ./app /bot/app
COPY ./bot.py /bot/bot.py

WORKDIR /bot

CMD ["/usr/bin/supervisord"]
