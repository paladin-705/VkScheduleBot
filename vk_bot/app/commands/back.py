from flask import current_app as app
from app import command_system
from app.helpers import get_main_keyboard
from app.helpers import registration_check
from app.messages import back_message, error_message

# Статистика
from app.statistic import track


def back(uid, key, data=''):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'back')

    # Если пользователя нет в базе, то ему выведет предложение зарегистрироваться
    try:
        is_registered, message, user = registration_check(uid)
        if not is_registered:
            return back_message, '', get_main_keyboard(is_registered=False)
        else:
            return back_message, '', get_main_keyboard(is_registered=True)
    except BaseException as e:
        app.logger.warning('back: {}'.format(str(e)))
        return error_message, '', ''


back_command = command_system.Command()

back_command.keys = ['назад', '/back', 'back']
back_command.description = 'Возвращение в главное меню'
back_command.process = back
