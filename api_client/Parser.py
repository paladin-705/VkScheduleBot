# -*- coding: utf-8 -*-
import pandas as pd
from parser_helpers import (parse_day, parse_time, parse_lesson_number,
                            parse_title, parse_lecturer, parse_classroom)
from parser_helpers import parse_date, parse_exam_data
from time import strftime
import sys
import logging


class Parser:
    def __init__(self, file_name):
        self.file_name = file_name

        # Логирование данных
        logger = logging.getLogger('parser-logger')
        logger.setLevel(logging.INFO)

        logFormatter = logging.Formatter('%(asctime)-15s [ %(levelname)s ] %(message)s')

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)

        # log_file = 'parser-{}.log'.format(strftime('%Y-%m-%d-%H.%M.%S'))
        # fileHandler = logging.FileHandler(mode='a', filename=log_file)
        # fileHandler.setFormatter(logFormatter)
        # logger.addHandler(fileHandler)

        self.logger = logger

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __parse_schedule(self, group_table):
        data = []               # Массив для хранения информации о лекциях
        for i in range(len(group_table)-1):
            # Взятие данных из ячейки и значений индексов
            index = group_table.index[i][0]
            lesson_info = group_table.index[i][1]

            lesson_data = group_table[i]

            # Одна пара описывается двумя строчками таблицы
            # type описывает, какая это часть описания пары
            type = i % 2

            # Если пара идёт каждую неделю, то во второй части описания пары
            # будет просто её дубликат
            if type == 1 and lecture_type == 'all':
                continue

            # Тут определяется тип пары - идёт ли она каждую неделю (all) или только раз в неделю - по чётным и
            # нечётным неделям (тип odd и even)
            if type == 0:
                if group_table[i] == group_table[i+1]:
                    lecture_type = 'all'
                else:
                    lecture_type = 'odd'
            else:
                lecture_type = 'even'

            #
            if pd.isna(lesson_data):
                continue

            day = parse_day(index)

            time_start, time_end = parse_time(lesson_info)
            lesson_number = parse_lesson_number(lesson_info)

            week_type = lecture_type

            title = parse_title(lesson_data)
            lecturer = parse_lecturer(lesson_data)
            classroom = parse_classroom(lesson_data)

            lesson_structure = {
                'day': day,
                'number': lesson_number,
                'week_type': week_type,
                'title': title,
                'classroom': classroom,
                'lecturer': lecturer,
                'time_start': time_start,
                'time_end': time_end,
            }
            data.append(lesson_structure)
        return data

    def __parse_exams(self, group_table):
        data = []  # Массив для хранения информации об экзаменах
        for i in range(len(group_table) - 1):
            exam_index = group_table.index[i]#parse_date(group_table.index[i])
            exam_info = group_table[i]#parse_exam_data(group_table[i])

            if pd.isna(exam_info):
                continue

            date = parse_date(exam_index)
            exam_data = parse_exam_data(exam_info)

            lecturer = exam_data[0] if len(exam_data) >= 1 else ''
            title = exam_data[1] if len(exam_data) >= 2 else ''
            classroom = exam_data[2] if len(exam_data) >= 3 else ''

            exam_structure = {
                'day': date,
                'title': title,
                'classroom': classroom,
                'lecturer': lecturer
            }
            data.append(exam_structure)
        return data

    def parse_schedule_from_excel(self, header_row=0):
        json_data = {}

        xls = pd.ExcelFile(self.file_name, engine='openpyxl')
        for sheet in xls.sheet_names:
            df = pd.read_excel(self.file_name, sheet, engine='openpyxl', header=header_row, index_col=[0, 1])
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            json_data[sheet] = {}
            for group in df.columns.values:
                self.logger.info('Load {} | {}'.format(sheet, group))
                group_table = df[group]

                # Парсинг занятий
                json_data[sheet][group] = self.__parse_schedule(group_table)
        return json_data

    def parse_exams_from_excel(self, header_row=0):
        json_data = {}

        xls = pd.ExcelFile(self.file_name, engine='openpyxl')
        for sheet in xls.sheet_names:
            df = pd.read_excel(self.file_name, sheet, engine='openpyxl', header=header_row, index_col=0)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            json_data[sheet] = {}
            for group in df.columns.values:
                self.logger.info('Load {} | {}'.format(sheet, group))
                group_table = df[group]

                # Парсинг экзаменов
                json_data[sheet][group] = self.__parse_exams(group_table)
        return json_data
