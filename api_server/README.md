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



## Доступ к данным всех организаций (DbInfoApi)
Эта группа методов позволяет получить информацию о всех организациях хранящихся в базе данных

### Коды ошибок
В случае ошибки сервер возвращает код 400, а также следующий код ошибки в виде json:

#### Возникла ошибка при получении информации о всех организациях
    {
        "error_code": 101,
        "message": "Select organizations failed"
    }
#### Возникла ошибка во время удаления всех организаций
    {
        "errorCode": 102,
        "errorMessage": "Delete organizations failed"
    }

### Получение списка организаций
Метод для получения списка организаций в виде json массива. В примере возвращается список состоящий из организаций `org1`, `org2` и `org3`. 

#### Request

`GET /api/v1/`

    curl -X GET -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 18:14:08 GMT
    Content-Type: application/json
    Content-Length: 134
    Connection: keep-alive

    ["org1","org2", "org3"]

### Удаление всех организаций
Метод полностью удаляет все организации из базы данных, а также их расписание занятий и экзаменов.

#### Request

`DELETE /api/v1/`

    curl -X DELETE -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 18:15:12 GMT
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive

    {}



## Доступ к данным организации (OrganizationApi)
Эта группа методов позволяет получить информацию о выбранной организации

### Коды ошибок
В случае ошибки сервер возвращает код 400, а также следующий код ошибки в виде json:

#### Возникла ошибка при получении информации об организации
    {
        "error_code": 201,
        "message": "Select organization failed"
    }
#### Возникла ошибка во время удаления организации
    {
        "errorCode": 202,
        "errorMessage": "Delete organization failed"
    }

### Получение списка факультетов выбранной организации
Метод для получения списка факультетов выбранной организации `organization` в виде json массива. В примере возвращается список состоящий из факультетов `faculty1`, `faculty2` и `faculty3`. 

#### Request

`GET /api/v1/organization`

    curl -X GET -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 18:48:08 GMT
    Content-Type: application/json
    Content-Length: 35
    Connection: keep-alive

    ["faculty1","faculty2","faculty3"]

### Удаление выбранной организаций
Метод удаляет выбранную организацию `organization`, а также её расписание занятий и экзаменов.

#### Request

`DELETE /api/v1/organization`

    curl -X DELETE -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 18:50:32 GMT
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive

    {}



## Доступ к данным факультетов (FacultyApi)
Эта группа методов позволяет получить информацию о факультетах выбранной организации

### Коды ошибок
В случае ошибки сервер возвращает код 400, а также следующий код ошибки в виде json:

#### Возникла ошибка при получении информации о факультете
    {
        "error_code": 301,
        "message": "Select faculty failed"
    }
#### Возникла ошибка во время удаления факультета
    {
        "errorCode": 302,
        "errorMessage": "Delete faculty failed"
    }

### Получение списка групп выбранного факультета
Метод для получения списка групп выбранной факультета `faculty`, принадлежащего организации `organization` в виде json массива. В примере возвращается список состоящий из групп `group1`, `group2` и `group3`. 

#### Request

`GET /api/v1/organization/faculty`

    curl -X GET -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 19:14:50 GMT
    Content-Type: application/json
    Content-Length: 29
    Connection: keep-alive

    ["group1","group2","group3"]

### Удаление выбранного факультета
Метод удаляет выбранный факультет `faculty` организации `organization`, а также его расписание занятий и экзаменов.

#### Request

`DELETE /api/v1/organization/faculty`

    curl -X DELETE -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 19:16:18 GMT
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive

    {}



## Доступ к данным групп (GroupApi)
Эта группа методов позволяет получить информацию о выбранной группе

### Коды ошибок
В случае ошибки сервер возвращает код 400, а также следующий код ошибки в виде json:

#### Возникла ошибка при получении информации о группе
    {
        "error_code": 401,
        "message": "Select group failed"
    }
#### Возникла ошибка во время удаления группы
    {
        "errorCode": 402,
        "errorMessage": "Delete group failed"
    }
#### Возникла ошибка во время добавления группы (такая группа уже существует)
    {
        "error_code": 403,
        "message": "Group already created"
    }
#### Возникла ошибка во время добавления группы (неизвестная ошибка)
    {
        "error_code": 404,
        "message": "Create group failed"
    }
#### Возникла ошибка во время обновления группы (в запросе отсутствуют json данные)
    {
        "error_code": 405,
        "message": "Missing json in request"
    }
#### Возникла ошибка во время обновления группы (в запросе отсутствуют данные новой названия организации группы)
    {
        "error_code": 406,
        "message": "Missing new_organization parameter"
    }
#### Возникла ошибка во время обновления группы (в запросе отсутствуют данные нового названия факультета группы)
    {
        "error_code": 407,
        "message": "Missing new_faculty parameter"
    }
#### Возникла ошибка во время обновления группы (в запросе отсутствуют данные нового названия группы)
    {
        "error_code": 408,
        "message": "Missing new_group parameter"
    }
#### Возникла ошибка во время обновления группы (неизвестная ошибка)
    {
        "error_code": 409,
        "message": "Change group failed"
    }

### Получение тега выбранной группы
Метод для получения тега группы `group` (принадлежащей факультету `faculty` организации `organization`). В примере возвращается тег группы имеющий значение `group_tag`.

#### Request

`GET /api/v1/organization/faculty/group`

    curl -X GET -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 19:42:53 GMT
    Content-Type: application/json
    Content-Length: 33
    Connection: keep-alive

    "group_tag"

### Добавление новой группы
Метод позволяет добавить группу `group` принадлежащую факультету `faculty` организации `organization` в базу данных. Метод возвращает тег добавленной группы `group_tag` в случае успешного выполнения запроса.

#### Request

`POST /api/v1/organization/faculty/group`

    curl -X POST -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 19:47:18 GMT
    Content-Type: application/json
    Content-Length: 33
    Connection: keep-alive

    "group_tag"

### Изменение данных выбранной группы
Метод позволяет изменить данные группы `group` принадлежащей факультету `faculty` организации `organization`. Он изменяет название группы на `upd_group`, а также изменяет факультет и организацию, которой принадлежит группа, на `upd_faculty` и `upd_organization` соответственно. Метод возвращает обновлённый тег группы `upd_group_tag` в случае успешного выполнения запроса.

#### Request

`PUT /api/v1/organization/faculty/group`

    curl -X PUT -i -H 'Authorization: Bearer api_token' -H 'Content-Type: application/json' -d '{"new_group":"upd_group", "new_faculty":"upd_faculty", "new_organization":"upd_organization"}' http://api_address:api_port/api/v1/organization/faculty/group

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 19:54:29 GMT
    Content-Type: application/json
    Content-Length: 33
    Connection: keep-alive

    "upd_group_tag"

### Удаление выбранной группы
Метод удаляет выбранную группу `group` (принадлежащую факультету `faculty` организации `organization`), а также её расписание занятий и экзаменов.

#### Request

`DELETE /api/v1/organization/faculty/group`

    curl -X DELETE -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 19:59:59 GMT
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive

    {}
