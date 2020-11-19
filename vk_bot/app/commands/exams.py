from flask import current_app as app
from app import command_system
from app.scheduledb import ScheduleDB
from app.helpers import registration_check
from app.messages import error_message

# Статистика
from app.statistic import track


def exams(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'exams')

    try:
        is_registered, message, user = registration_check(uid)
        if not is_registered:
            return message, '', ''

        with ScheduleDB(app.config) as db:
            exams_list = db.get_exams(user[0])

        message = ''
        for exam in exams_list:
            message += exam[0].strftime('%d.%m.%Y') + ":\n"

            title = ' '.join(str(exam[1]).split())
            lecturer = ' '.join(str(exam[2]).split())
            classroom = ' '.join(str(exam[3]).split())

            message += title + ' | ' + lecturer + ' | ' + classroom + "\n"
            message += "------------\n"
        if len(message) == 0:
            message = 'Похоже расписания экзаменов для вашей группы нет в базе'
    except BaseException as e:
        app.logger.warning('exams: {}'.format(str(e)))
        return error_message, '', ''
    return message, '', ''


exams_command = command_system.Command()

exams_command.keys = ['экзамены', 'экзамен', '/exams', 'exams']
exams_command.description = 'Выводит список экзаменов'
exams_command.process = exams
