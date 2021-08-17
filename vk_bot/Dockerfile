FROM python:3.6-alpine

LABEL maintainer="Sergey Kornev <paladin705@yandex.ru>"

ENV TZ="Europe/Moscow"

ENV DB_NAME=
ENV DB_USER=
ENV DB_PASSWORD=
ENV DB_HOST=

ENV VK_CONFIRMATION_TOKEN=
ENV VK_API_TOKEN=
ENV STATISTIC_TOKEN=""

ENV WEEK_TYPE=

ENV ADMIN_VK_ID=

ENV DB_USER_TAG=

ENV FLASK_ROUTE_PATH=

ENV VK_ID_BLACKLIST=""

WORKDIR /bot

RUN apk update \
    && apk upgrade \
    && apk add tzdata \
    && apk add git build-base postgresql-dev

COPY deploy requirements.txt ./

RUN pip3 install gunicorn \
    && pip3 install -r requirements.txt \
    && chmod +x deploy

COPY app ./app

CMD ./deploy ${DB_NAME} ${DB_USER} ${DB_PASSWORD} ${DB_HOST} \
             ${VK_CONFIRMATION_TOKEN} ${VK_API_TOKEN} \
             ${WEEK_TYPE} ${STATISTIC_TOKEN} ${ADMIN_VK_ID} \
             ${DB_USER_TAG} ${FLASK_ROUTE_PATH} ${VK_ID_BLACKLIST} ${TZ}