from flask import current_app as app
from app import command_system
from app.helpers import get_main_keyboard
from app.helpers import registration_check
from app.messages import error_message, start_message

# Статистика
from app.statistic import track


def start(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'start')

    # Если пользователя нет в базе, то ему выведет предложение зарегистрироваться
    try:
        is_registered, message, user = registration_check(uid)

        if not is_registered:
            return start_message, '', get_main_keyboard(is_registered=False)
        else:
            return start_message, '', get_main_keyboard(is_registered=True)
    except BaseException as e:
        app.logger.warning('start: {}'.format(str(e)))
        return error_message, '', ''


start_command = command_system.Command()

start_command.keys = ['старт', '/start', 'start', 'привет', 'здравствуй', 'начать']
start_command.description = 'Выводит стартовое сообщение'
start_command.process = start
