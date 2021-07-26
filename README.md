# VkScheduleBot
Бот для ВК показывающий расписание занятий. Вы можете протестировать его работу, перейдя по ссылке: [VkScheduleBot](https://vk.com/club199143657)

Проект разделён на модули. Такая структура, позволяет устанавливать лишь необходимые разработчику части проекта. Ниже представлен список основных модулей бота:
* Модуль ВК бота: [VkScheduleBot](../vk_bot) - Бот для ВК показывающий расписание занятий. Основной модуль проекта, осуществляющий обработку пользовательских запросов и формирование ответов на них.  
* Модуль для автоматической отправки расписания: [autoposting](../autoposting)
* Модуль для работы с базой данных бота (добавление/изменение/удаление групп и файлов расписания): [api_server](../api_server)
* Программа для взаимодействия с сервером API бота (добавление/изменение/удаление групп и файлов расписания): [api_client](../api_client)

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
