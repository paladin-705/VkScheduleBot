from flask import current_app as app
from app import command_system
from app.create_lessons_time_list import create_lessons_time_list
from app.messages import error_message

# Статистика
from app.statistic import track


def lessons_time_list(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'lessons_time_list')

    try:
        message = create_lessons_time_list()

        if len(message) == 0:
            message = 'Похоже времени начала и окончания пар ещё нет в базе'

    except BaseException as e:
        app.logger.warning('lessons_time_list: {}'.format(str(e)))
        return error_message, '', ''
    return message, '', ''


lessons_time_list_command = command_system.Command()

lessons_time_list_command.keys = ['время занятий', 'time', '/lessons_time', 'lessons_time', '/time', 'time']
lessons_time_list_command.description = 'Выводит время начала и окончания пар'
lessons_time_list_command.process = lessons_time_list
