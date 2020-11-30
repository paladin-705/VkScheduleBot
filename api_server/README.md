# VkScheduleBot API Server
Сервер предоставляющий интерфейс для взимодействия с БД расписания. Модуль для [VkScheduleBot](../vk_bot).

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_api)

Docker Hub: [paladin705/vk_schedule_bot_api](https://hub.docker.com/r/paladin705/vk_schedule_bot_api)

## Зависимости
Модуль использует СУБД PostgreSQL для хранения данных. Адрес: `http://<адрес сервера>/api/`.

Сервер реализованный в docker контейнере не имеет прямого доступа к сети и использует сокет `/api/socket/api.sock` для обработки запросов. Чтобы передать поступающие запросы серверу, можно использовать nginx reverse proxy для передачи их на сокет сервера.

## Docker
Для запуска docker контейнера загружаемого с [Docker Hub](https://hub.docker.com/r/paladin705/vk_schedule_bot_api) можно использовать следующую команду:
```shell
docker run \
    -v ./vk_bot_api/socket:/api/socket \
    -v ./vk_bot_api/log:/api/log \
    -e DB_NAME=<Введите значение параметра> \
    -e DB_USER=Введите значение параметра<> \
    -e DB_PASSWORD=<Введите значение параметра> \
    -e DB_HOST=<Введите значение параметра> \
    -e TZ=<Введите значение параметра> \
    paladin705/vk_schedule_bot_api:latest
```

### Файлы
* `/api/socket` - В данной директории находится сокет сервера: `api.sock`. Он используется для обработки запросов к серверу
* `/api/log` - Директория где располагаются логи сервера

### Переменные среды

* `DB_NAME` - Название базы данных (БД) PostgreSQL
* `DB_USER` - Имя пользователя БД
* `DB_PASSWORD` - Пароль пользователя БД
* `DB_HOST` - Адрес БД
* `TZ` - Часовой пояс. По умолчанию `Europe/Moscow`

## Работа с API


