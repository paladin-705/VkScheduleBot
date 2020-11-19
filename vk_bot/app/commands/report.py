from flask import current_app as app
from app import command_system
from app.scheduledb import ScheduleDB
from app.messages import error_message, report_help_message, report_ok_message

# Статистика
from app.statistic import track


def report(uid, key, arg=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, arg, 'report')

    if arg != '':
        with ScheduleDB(app.config) as db:
            if db.add_report(uid, arg):
                return report_ok_message, '', ''
            else:
                return error_message, '', ''
    else:
        return report_help_message, '', ''


report_command = command_system.Command()

report_command.keys = ['отзыв', 'поддержка', 'репорт', '/report', 'report', '/send_report', 'send_report']
report_command.description = 'Можно отправить информацию об ошибке или что то ещё. ' \
                             'Введите команду(без кавычек): отзыв <ваше сообщение>'
report_command.process = report
