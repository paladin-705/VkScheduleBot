import json
from Parser import Parser


def menu_parse_schedule():
    file_name = input('Введите имя xls файла: ')
    organization = input('Введите название организации: ')
    header_row = int(input('Номер столбца заголовков (по умолчанию 0): '))

    with Parser(file_name) as parser:
        data = parser.parse_schedule_from_excel(header_row)

    json_data = {organization: data}

    with open('schedule_data.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)
    print('Расписание занятий сохранено в schedule_data.json')


def menu_parse_exams():
    file_name = input('Введите имя xls файла: ')
    organization = input('Введите название организации: ')
    header_row = int(input('Номер столбца заголовков (по умолчанию 0): '))

    with Parser(file_name) as parser:
        data = parser.parse_exams_from_excel(header_row)

    json_data = {organization: data}

    with open('exams_data.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)
    print('Расписание экзаменов сохранено в exams_data.json')

