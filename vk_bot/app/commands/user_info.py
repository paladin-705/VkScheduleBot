from flask import current_app as app
from app import command_system
from app.scheduledb import ScheduleDB
from app.helpers import get_user_info_keyboard
from app.helpers import registration_check
from app.messages import error_message, user_info_title_message, \
    user_info_faculty_message, user_info_group_message, \
    user_info_ap_time_message, user_info_ap_type_message

# Статистика
from app.statistic import track


def user_info(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'user_info')

    # Если пользователя нет в базе, то ему выведет предложение зарегистрироваться
    try:
        is_registered, message, user = registration_check(uid)

        if not is_registered:
            return user_info_title_message, '', get_user_info_keyboard(is_registered=False)
        else:
            with ScheduleDB(app.config) as db:
                info = db.get_user_info(uid)

            if info is None:
                faculty = 'Пусто'
                group = 'Пусто'
                ap_time = 'Не установлено'
                ap_type = 'Не установлено'
            else:
                faculty = ' '.join(str(info[1]).split()) if len(info) >= 2 else 'Пусто'
                group = ' '.join(str(info[2]).split()) if len(info) >= 3 else 'Пусто'

                if len(info) >= 5 and info[3] is not None:
                    ap_time = str(info[3]) if info[3] is not None else 'Не установлено'
                    ap_type = 'На сегодня' if info[4] else 'На завтра'
                else:
                    ap_time = 'Не установлено'
                    ap_type = 'Не установлено'

            message = '{}\n{}: {}\n{}: {}\n{}: {}\n{}: {}'.format(
                user_info_title_message,
                user_info_faculty_message, faculty,
                user_info_group_message, group,
                user_info_ap_time_message, ap_time,
                user_info_ap_type_message, ap_type)
            return message, '', get_user_info_keyboard(is_registered=True)
    except BaseException as e:
        app.logger.warning('user_info: {}'.format(str(e)))
        return error_message, '', ''


user_info_command = command_system.Command()

user_info_command.keys = ['личный кабинет', '/user_info', 'user_info']
user_info_command.description = 'Личный кабинет'
user_info_command.process = user_info
