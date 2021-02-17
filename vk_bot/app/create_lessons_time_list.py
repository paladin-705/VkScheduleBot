from functools import lru_cache

from flask import current_app as app

from app.scheduledb import ScheduleDB
from app import app


@lru_cache(maxsize=1)
def create_lessons_time_list():
    time_list = ''
    try:
        with ScheduleDB(app.config) as db:
            data = db.get_lessons_time()

        time_list = '🔎 | Время начала и окончания пар\n\n'
        for number, start_time, end_time in data:
            time_list += '⏳ | {} пара: {} - {}\n'.format(
                number,
                start_time.strftime("%H:%M"),
                end_time.strftime("%H:%M"))

    except BaseException as e:
        app.logger.warning('create_lessons_time_list: {}'.format(str(e)))
    finally:
        return time_list
