from flask import current_app as app
from app import command_system
from app.helpers import get_settings_keyboard
from app.helpers import registration_check
from app.messages import error_message, settings_message

# Статистика
from app.statistic import track


def settings(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'settings')

    try:
        is_registered, message, user = registration_check(uid)

        if not is_registered:
            return settings_message, '', get_settings_keyboard(is_registered=False)
        else:
            return settings_message, '', get_settings_keyboard(is_registered=True)
    except BaseException as e:
        app.logger.warning('settings: {}'.format(str(e)))
        return error_message, '', ''


settings_command = command_system.Command()

settings_command.keys = ['настройки', '/settings', 'settings']
settings_command.description = 'Настройки'
settings_command.process = settings
