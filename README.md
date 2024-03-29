# VkScheduleBot
Бот для ВК показывающий расписание занятий. Вы можете протестировать его работу, перейдя по ссылке: [VkScheduleBot](https://vk.com/club199143657)

Проект разделён на модули. Такая структура, позволяет устанавливать лишь необходимые разработчику части проекта. Ниже представлен список основных модулей бота:
* Модуль ВК бота: [VkScheduleBot](./vk_bot) - Бот для ВК показывающий расписание занятий. Основной модуль проекта, осуществляющий обработку пользовательских запросов и формирование ответов на них.  
* Модуль для автоматической отправки расписания: [autoposting](./autoposting)
* Модуль для работы с базой данных бота (просмотр/добавление/изменение/удаление групп и файлов расписания): [api_server](./api_server)
* Программа для взаимодействия с сервером API бота (просмотр/добавление/изменение/удаление групп и файлов расписания): [api_client](./api_client)
* Панель управления базой данных бота: [VkScheduleBot Control Panel](https://github.com/paladin-705/VkScheduleBotDB_ControlPanel). Предоставляет веб-интерфейс для взаимодействия с БД расписания, а также позволяет редактировать пользователей API бота (модуль [api_server](./api_server)). Панель управления является модулем для [VkScheduleBot](./vk_bot) и [UniversityScheduleBot](https://github.com/paladin-705/UniversityScheduleBot)

Также бот совместим с ботом для Telegram ([UniversityScheduleBot](https://github.com/paladin-705/UniversityScheduleBot)) - боты могут использовать одну базу данных для хранения расписания и информации о пользователях.

## Готовые Docker образы
Для всех модулей проекта уже собраны готовые Docker образы.

### Модуль ВК бота
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot)

Docker Hub: [paladin705/vk_schedule_bot](https://hub.docker.com/r/paladin705/vk_schedule_bot)

### Модуль для автоматической отправки расписания
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_autoposting)

Docker Hub: [paladin705/vk_schedule_bot_autoposting](https://hub.docker.com/r/paladin705/vk_schedule_bot_autoposting)

### Модуль для работы с базой данных бота
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_api)

Docker Hub: [paladin705/vk_schedule_bot_api](https://hub.docker.com/r/paladin705/vk_schedule_bot_api)

### Панель управления базой данных бота
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_db_control_panel)

Docker Hub: [paladin705/vk_schedule_bot_db_control_panel](https://hub.docker.com/r/paladin705/vk_schedule_bot_db_control_panel)

## Пример запуска бота с помощью Docker compose из готовых Docker образов
Пример рассчитан на использование Linux.

Для запуска бота из готовых Docker образов вам понадобятся файлы `deploy`, `docker-compose.yml`, `nginx.conf` и `db/schema.sql` расположенные в папке репозитория. Клонируйте репозиторий и перенесите эти файлы в новую папку (в примере используется папка `bot`):
```shell
git clone https://github.com/paladin-705/VkScheduleBot.git

mkdir bot
mkdir bot/db

cp VkScheduleBot/deploy bot/deploy
cp VkScheduleBot/docker-compose.yml bot/docker-compose.yml
cp VkScheduleBot/nginx.conf bot/nginx.conf
cp VkScheduleBot/db/schema.sql bot/db/schema.sql

rm -r VkScheduleBot
```
Перейдите в папку `bot` и сделайте файл  `deploy` исполняемым:
```shell
cd bot
chmod +x deploy
```
Запустите скрипт `deploy` для установки параметров бота и запуска Docker контейнеров:
```shell
./deploy <PG_DB> <PG_USER> <PG_PASSWORD> \
         <VK_CONFIRMATION_TOKEN> <VK_API_TOKEN> \ 
         <STATISTIC_TOKEN> <WEEK_TYPE> <ADMIN_VK_ID> \
         <DB_USER_TAG> <FLASK_ROUTE_PATH>
```
#### Параметры скрипта

* `PG_DB` - Название базы данных (БД) PostgreSQL
* `PG_USER` - Имя пользователя БД
* `PG_PASSWORD` - Пароль пользователя БД
* `VK_CONFIRMATION_TOKEN` - Токен для подтверждения адреса сервера. Параметр VK Callback API
* `VK_API_TOKEN` - Ключ доступа к сообщениям сообщества. Параметр VK API
* `STATISTIC_TOKEN` - Токен для отправки статистики на [chatbase.com](https://chatbase.com/). На данный момент не используется - Chatbase прекращает работу 27 сентября 2021 года. Можно задать любое значение, но для скрипта `deploy` данный параметр не должен быть пустым
* `WEEK_TYPE` - Тип первой недели семестра 0 - числитель, 1 - знаменатель
* `ADMIN_VK_ID` - VK ID страницы администратора (только номер) для отправки информации о состоянии сервера
* `DB_USER_TAG` - Идентификатор пользователей бота (используется для разделения пользователей, при общей базе данных для нескольких ботов
* `FLASK_ROUTE_PATH` - Опредлеляет адрес сервера бота для VK Callback API

В дальнейшем, если изменение настроек не требуется, можно запускать бота с помощью команды:
```shell
docker-compose up -d
```
