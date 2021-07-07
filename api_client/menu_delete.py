import json
from api import login
from api import (delete_all_orgs, delete_org, delete_faculty,
                 delete_group, delete_group_schedule, delete_group_exams)
from menu_helpers import input_org_info
from menu_get import create_org_structure


def confirm():
    answer = input('Для потдверждения введите y: ')
    if answer == 'y':
        return True
    else:
        return False


def menu_delete_all_orgs(ip, port, username, password):
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит данные всех организаций, а также всё расписание занятий и экзаменов.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        delete_all_orgs(ip, port, access_token)
        print('Все организации усешно удалены')
    else:
        print('Действие отменено')


def menu_delete_org(ip, port, username, password):
    org = input('Введите организацию: ')
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит данные указанной организации, '
          'а также всё расписание занятий и экзаменов принадлежащее ей.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        delete_org(ip, port, access_token, org)
        print('Организация {} успешно удалена'.format(org))
    else:
        print('Действие отменено')


def menu_delete_faculty(ip, port, username, password):
    org = input('Введите организацию: ')
    faculty = input('Введите курс(кафедру): ')
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит данные указанного курса(кафедры), '
          'а также всё расписание занятий и экзаменов принадлежащее ему.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        delete_faculty(ip, port, access_token, org, faculty)
        print('Курс(кафедра) {} организации {} успешно удалён'.format(faculty, org))
    else:
        print('Действие отменено')


def menu_delete_group(ip, port, username, password):
    org, faculty, group = input_org_info()
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит данные указанной группы, '
          'а также всё расписание занятий и экзаменов '
          'принадлежащее ей.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        delete_group(ip, port, access_token, org, faculty, group)
        print('Группа {} курса(кафедры) {} организации {} успешно удалена'.format(group, faculty, org))
    else:
        print('Действие отменено')


def menu_delete_groups_from_json(ip, port, username, password, login_attempt=10):
    file_name = input('Введите имя json файла: ')

    with open(file_name) as json_file:
        json_data = json.load(json_file)

    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит данные указанных в json файле групп, '
          'а также всё расписание занятий и экзаменов '
          'принадлежащих им.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        for org_data in json_data:
            org = org_data[0]
            faculty = org_data[1]
            group = org_data[2]

            for attempt in range(login_attempt):
                try:
                    delete_group(ip, port, access_token, org, faculty, group)
                    print('Группа {} курса(кафедры) {} организации {} успешно удалена'.format(
                            group, faculty, org))
                except AccessDeniedError:
                    access_token, refresh_token = login(ip, port, username, password)
                    continue
                break
    else:
        print('Действие отменено')


def menu_delete_group_schedule(ip, port, username, password):
    org, faculty, group = input_org_info()
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит расписание занятий указанной группы.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        delete_group_schedule(ip, port, access_token, org, faculty, group)
        print('Расписание занятий '
              'группы (преподавателя) {} курса(кафедры) {} организации {} успешно удалено'.format(group, faculty, org))
    else:
        print('Действие отменено')


def menu_delete_group_exams(ip, port, username, password):
    org, faculty, group = input_org_info()
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит расписание экзаменов указанной группы.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        delete_group_exams(ip, port, access_token, org, faculty, group)
        print('Расписание экзаменов '
              'группы (преподавателя) {} курса(кафедры) {} организации {} успешно удалено'.format(group, faculty, org))
    else:
        print('Действие отменено')


def menu_delete_all_schedule(ip, port, username, password, login_attempt=10):
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит расписание занятий всех групп.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        org_data = create_org_structure(ip, port, username, password)

        for org in org_data:
            for faculty in org_data[org]:
                for group in org_data[org][faculty]:
                    for attempt in range(login_attempt):
                        try:
                            delete_group_schedule(ip, port, access_token, org, faculty, group)
                            print('Расписание занятий '
                                  'группы (преподавателя) {} курса(кафедры) {} организации {} успешно удалено'.format(
                                    group, faculty, org))
                        except AccessDeniedError:
                            access_token, refresh_token = login(ip, port, username, password)
                            continue
                        break
    else:
        print('Действие отменено')


def menu_delete_all_exams(ip, port, username, password, login_attempt=10):
    print('ВНИМАНИЕ:')
    print('Это действие безвозвратно удалит расписание экзаменов всех групп.')

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        org_data = create_org_structure(ip, port, username, password)

        for org in org_data:
            for faculty in org_data[org]:
                for group in org_data[org][faculty]:
                    for attempt in range(login_attempt):
                        try:
                            delete_group_exams(ip, port, access_token, org, faculty, group)
                            print('Расписание экзаменов '
                                  'группы (преподавателя) {} курса(кафедры) {} организации {} успешно удалено'.format(
                                    group, faculty, org))
                        except AccessDeniedError:
                            access_token, refresh_token = login(ip, port, username, password)
                            continue
                        break
    else:
        print('Действие отменено')
