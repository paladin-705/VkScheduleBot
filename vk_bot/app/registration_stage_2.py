from flask import current_app as app
from app.scheduledb import ScheduleDB
from app.scheduledb import organization_field_length
from app.scheduledb import faculty_field_length
from app.messages import error_message
import json

# Статистика
from app.statistic import track


def registration_stage_2(uid, key, data):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, data, 'registration-stage-2')

    try:
        with ScheduleDB(app.config) as db:
            result = db.get_faculty(key)

        if len(result) == 0:
            return error_message, ''

        buttons = []
        for i in range(len(result)):
            row = result[i]
            if (i % 2) == 0:
                buttons.append([])
            buttons[int(i / 2)].append({
                        "action": {
                            "type": "text",
                            "label": str(row[0]),
                            "payload":  {
                                "registration": "reg:stage 3:{0}".format(
                                    str(row[1])[:organization_field_length + faculty_field_length])
                            }
                        },
                        "color": "default"
                    })

        return 'Выберите курс:', json.dumps(
            {
                "one_time": False,
                "buttons": buttons
            }
            , ensure_ascii=False)
    except BaseException as e:
        app.logger.warning('registration_stage_2: {}'.format(str(e)))
        return error_message, ''
