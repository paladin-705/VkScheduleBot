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

### Содержание
- [Создание пользователя API](#создание-пользователя-api)
- [Авторизация и получение токена](#авторизация-и-получение-токена)
  * [Коды ошибок](#коды-ошибок)
  * [Авторизация](#авторизация)
  * [Обновление токена](#обновление-токена)
- [Доступ к данным всех организаций (DbInfoApi)](#доступ-к-данным-всех-организаций-dbinfoapi)
  * [Коды ошибок](#коды-ошибок-1)
  * [Получение списка организаций](#получение-списка-организаций)
  * [Удаление всех организаций](#удаление-всех-организаций)
- [Доступ к данным организации (OrganizationApi)](#доступ-к-данным-организации-organizationapi)
  * [Коды ошибок](#коды-ошибок-2)
  * [Получение списка факультетов выбранной организации](#получение-списка-факультетов-выбранной-организации)
  * [Удаление выбранной организаций](#удаление-выбранной-организаций)
- [Доступ к данным факультетов (FacultyApi)](#доступ-к-данным-факультетов-facultyapi)
  * [Коды ошибок](#коды-ошибок-3)
  * [Получение списка групп выбранного факультета](#получение-списка-групп-выбранного-факультета)
  * [Удаление выбранного факультета](#удаление-выбранного-факультета)
- [Доступ к данным групп (GroupApi)](#доступ-к-данным-групп-groupapi)
  * [Коды ошибок](#коды-ошибок-4)
  * [Получение тега выбранной группы](#получение-тега-выбранной-группы)
  * [Добавление новой группы](#добавление-новой-группы)
  * [Изменение данных выбранной группы](#изменение-данных-выбранной-группы)
  * [Удаление выбранной группы](#удаление-выбранной-группы)
- [Доступ к данным расписания занятий выбранной группы (ScheduleApi)](#доступ-к-данным-расписания-занятий-выбранной-группы-scheduleapi)
  * [Коды ошибок](#коды-ошибок-5)
  * [Получение расписания занятий выбранной группы](#получение-расписания-занятий-выбранной-группы)
  * [Добавление расписания занятий выбранной группы](#добавление-расписания-занятий-выбранной-группы)
  * [Удаление расписания занятий выбранной группы](#удаление-расписания-занятий-выбранной-группы)
- [Доступ к данным расписания экзаменов выбранной группы (ExamsApi)](#доступ-к-данным-расписания-экзаменов-выбранной-группы-examsapi)
  * [Коды ошибок](#коды-ошибок-6)
  * [Получение расписания экзаменов выбранной группы](#получение-расписания-экзаменов-выбранной-группы)
  * [Добавление расписания экзаменов выбранной группы](#добавление-расписания-экзаменов-выбранной-группы)
  * [Удаление расписания экзаменов выбранной группы](#удаление-расписания-экзаменов-выбранной-группы)

## Создание пользователя API
Для работы с API вам будет необходимо добавить в таблицу `api_users` базы данных, имя нового пользователя пользователя API и хеш пароля. Методов API для регистрации пользователей не предусмотрено. Вам необходимо создать имя пользователя и пароль, а затем сгенерировать bcrypt хеш пароля. Затем вам необходимо сохранить выбранное имя пользователя API и сгенерированный хеш пароля в таблицу `api_users` базы данных.

Следующий пример показывает простой Python скрипт для создания нового пользователя API. Для его работы понадобятся библиотеки `bcrypt` и `psycopg2`:
```shell
pip install bcrypt psycopg2
```

После установки библиотек bcrypt и psycopg2, необходимо создать и запустить следующий скрипт для Python 3:
```python
import bcrypt
import psycopg2

# Данные нового пользователя API
api_username = 'Имя пользователя API'
api_password = 'Пароль пользователя API'

# Параметры подключения базы данных
db_name = 'Название базы данных (БД) PostgreSQL'
db_user = 'Имя пользователя БД'
db_password = 'Пароль пользователя БД'
db_host = 'Адрес сервера БД'
db_port = Порт сервера БД (число)

# Создание хеша пароля
pw_hash = bcrypt.hashpw(api_password.encode('utf-8'), bcrypt.gensalt())

# Загрузка нового пользователя APi в базу данных
con = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port)

cur = con.cursor()
cur.execute('INSERT INTO api_users(username, pw_hash) VALUES(%s,%s);', (api_username, pw_hash.decode('utf-8')))
con.commit()
```
Вам необходимо записать в переменные `api_username` и `api_password` желаемое имя пользователя API и его пароль соответственно. Переменные `db_name`, `db_user`, `db_password`, `db_host` и `db_port` используются для установки соединения с сервером PostgreSQL базы данных. Вы должны использовать для их заполнения теже значения, что и для сервера API (если скрипт запускается не с компьютера, на котором запущен сервер API, то значение `db_host` и `db_port` может отличаться).

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
#### Срок действия токена истек
    {
        "msg":"Token has expired"
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



## Доступ к данным расписания занятий выбранной группы (ScheduleApi)
Эта группа методов позволяет получить информацию о расписании занятий выбранной группы

### Коды ошибок
В случае ошибки сервер возвращает код 400, а также следующий код ошибки в виде json:

#### Возникла ошибка при получении информации о расписании занятий выбранной группы
    {
        "error_code": 501,
        "message": "Select schedule failed"
    }
#### Возникла ошибка во время удаления расписания занятий выбранной группы
    {
        "errorCode": 502,
        "errorMessage": "Delete schedule failed"
    }
#### Возникла ошибка во время добавления расписания занятий выбранной группы (неизвестная ошибка)
    {
        "error_code": 503,
        "message": "Create schedule failed"
    }
#### Возникла ошибка во время удаления расписания занятий выбранной группы (в запросе отсутствуют json данные расписания)
    {
        "error_code": 504,
        "message": "Empty data"
    }
#### Неизвестная группа (такой группы не существует) 
    {
        "error_code": 505,
        "message": "Unknown group"
    }

### Получение расписания занятий выбранной группы
Метод для получения расписания занятий группы `group` (принадлежащей факультету `faculty` организации `organization`). В примере возвращается json массив с тремя значениями (тремя занятиями).

Каждый элемент json массива имеет следующую структуру:
```json
{
    "day": "День недели (английское название)",
    "number": Номер занятия (число),
    "week_type": "Допустимы лишь следующие значения: odd -  занятие проводится по нечётным неделям, even - по чётным неделям, all - каждую неделю",
    "title": "Название занятия",
    "classroom": "Аудитория в которой проводится занятие. Необязательный параметр",
    "lecturer": "Преподаватель ведущий занятие. Необязательный параметр",
    "time_start": "Время начала занятия (Формат: ЧЧ:ММ). Необязательный параметр",
    "time_end": "Время окончания занятия (Формат: ЧЧ:ММ). Необязательный параметр"
}
```

#### Request

`GET /api/v1/organization/faculty/group/schedule`

    curl -X GET -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group/schedule

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 20:58:01 GMT
    Content-Type: application/json
    Content-Length: 468
    Connection: keep-alive

    [{"classroom":"classroom 1","day":"Monday","endTime":"10:05:00","lecturer":"lecturer 1","number":1,"startTime":"08:30:00","title":"Test title 1","type":0},{"classroom":"classroom 2","day":"Tuesday","endTime":"11:55:00","lecturer":"lecturer 2","number":2,"startTime":"10:20:00","title":"Test title 2","type":1},{"classroom":"classroom 3","day":"Wednesday","endTime":"13:45:00","lecturer":"lecturer 3","number":3,"startTime":"12:10:00","title":"Test title 3","type":2}]

### Добавление расписания занятий выбранной группы
Метод позволяет добавить расписание занятий для выбранной группы `group` (принадлежащей факультету `faculty` организации `organization`). Добавляемое расписание должно быть представлено в виде json массива, формат которого рассматривается ниже. 

В качестве примера запроса, для группы `group` (принадлежащей факультету `faculty` организации `organization`), будут добавлены следующие занятия в виде массива `data`:
```json
{
  "data": [
    {
      "day": "Понедельник",
      "number": 1,
      "week_type": "odd",
      "title": "Test title 1",
      "classroom": "classroom 1",
      "lecturer": "lecturer 1",
      "time_start": "08:30",
      "time_end": "10:05"
    },
    {
      "day": "Tuesday",
      "number": 2,
      "week_type": "even",
      "title": "Test title 2",
      "classroom": "classroom 2",
      "lecturer": "lecturer 2",
      "time_start": "10:20",
      "time_end": "11:55"
    },
    {
      "day": "Wednesday",
      "number": 3,
      "week_type": "all",
      "title": "Test title 3",
      "classroom": "classroom 3",
      "lecturer": "lecturer 3",
      "time_start": "12:10",
      "time_end": "13:45"
    }
  ]
}
```
Поле `week_type` может принимать только значения `odd`, `even` или `all`. Они соответствуют парам, которые проходят лишь по нечётным (`odd`) и чётным (`even`) неделям, а также парам, которые проходят каждую неделю (`all`).

Поля `classroom`, `time_start`, `time_end` и `lecturer`, являются необязательными.

Метод возвращает массив из занятий, которые не удалось добавить (массив `failed`), если все занятия были добавлены, то массив `failed` будет пуст.

#### Request

`POST /api/v1/organization/faculty/group/schedule`

    curl -X POST -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group/schedule -H 'Content-Type: application/json' -d '{"data": [{"day": "Monday","number": 1,"week_type": "odd","title": "Test title 1","classroom": "classroom 1","lecturer": "lecturer 1","time_start": "08:30","time_end": "10:05"}, {"day": "Tuesday","number": 2,"week_type": "even","title": "Test title 2","classroom": "classroom 2","lecturer": "lecturer 2","time_start": "10:20","time_end": "11:55"},{"day": "Wednesday","number": 3,"week_type": "all","title": "Test title 3","classroom": "classroom 3","lecturer": "lecturer 3","time_start": "12:10","time_end": "13:45"}]}'

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 21:03:49 GMT
    Content-Type: application/json
    Content-Length: 14
    Connection: keep-alive

    {"failed":[]}

### Удаление расписания занятий выбранной группы
Метод производит удаление всего расписания занятий для выбранной группы `group` (принадлежащей факультету `faculty` организации `organization`).

#### Request

`DELETE /api/v1/organization/faculty/group/schedule`

    curl -X DELETE -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group/schedule

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 21:15:29 GMT
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive

    {}



## Доступ к данным расписания экзаменов выбранной группы (ExamsApi)
Эта группа методов позволяет получить информацию о расписании экзаменов выбранной группы

### Коды ошибок
В случае ошибки сервер возвращает код 400, а также следующий код ошибки в виде json:

#### Возникла ошибка при получении информации о расписании экзаменов выбранной группы
    {
        "error_code": 601,
        "message": "Select exams failed"
    }
#### Возникла ошибка во время удаления расписания экзаменов выбранной группы
    {
        "errorCode": 602,
        "errorMessage": "Delete exams failed"
    }
#### Возникла ошибка во время добавления расписания экзаменов выбранной группы (неизвестная ошибка)
    {
        "error_code": 603,
        "message": "Create exams failed"
    }
#### Возникла ошибка во время удаления расписания экзаменов выбранной группы (в запросе отсутствуют json данные расписания)
    {
        "error_code": 604,
        "message": "Empty data"
    }
#### Неизвестная группа (такой группы не существует) 
    {
        "error_code": 605,
        "message": "Unknown group"
    }

### Получение расписания экзаменов выбранной группы
Метод для получения расписания экзаменов группы `group` (принадлежащей факультету `faculty` организации `organization`). В примере возвращается json массив с тремя значениями (тремя экзаменами).

Каждый элемент json массива имеет следующую структуру:
```json
{
    "day": "День проведения экзамена (Формат: ДД.ММ.ГГГГ)",
    "title": "Название экзамена",
    "classroom": "Аудитория в которой проводится экзамен. Необязательный параметр",
    "lecturer": "Преподаватель принимающий экзамен. Необязательный параметр"
}
```

#### Request

`GET /api/v1/organization/faculty/group/exams`

    curl -X GET -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group/exams

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 21:44:09 GMT
    Content-Type: application/json
    Content-Length: 371
    Connection: keep-alive

    [{"classroom":"Test classroom 1","day":"Mon, 25 Jan 2021 00:00:00 GMT","lecturer":"Test lecturer 1","title":"Test title 1"},{"classroom":"Test classroom 2","day":"Tue, 26 Jan 2021 00:00:00 GMT","lecturer":"Test lecturer 2","title":"Test title 2"},{"classroom":"Test classroom 3","day":"Wed, 27 Jan 2021 00:00:00 GMT","lecturer":"Test lecturer 3","title":"Test title 3"}]

### Добавление расписания экзаменов выбранной группы
Метод позволяет добавить расписание экзаменов для выбранной группы `group` (принадлежащей факультету `faculty` организации `organization`). Добавляемое расписание должно быть представлено в виде json массива, формат которого рассматривается ниже. 

В качестве примера запроса, для группы `group` (принадлежащей факультету `faculty` организации `organization`), будут добавлены следующие экзамены в виде массива `data`:
```json
{
  "data": [
    {
      "day": "25.01.2021",
      "title": "Test title 1",
      "classroom": "Test classroom 1",
      "lecturer": "Test lecturer 1"
    },
    {
      "day": "26.01.2021",
      "title": "Test title 2",
      "classroom": "Test classroom 2",
      "lecturer": "Test lecturer 2"
    },
    {
      "day": "27.01.2021",
      "title": "Test title 3",
      "classroom": "Test classroom 3",
      "lecturer": "Test lecturer 3"
    }
  ]
}
```
Поля `classroom` и `lecturer`, являются необязательными.

Метод возвращает массив из экзаменов, которые не удалось добавить (массив `failed`), если все экзамены были добавлены, то массив `failed` будет пуст.

#### Request

`POST /api/v1/organization/faculty/group/exams`

    curl -X POST -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group/exams -H 'Content-Type: application/json' -d '{"data": [{"day": "25.01.2021","title": "Test title 1","classroom": "Test classroom 1","lecturer": "Test lecturer 1"}, {"day": "26.01.2021","title": "Test title 2","classroom": "Test classroom 2","lecturer": "Test lecturer 2"}, {"day": "27.01.2021","title": "Test title 3","classroom": "Test classroom 3","lecturer": "Test lecturer 3"}]}'

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 21:46:15 GMT
    Content-Type: application/json
    Content-Length: 14
    Connection: keep-alive

    {"failed":[]}

### Удаление расписания экзаменов выбранной группы
Метод производит удаление всего расписания экзаменов для выбранной группы `group` (принадлежащей факультету `faculty` организации `organization`).

#### Request

`DELETE /api/v1/organization/faculty/group/exams`

    curl -X DELETE -i -H 'Authorization: Bearer api_token' http://api_address:api_port/api/v1/organization/faculty/group/exams

#### Response

    HTTP/1.1 200 OK
    Server: nginx/1.14.2
    Date: Mon, 26 Jul 2021 21:48:00 GMT
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive

    {}
