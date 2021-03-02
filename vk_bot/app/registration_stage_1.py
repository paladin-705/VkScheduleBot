from flask import current_app as app
from app.scheduledb import ScheduleDB
from app.scheduledb import organization_field_length
from app.messages import error_message
from app.helpers import create_button_negative
import json

# Статистика
from app.statistic import track


def registration_stage_1(uid, key, data):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, data, 'registration-stage-1')

    try:
        with ScheduleDB(app.config) as db:
            result = db.get_organizations()
        if len(result) == 0:
            return error_message, ''

        buttons = []

        for row in result:
            buttons.append(
                [
                    {
                        "action": {
                            "type": "text",
                            "label": str(row[0]),
                            "payload": {
                                "registration": "reg:stage 2:{0}".format(str(row[1])[:organization_field_length])
                            }
                        },
                        "color": "default"
                    }
                ])
        buttons.append([create_button_negative('Назад')])

        return 'Выберите организацию:', json.dumps(
            {
                "one_time": False,
                "buttons": buttons
            }
            , ensure_ascii=False)
    except BaseException as e:
        app.logger.warning('registration_stage_1: {}'.format(str(e)))
        return error_message, ''
