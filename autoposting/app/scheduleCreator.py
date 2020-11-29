# -*- coding: utf-8 -*-
from functools import lru_cache

from scheduledb import ScheduleDB
import helpers


def print_type(raw_type, week_type=-1):
    # Если задан тип недели (числитель/знаменатель), т.е week_type не равен значению по умолчанию,
    # то дополнительная информация о типе недели не выводится
    if week_type != -1:
        return ""

    raw_type = int(raw_type)
    if raw_type == 0:
        return "числ"
    elif raw_type == 1:
        return "знам"
    else:
        return ""


def print_week_type(week_type=-1):
    if week_type == 0:
        return "числитель"
    elif week_type == 1:
        return "знаменатель"
    else:
        return ""


@lru_cache(maxsize=128)
def create_schedule_text(tag, day, week_type, config):
    result = []
    schedule = ""
    is_empty = True
    try:
        with ScheduleDB(config) as db:
            data = db.get_schedule(tag, day, week_type)

        schedule += "🔎 | {}: {}\n\n".format(
            helpers.daysOfWeek_rus[day], print_week_type(week_type))
        index = 0
        while index < len(data):
            is_empty = False
            row = data[index]

            title = ' '.join(str(row[1]).split())
            classroom = ' '.join(str(row[2]).split())

            schedule +=  '⏳ | {} пара: '.format(str(row[0]))
            # Этот блок нужен для вывода тех занятий, где занятия по числителю и знамнателю различаются
            if index != len(data) - 1:
                # Сравнивается порядковый номер занятия данной и следующей строки и если они равны,
                # то они выводятся вместе
                if data[index + 1][0] == row[0]:
                    schedule += '{0} {1} {2}\n'.format(title, classroom, print_type(row[3], week_type))

                    index += 1
                    row = data[index]
                    title = ' '.join(str(row[1]).split())
                    classroom = ' '.join(str(row[2]).split())

                    schedule += '&#12288;&#10;&#12288;' \
                                '&#12288;&#10;&#12288;' \
                                '&#12288;&#10;{0} {1} {2}\n\n'.format(title, classroom, print_type(row[3], week_type))
                else:
                    schedule += '{0} {1} {2}\n\n'.format(title, classroom, print_type(row[3], week_type))
            else:
                schedule += '{0} {1} {2}\n\n'.format(title, classroom, print_type(row[3], week_type))

            index += 1
        result.append(schedule)
        result.append(is_empty)
    except:
        pass
    finally:
        if len(result) != 2:
            result = ['', True]
        return result
