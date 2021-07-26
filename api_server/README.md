# VkScheduleBot API Server
Сервер предоставляющий интерфейс для взимодействия с БД расписания. Модуль для [VkScheduleBot](../vk_bot).

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_api)

Docker Hub: [paladin705/vk_schedule_bot_api](https://hub.docker.com/r/paladin705/vk_schedule_bot_api)

Программа для взаимодействия с сервером: [api_client](../api_client)

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
Сервер реализует REST API для взаимодействия с базой данных бота. С API можно взаимодействовать не только с помощью программы [api_client](../api_client), но и с помощью http-запросов.

Для примеров запросов в качестве IP адреса и порта сервера API используются значения `api_address` и `api_port`.

## Авторизация и получение токена
Для того, чтобы пользоваться функциями API, необходимо пройти авторизацию и получить `api_token` и `api_refresh_token`. `api_token` в дальнейшем будет использоваться при отправке запросов к API, при этом, он устаревает через 15 минут использования. Для обновления `api_token`, может использоваться `api_refresh_token`.

### Коды ошибок
В случае ошибки сервер возвращает код 400 или 401, а также следующий код ошибки в виде json:

#### В запросе отсутствуют json данные
    {
        "error_code": 701,
        "message": "Missing json in request"
    }
#### В json данных запроса отсутствует имя пользователя
    {
        "error_code": 702,
        "message": "Missing username parameter"
    }
#### В json данных запроса отсутствует пароль пользователя
    {
        "error_code": 703,
        "errorMessage": "Missing password parameter"
    }
#### Ошибка авторизации (неверные данные пользователя)
    {
        "error_code": 704,
        "errorMessage": "Bad username or password"
    }
#### Неизвестная ошибка
    {
        "error_code": 705,
        "errorMessage": "Unknown error"
    }

### Авторизация
Для получения `api_token` и `api_refresh_token`, необходимо авторизоваться, путём ввода имени пользователя `api_user` и соответствующего ему пароля `api_password`.

#### Request

`POST /api/auth/login`

    curl -X POST -i -H 'Content-Type: application/json' -d '{"username":"api_user", "password":"api_password"}' http://api_address:api_port/api/auth/login

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 16:44:02 GMT
    Content-Type: application/json
    Content-Length: 587
    Connection: keep-alive

    {"access_token":"api_token","refresh_token":"api_refresh_token"}

### Обновление токена
Этот метод служит для обновления значения `api_token` (будет получен новый токен `new_api_token`).

#### Request

`POST /api/auth/refresh`

    curl -X POST -i -H 'Authorization: Bearer refresh_token'  http://api_address:api_port/api/auth/refresh

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 17:29:34 GMT
    Content-Type: application/json
    Content-Length: 293
    Connection: keep-alive

    {"access_token":"new_api_token"}

