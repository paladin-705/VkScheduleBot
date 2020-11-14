# -*- coding: utf-8 -*-
from menu_parse import menu_parse_schedule, menu_parse_exams
from menu_get import menu_get_org_structure, menu_get_schedule, menu_get_exams
from menu_add import menu_add_schedule, menu_add_exams, menu_add_group
from menu_delete import (menu_delete_all_orgs, menu_delete_org, menu_delete_faculty,
                         menu_delete_group, menu_delete_group_schedule, menu_delete_group_exams)


def show_menu():
    print('=======\n')
    print('Парсинг данных:')
    print('1.\tПарсинг xls файла с расписанием занятий')
    print('2.\tПарсинг xls файла с расписанием экзаменов')

    print('Просмотр данных:')
    print('3.\tВывод структуры групп в БД')
    print('4.\tВывод расписания занятий группы (преподавателя)')
    print('5.\tВывод экзаменов занятий группы (преподавателя)')

    print('Добавление данных:')
    print('6.\tЗагрузка расписания занятий в БД из json файла')
    print('7.\tЗагрузка расписания экзаменов в БД из json файла')
    print('8.\tДобавление группы в БД')

    print('Удаление данных:')
    print('9.\tУдаление расписания занятий')
    print('10.\tУдаление расписания экзаменов')
    print('11.\tУдаление группы(преподавателя)')
    print('12.\tУдаление курса(кафедры)')
    print('13.\tУдаление организации')
    print('14.\tУдаление всех организаций')
    print()
    print('15.\tВыход')

    try:
        menu_type = int(input('Введите номер пункта: '))
    except ValueError:
        menu_type = None

    return menu_type


if __name__ == '__main__':
    ip = input('Введите адрес сервера: ')
    port = input('Введите порт сервера: ')

    username = input('Введите имя пользоватея: ')
    password = input('Введите пароль: ')

    while True:
        try:
            menu_type = show_menu()

            if menu_type == 1:
                menu_parse_schedule()
            elif menu_type == 2:
                menu_parse_exams()

            elif menu_type == 3:
                menu_get_org_structure(ip, port, username, password)
            elif menu_type == 4:
                menu_get_schedule(ip, port, username, password)
            elif menu_type == 5:
                menu_get_exams(ip, port, username, password)

            elif menu_type == 6:
                menu_add_schedule(ip, port, username, password)
            elif menu_type == 7:
                menu_add_exams(ip, port, username, password)
            elif menu_type == 8:
                menu_add_group(ip, port, username, password)

            elif menu_type == 9:
                menu_delete_group_schedule(ip, port, username, password)
            elif menu_type == 10:
                menu_delete_group_exams(ip, port, username, password)
            elif menu_type == 11:
                menu_delete_group(ip, port, username, password)
            elif menu_type == 12:
                menu_delete_faculty(ip, port, username, password)
            elif menu_type == 13:
                menu_delete_org(ip, port, username, password)
            elif menu_type == 14:
                menu_delete_all_orgs(ip, port, username, password)

            elif menu_type == 15:
                break
            else:
                print('Неопознанная команда')
        except BaseException as e:
            print('Исключение: {}', str(e))
