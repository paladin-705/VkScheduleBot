import difflib
import importlib
import json
import os
import re

from flask import current_app as app

from app.registration_stage_1 import registration_stage_1
from app.registration_stage_2 import registration_stage_2
from app.registration_stage_3 import registration_stage_3
from app.registration_stage_4 import registration_stage_4

from app import vkapi
from app.scheduledb import ScheduleDB
from app.helpers import registration_check
from app.command_system import command_list
from app.statistic import track
from app.helpers import get_keyboard
from app.messages import unknown_message, schedule_info_message, error_message


def load_modules():
    # путь от рабочей директории, ее можно изменить в настройках приложения
    files = os.listdir("app/commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("app.commands." + m[0:-3])


def get_answer(uid, body):
    data = body.split(' ', maxsplit=1)
    user_command = data[0]
    arg = ""
    if len(data) == 2:
        arg = data[1]

    # Если пользователя нет в базе, то ему выведет предложение зарегистрироваться
    try:
        # Сообщение по умолчанию если распознать не удастся
        message = unknown_message

        max_ratio = 0
        command = None
        key = ''

        for c in command_list:
            for k in c.keys:
                ratio1 = difflib.SequenceMatcher(None, k, user_command).ratio()
                ratio2 = difflib.SequenceMatcher(None, k, body).ratio()
                ratio = max(ratio1, ratio2)

                if ratio > max_ratio:
                    max_ratio = ratio
                    command = c
                    key = k
                    if ratio >= 0.95:
                        message, attachment, keyboard = c.process(uid, key, arg)
                        return message, attachment, keyboard
        if max_ratio > 0.5:
            message, attachment, keyboard = command.process(uid, key, arg)
            message = "Ваш запрос распознан как: {}\n\n{}\n\n" \
                      "Если запрос был распознан неправильно, напишите 'помощь', " \
                      "чтобы узнать доступные команды".format(key, message)
            return message, attachment, keyboard
        else:
            # Статистика
            track(app.config['STATISTIC_TOKEN'], uid, body, 'unknown')

    except BaseException as e:
        app.logger.warning('get_answer: {}'.format(str(e)))
        return error_message, '', ''

    return message, '', ''


def create_answer(data):
    load_modules()

    user_id = data['peer_id']

    rcvd_message = re.sub(r'\[\w*\|@\w*\][,\s]?\s?', '', data['text'].lower()) # Из текста убирается упоминание бота с помощью @, если оно присутствует
    action = json.loads(data.get('action', '{}'))
    payload = json.loads(data.get('payload', '{}'))
    
    payload_reg = payload.get('registration', '')
    payload_data = re.split(r':', payload_reg)
    
    p_type = payload_data[0] if len(payload_data) >= 1 else ''
    p_stage = payload_data[1] if len(payload_data) >= 2 else ''
    p_key = payload_data[2] if len(payload_data) >= 3 else ''
    
    if 'auto_posting_on' in payload.keys():
        rcvd_message = 'auto_posting_on'
    
    action_type = payload.get('type', '')
    
    if action_type == 'chat_invite_user':
        rcvd_message = 'start'
    
    if p_type == 'reg':
        attachment = ''
        text_data = rcvd_message.split(' ', maxsplit=1)[0]

        if p_stage == 'stage 1':
            message, keyboard = registration_stage_1(user_id, p_key, text_data)
        elif p_stage == 'stage 2':
            message, keyboard = registration_stage_2(user_id, p_key, text_data)
        elif p_stage == 'stage 3':
            message, keyboard = registration_stage_3(user_id, p_key, text_data)
        elif p_stage == 'stage 4':
            message, keyboard = registration_stage_4(user_id, p_key, text_data)
        else:
            keyboard = ''
            message, attachment = get_answer(user_id, rcvd_message)
    elif 'schedule' in payload.keys():
        message, attachment, keyboard = schedule_info_message, '', get_keyboard()
    else:
        message, attachment, keyboard = get_answer(user_id, rcvd_message)

    vkapi.send_message(data, app.config['TOKEN'], message, attachment, keyboard)

    # Статистика
    track(app.config['STATISTIC_TOKEN'], user_id, message, '', 'agent')


def message_deny_handler(data):
    uid = data['user_id']

    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, 'message_deny', 'message_deny')

    try:
        is_registered, message, user = registration_check(uid)
        if not is_registered:
            return
        with ScheduleDB(app.config) as db:
            db.set_auto_post_time(uid, None, None)
    except BaseException as e:
        app.logger.warning('message_deny: {}'.format(str(e)))
