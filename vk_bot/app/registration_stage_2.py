from flask import current_app as app
from app.scheduledb import ScheduleDB
from app.scheduledb import organization_field_length
from app.scheduledb import faculty_field_length
from app.messages import error_message
from app.helpers import create_button_negative
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
        
        if len(result) > 8:
            buttons_in_row = 3
        else:
            buttons_in_row = 2
        
        buttons = []
        for i in range(len(result)):
            row = result[i]
            if (i % buttons_in_row) == 0:
                buttons.append([])
            buttons[int(i / buttons_in_row)].append({
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
        buttons.append([create_button_negative('Назад', {'registration': 'reg:stage 1:'})])

        return 'Выберите курс:', json.dumps(
            {
                "one_time": False,
                "buttons": buttons
            }
            , ensure_ascii=False)
    except BaseException as e:
        app.logger.warning('registration_stage_2: {}'.format(str(e)))
        return error_message, ''
