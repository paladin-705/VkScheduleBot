import configparser

import helpers
from scheduledb import ScheduleDB
from scheduleCreator import create_schedule_text
import vkapi

from datetime import datetime, timedelta
import threading
from time import sleep

# Статистика
from statistic import track


config = configparser.ConfigParser()
config.read('config.cfg')


def send_schedule(users, current_time, day, week_type):
    blacklist = config.get('bot', 'VK_ID_BLACKLIST').split(',')
    
    if users is None:
        return None
    try:
        count = 0
        for user in users:
            uid = user[0]
            tag = user[1]
            
            if str(uid) in blacklist:
                continue
            
            schedule, is_empty = create_schedule_text(tag, day, week_type)
            if is_empty:
                continue
            vkapi.send_auto_posting_message(uid, config.get('bot', 'TOKEN'), schedule)
            count += 1

            # Статистика
            track(config.get('bot', 'STATISTIC_TOKEN'), uid, current_time, 'auto_posting')

            if count > 20:
                count = 0
                sleep(1)
    except BaseException as e:
        vkapi.send_error_message(config.get('bot', 'ADMIN_VK_ID'), config.get('bot', 'TOKEN'), str(e))


def auto_posting(current_time):
    today = datetime.now()
    week_type = (today.isocalendar()[1] + int(config.get('bot', 'WEEK_TYPE'))) % 2

    if datetime.weekday(today) == 6:
        today += timedelta(days=1)
        week_type = (week_type + 1) % 2

    day = helpers.daysOfWeek[datetime.weekday(today)]

    # Выборка пользователей из базы у которых установлена отправка расписания на текущий день
    with ScheduleDB() as db:
        users = db.find_users_where(auto_posting_time=current_time, is_today=True)

    send_schedule(users, current_time, day, week_type)

    # Выборка пользователей из базы у которых установлена отправка расписания на завтрашний день,
    # если сегодня воскресенье, то расписание будет отправляться на понедельник.
    if datetime.weekday(datetime.now()) != 6:
        today += timedelta(days=1)

    day = helpers.daysOfWeek[datetime.weekday(today)]

    with ScheduleDB() as db:
        users = db.find_users_where(auto_posting_time=current_time, is_today=False)

    send_schedule(users, current_time, day, week_type)


if __name__ == "__main__":
    while True:
        threading.Thread(target=auto_posting(datetime.now().time().strftime("%H:%M:00"))).start()
        # Вычисляем разницу в секундах, между началом минуты и временем завершения потока
        time_delta = datetime.now() - datetime.now().replace(second=0, microsecond=0)
        # Поток засыпает на время равное количеству секунд до следующей минуты
        sleep(60 - time_delta.seconds)
