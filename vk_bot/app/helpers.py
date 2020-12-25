import json
import datetime

from flask import current_app as app
from app.scheduledb import ScheduleDB
from app.messages import registration_message


daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

ScheduleType = {
    "понедельник": daysOfWeek[0],
    "вторник": daysOfWeek[1],
    "среда": daysOfWeek[2],
    "четверг": daysOfWeek[3],
    "пятница": daysOfWeek[4],
    "суббота": daysOfWeek[5],
    "воскресенье": daysOfWeek[6],
    "сегодня": "Today",
    "завтра": "Tomorrow",
    "неделя": daysOfWeek
}

daysOfWeek_rus = {
    daysOfWeek[0]: "Понедельник",
    daysOfWeek[1]: "Вторник",
    daysOfWeek[2]: "Среда",
    daysOfWeek[3]: "Четверг",
    daysOfWeek[4]: "Пятница",
    daysOfWeek[5]: "Суббота",
    daysOfWeek[6]: "Воскресенье",
}


def create_button_default(label, payload=None):
    if payload is None:
        return {
            "action": {
              "type": "text",
              "label": label
            },
            "color": "default"
          }
    else:
        return {
            "action": {
                "type": "text",
                "label": label,
                "payload": payload
            },
            "color": "default"
        }


def create_button_primary(label, payload=None):
    if payload is None:
        return {
            "action": {
              "type": "text",
              "label": label
            },
            "color": "primary"
          }
    else:
        return {
            "action": {
                "type": "text",
                "label": label,
                "payload": payload
            },
            "color": "primary"
        }


def create_button_positive(label, payload=None):
    if payload is None:
        return {
            "action": {
              "type": "text",
              "label": label
            },
            "color": "positive"
          }
    else:
        return {
            "action": {
                "type": "text",
                "label": label,
                "payload": payload
            },
            "color": "positive"
        }


def create_button_negative(label, payload=None):
    if payload is None:
        return {
            "action": {
              "type": "text",
              "label": label
            },
            "color": "negative"
          }
    else:
        return {
            "action": {
                "type": "text",
                "label": label,
                "payload": payload
            },
            "color": "negative"
        }


def get_keyboard():
    now = datetime.datetime.now()

    buttons = []

    today = create_button_primary('Сегодня')
    tomorrow = create_button_primary('Завтра')
    week = create_button_primary('Вся неделя')

    monday = create_button_default('Понедельник')
    tuesday = create_button_default('Вторник')
    wednesday = create_button_default('Среда')
    thursday = create_button_default('Четверг')
    friday = create_button_default('Пятница')
    sunday = create_button_default('Суббота')

    back = create_button_negative('Назад')

    if now.month == 1 or now.month == 12 or now.month == 5 or now.month == 6:
        exams = create_button_default('Экзамены')
        buttons.append([exams])

    buttons.append([today, tomorrow])
    buttons.append([monday, thursday])
    buttons.append([tuesday, friday])
    buttons.append([wednesday, sunday])
    buttons.append([back])

    return json.dumps(
        {
            "one_time": False,
            "buttons": buttons
        }
        , ensure_ascii=False)


def get_main_keyboard(is_registered):
    buttons = []

    if is_registered:
        button1_1 = create_button_positive('Личный кабинет', {'user_info': ''})
        button1_2 = create_button_positive('Расписание', {'schedule': ''})
    else:
        button1_1 = create_button_positive('Регистрация', {'registration': 'reg:stage 1:'})

    button2_1 = create_button_primary('Настройки')
    button2_2 = create_button_primary('Прочее')

    if is_registered:
        buttons.append([button1_1, button1_2])
    else:
        buttons.append([button1_1])
    buttons.append([button2_1, button2_2])

    return json.dumps(
        {
            "one_time": False,
            "buttons": buttons
        }
        , ensure_ascii=False)


def get_user_info_keyboard(is_registered):
    buttons = []

    if is_registered:
        button1_1 = create_button_positive('Изменить данные', {'registration': 'reg:stage 1:'})
    else:
        button1_1 = create_button_positive('Регистрация', {'registration': 'reg:stage 1:'})

    button1_2 = create_button_negative('Назад')

    buttons.append([button1_1, button1_2])

    return json.dumps(
        {
            "one_time": False,
            "buttons": buttons
        }
        , ensure_ascii=False)


def get_settings_keyboard(is_registered):
    buttons = []

    if is_registered:
        button1_1 = create_button_positive('Включить рассылку', {'auto_posting_on': ''})
        button1_2 = create_button_negative('Отключить рассылку')
    else:
        button1_1 = create_button_positive('Регистрация', {'registration': 'reg:stage 1:'})
    
    button2_1 = create_button_negative('Назад')
    
    if is_registered:
        buttons.append([button1_1, button1_2])
    else:
        buttons.append([button1_1])
    
    buttons.append([button2_1])

    return json.dumps(
        {
            "one_time": False,
            "buttons": buttons
        }
        , ensure_ascii=False)


def get_other_keyboard():
    buttons = []

    button1_1 = create_button_positive('Ресурсы')
    button1_2 = create_button_positive('FAQ')
    button2_1 = create_button_primary('Поддержка')
    button2_2 = create_button_negative('Назад')

    buttons.append([button1_1, button1_2])
    buttons.append([button2_1, button2_2])

    return json.dumps(
        {
            "one_time": False,
            "buttons": buttons
        }
        , ensure_ascii=False)


def registration_check(uid):
    is_registered = True
    message = ''

    with ScheduleDB(app.config) as db:
        user = db.find_user(uid)
    if not user or user[0] is None:
        user = None
        is_registered = False
        message = registration_message

    return is_registered, message, user
