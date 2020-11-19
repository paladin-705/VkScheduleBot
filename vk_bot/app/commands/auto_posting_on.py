from flask import current_app as app
from app import command_system
from app.scheduledb import ScheduleDB
from app.helpers import registration_check
from app.messages import registration_message, error_message, auto_posting_on_help_message

import re
import difflib

# Статистика
from app.statistic import track


def auto_posting_on(uid, key, arg=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, arg, 'auto_posting_on')

    data = arg.split(' ', maxsplit=1)
    time = data[0]
    type = ''

    if len(data) == 2:
        type = data[1]
    try:
        if re.match(time, r'\d{1,2}:\d\d'):
            raise BaseException
    except:
        return auto_posting_on_help_message, '', ''

    try:
        is_registered, message, user = registration_check(uid)
        if not is_registered:
            return message, '', ''

        with ScheduleDB(app.config) as db:
            hour = ''.join(filter(lambda x: x.isdigit(), re.split(r':', time)[0]))
            minutes = ''.join(filter(lambda x: x.isdigit(), re.split(r':', time)[1]))

            if difflib.SequenceMatcher(None, type, 'сегодня').ratio() > \
                    difflib.SequenceMatcher(None, type, 'завтра').ratio() or type == '':
                is_today = True
            else:
                is_today = False

            # Проверка на соответствие введённых пользователем данных принятому формату
            if not hour.isdigit() or not minutes.isdigit():
                return auto_posting_on_help_message, '', ''

            if db.set_auto_post_time(uid, (hour + ":" + minutes + ":" + "00").rjust(8, '0'), is_today):
                return 'Время установлено', '', ''
            else:
                return error_message, '', ''
    except BaseException as e:
        app.logger.warning('auto_posting_on: {}'.format(str(e)))
        return error_message, '', ''


auto_posting_on_command = command_system.Command()

auto_posting_on_command.keys = ['рассылка', 'ap', 'ар', 'автопостинг', '/auto_posting_on', 'auto_posting_on']
auto_posting_on_command.description = 'Включение и выбор времени для автоматической отправки расписания в диалог, ' \
                                      'время должно иметь формат ЧЧ:ММ'
auto_posting_on_command.process = auto_posting_on
