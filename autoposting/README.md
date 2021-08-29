# VkScheduleBot autoposting script
Модуль выполняющий автоматическую рассылку расписания для [VkScheduleBot](../vk_bot).

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_autoposting)

Docker Hub: [paladin705/vk_schedule_bot_autoposting](https://hub.docker.com/r/paladin705/vk_schedule_bot_autoposting)

## Зависимости
Модуль использует VK Callback API для отправки расписания и СУБД PostgreSQL для хранения данных.


## Docker
Для запуска docker контейнера загружаемого с [Docker Hub](https://hub.docker.com/r/paladin705/vk_schedule_bot_autoposting) можно использовать следующую команду:
```shell
docker run \
    -v ./autoposting/log:/app/log \
    -e DB_NAME=<Введите значение параметра> \
    -e DB_USER=Введите значение параметра<> \
    -e DB_PASSWORD=<Введите значение параметра> \
    -e DB_HOST=<Введите значение параметра> \
    -e DB_USER_TAG=<Введите значение параметра> \
    -e VK_API_TOKEN=<Введите значение параметра> \
    -e STATISTIC_TOKEN=<Введите значение параметра> \
    -e WEEK_TYPE=<Введите значение параметра> \
    -e ADMIN_VK_ID=<Введите значение параметра> \
    -e VK_ID_BLACKLIST=<Введите значение параметра> \
    -e TZ=<Введите значение параметра> \
    paladin705/vk_schedule_bot_autoposting:latest
```

### Файлы
* `/app/log` - Директория где располагаются логи модуля

### Переменные среды

* `DB_NAME` - Название базы данных (БД) PostgreSQL
* `DB_USER` - Имя пользователя БД
* `DB_PASSWORD` - Пароль пользователя БД
* `DB_HOST` - Адрес БД
* `DB_USER_TAG` - Идентификатор пользователей бота (используется для разделения пользователей, при общей базе данных для нескольких ботов
* `VK_API_TOKEN` - Ключ доступа к сообщениям сообщества. Параметр VK API
* `STATISTIC_TOKEN` - Токен для отправки статистики на [chatbase.com](https://chatbase.com/). Необязательный параметр (На данный момент не используется - Chatbase прекращает работу 27 сентября 2021 года)
* `WEEK_TYPE` - Тип первой недели семестра 0 - числитель, 1 - знаменатель
* `ADMIN_VK_ID` - VK ID страницы администратора (только номер) для отправки информации о состоянии сервера
* `VK_ID_BLACKLIST` - Чёрный список VK ID через запятую (Пример: 1,2,3,4,5). Бот не будет отвечать на сообщения из этого списка. Необязательный параметр
* `TZ` - Часовой пояс. Необязательный параметр. По умолчанию `Europe/Moscow`
