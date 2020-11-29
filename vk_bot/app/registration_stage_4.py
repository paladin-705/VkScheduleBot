from flask import current_app as app
from app.scheduledb import ScheduleDB
from app.helpers import get_main_keyboard
from app.messages import error_message, registration_success_message

# Статистика
from app.statistic import track


def registration_stage_4(uid, key, data):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, data, 'registration-stage-4')

    try:
        with ScheduleDB(app.config) as db:
            row = db.get_group(key)

        if len(row) == 0:
            return error_message, ''

        message = registration_success_message

        with ScheduleDB(app.config) as db:
            user = db.find_user(uid)
            if user:
                db.update_user(uid, " ", " ", str(row[0][1]))
            else:
                db.add_user(uid, " ", " ", str(row[0][1]))

        return message, get_main_keyboard(is_registered=True)
    except BaseException as e:
        app.logger.warning('registration_stage_4: {}'.format(str(e)))
        return error_message, ''
