from flask import current_app as app
from app import command_system, helpers
from app.scheduledb import ScheduleDB
from app.scheduleCreator import create_schedule_text
from app.helpers import registration_check
from app.messages import registration_message, error_message
from app.helpers import get_main_keyboard

from datetime import datetime, time, timedelta

# Статистика
from app.statistic import track


def schedule(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'schedule')

    try:
        is_registered, message, user = registration_check(uid)
        if not is_registered:
            return message, '', get_main_keyboard(is_registered=False)
    except BaseException as e:
        app.logger.warning('schedule: {}'.format(str(e)))
        return error_message, '', ''

    try:
        week_type = -1
        message = ''

        if key == 'неделя' or key == 'расписание':
            days = helpers.ScheduleType['неделя']
        elif key == 'вчера':
            yesterday = datetime.now()
            yesterday -= timedelta(days=1)

            week_type = (yesterday.isocalendar()[1] + app.config['WEEK_TYPE']) % 2

            days = [helpers.daysOfWeek[datetime.weekday(yesterday)]]
        elif key == 'сегодня':
            today = datetime.now()
            # Если запрашивается расписание на сегодняшний день,
            # то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            week_type = (today.isocalendar()[1] + app.config['WEEK_TYPE']) % 2

            # Если время больше чем 21:30, то показываем расписание на следующий день
            #if today.time() >= time(21, 30):
            #   today += timedelta(days=1)
            # Если сегодня воскресенье, то показывается расписание на понедельник следующей недели
            # Также в этом случае, как week_type используется тип следующей недели
            if datetime.weekday(today) == 6:
               today += timedelta(days=1)
               week_type = (week_type + 1) % 2

            days = [helpers.daysOfWeek[datetime.weekday(today)]]
        elif key == 'завтра':
            tomorrow = datetime.now()
            tomorrow += timedelta(days=1)
            # Если запрашивается расписание на завтрашний день,
            # то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            week_type = (tomorrow.isocalendar()[1] + app.config['WEEK_TYPE']) % 2


            # Если сегодня воскресенье, то показывается расписание на понедельник следующей недели
            # Также в этом случае, как week_type используется тип следующей недели
            #if datetime.weekday(tomorrow) == 6:
            #   tomorrow += timedelta(days=1)
            #   week_type = (week_type + 1) % 2

            days = [helpers.daysOfWeek[datetime.weekday(tomorrow)]]
        elif key == 'послезавтра':
            day_after_tomorrow = datetime.now()
            day_after_tomorrow += timedelta(days=2)
            # Если запрашивается расписание на завтрашний день,
            # то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            week_type = (day_after_tomorrow.isocalendar()[1] + app.config['WEEK_TYPE']) % 2

            # Если сегодня воскресенье, то показывается расписание на понедельник следующей недели
            # Также в этом случае, как week_type используется тип следующей недели
            # if datetime.weekday(tomorrow) == 6:
            #   tomorrow += timedelta(days=1)
            #   week_type = (week_type + 1) % 2

            days = [helpers.daysOfWeek[datetime.weekday(day_after_tomorrow)]]
        else:
            days = [helpers.ScheduleType[key]]

        for day in days:
            try:
                with ScheduleDB(app.config) as db:
                    user = db.find_user(uid)
                if user and user[0] != '':
                    result = create_schedule_text(user[0], day, week_type)
                    message += result[0] + "\n\n"
                else:
                    message = registration_message
            except BaseException as e:
                if uid == 354726059:
                    return 'schedule: ' + str(e), '', ''
                message = error_message
    except BaseException as e:
        app.logger.warning('schedule: {}'.format(str(e)))
        return error_message, '', ''
    return message, '', ''


schedule_command = command_system.Command()

schedule_command.keys = ['расписание', 'неделя', 'вчера', 'сегодня', 'завтра', 'послезавтра',
                         'понедельник', 'вторник', "среда", 'четверг', "пятница", "суббота", 'воскресенье']
schedule_command.description = 'Выводит расписание на неделю, также вместо команды "расписание" ' \
                               'можно написать любой день недели или команду "сегодня" или "завтра"'
schedule_command.process = schedule
