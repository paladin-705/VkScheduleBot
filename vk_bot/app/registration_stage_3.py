from flask import current_app as app
from app.scheduledb import ScheduleDB
from app.scheduledb import organization_field_length
from app.messages import error_message
from app.helpers import create_button_negative
import json

# Статистика
from app.statistic import track


def registration_stage_3(uid, key, data):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, data, 'registration-stage-3')

    try:
        with ScheduleDB(app.config) as db:
            result = db.get_group(key)

        if len(result) == 0:
            return error_message, ''

        buttons = []

        for i in range(len(result)):
            row = result[i]
            if (i % 3) == 0:
                buttons.append([])
            buttons[int(i / 3)].append({
                        "action": {
                            "type": "text",
                            "label": str(row[0]),
                            "payload": {
                                "registration": "reg:stage 4:{0}".format(str(row[1]))
                            }
                        },
                        "color": "default"
                    })
        buttons.append([create_button_negative('Назад', {
            'registration': 'reg:stage 2:{0}'.format(
                str(row[1])[:organization_field_length])
        })])

        return 'Выберите группу:', json.dumps(
            {
                "one_time": False,
                "buttons": buttons
            }
            , ensure_ascii=False)
    except BaseException as e:
        app.logger.warning('registration_stage_3: {}'.format(str(e)))
        return error_message, ''
