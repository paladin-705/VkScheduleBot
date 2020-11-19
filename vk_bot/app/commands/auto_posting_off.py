from flask import current_app as app
from app import command_system
from app.scheduledb import ScheduleDB
from app.helpers import registration_check
from app.messages import error_message, auto_posting_off_message

# Статистика
from app.statistic import track


def auto_posting_off(uid, key, arg=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, arg, 'auto_posting_off')

    try:
        is_registered, message, user = registration_check(uid)
        if not is_registered:
            return message, '', ''

        with ScheduleDB(app.config) as db:
            if db.set_auto_post_time(uid, None, None):
                return auto_posting_off_message, '', ''
            else:
                return error_message, '', ''
    except BaseException as e:
        app.logger.warning('auto_posting_off: {}'.format(str(e)))
        return error_message, '', ''


auto_posting_off_command = command_system.Command()

auto_posting_off_command.keys = ['отключить рассылку', 'ap off', 'ар off', 'автопостинг off',
                                 '/auto_posting_off', 'auto_posting_off']
auto_posting_off_command.description = 'Выключение автоматической отправки расписания'
auto_posting_off_command.process = auto_posting_off
