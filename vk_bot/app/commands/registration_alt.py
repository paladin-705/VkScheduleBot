from flask import current_app as app
from app import command_system
from app.scheduledb import ScheduleDB
from app.messages import (registration_success_message, registration_alt_help_message,
                          error_message)

# Статистика
from app.statistic import track


def registration_alt(uid, key, data=''):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, data, 'registration_alt')

    if data == '':
        return registration_alt_help_message, '', ''
    try:
        with ScheduleDB(app.config) as db:
            organizations = db.get_similar_organizations(data)

        if len(organizations) != 0:
            message = registration_success_message
            if organizations[0][2] > 0.8:
                message += '\n\nВы зарегистрированны в: {}'.format(organizations[0][1])
            else:
                message += '\n\nВы зарегистрированны в наиболее совпадающей с запросом группе: {}\n' \
                          '-----\nДругие похожие:\n'.format(organizations[0][1])
                for org in organizations:
                    message += "{}\n".format(org[1])

            with ScheduleDB(app.config) as db:
                user = db.find_user(uid)
                if user:
                    db.update_user(uid, " ", " ", organizations[0][0])
                else:
                    db.add_user(uid, " ", " ", organizations[0][0])

            return message, '', ''
        else:
            return error_message, '', ''
    except BaseException as e:
        app.logger.warning('registration_alt: {}'.format(str(e)))
        return error_message, '', ''


registration_command = command_system.Command()

registration_command.keys = ['reg', ]
registration_command.description = 'Альтернативная команда для регистрации в текстовом режиме'
registration_command.process = registration_alt
