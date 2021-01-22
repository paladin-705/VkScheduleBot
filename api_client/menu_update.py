import json
import re
from menu_get import create_org_structure
from menu_delete import confirm
from menu_helpers import input_org_info
from api import login, update_group
from api import AccessDeniedError


def menu_update_group(ip, port, username, password):
    print('Введите текущие данные группы:')
    old_org, old_faculty, old_group = input_org_info()

    print('Введите новые (изменённые) данные группы:')
    new_org, new_faculty, new_group = input_org_info()

    print('ВНИМАНИЕ:')
    print('Это действие изменит данные группы на:')
    print('{} -> {}'.format(old_org, new_org))
    print('{} -> {}'.format(old_faculty, new_faculty))
    print('{} -> {}'.format(old_group, new_group))

    if confirm():
        access_token, refresh_token = login(ip, port, username, password)
        tag = update_group(
            ip=ip,
            port=port,
            access_token=access_token,
            old_org=old_org,
            old_faculty=old_faculty,
            old_group=old_group,
            new_org=new_org,
            new_faculty=new_faculty,
            new_group=new_group
        )
        print('Группа обновлена')
        print('Новый тег группы: {}'.format(tag))
    else:
        print('Действие отменено')


def menu_update_groups_number(ip, port, username, password, login_attempt=10):
    print('ВНИМАНИЕ:')
    print('Это действие изменит данные групп')

    update_list = []
    delete_list = []
    skip_list = []

    if confirm():
        org_structure = create_org_structure(
            ip,
            port,
            username,
            password)

        access_token, refresh_token = login(ip, port, username, password)

        for org in org_structure.keys():
            for faculty in org_structure[org].keys():
                for group in org_structure[org][faculty]:
                    change_flg = False
                    delete_flg = False

                    new_group = ''

                    group_data = group.split('-')
                    if len(group_data) == 2:
                        result = re.match(r"(\d{1,3})(\w*)", group_data[1])

                        if result:
                            items = result.groups()

                            if len(items) == 2 and items[0].isdigit() and 2 <= len(items[0]) <= 3:
                                if len(items[0]) == 2:
                                    next_semester_number = int(items[0][0]) + 1
                                    group_number = items[0][1]
                                elif len(items[0]) == 3:
                                    next_semester_number = int(items[0][0:1]) + 1
                                    group_number = items[0][2]

                                new_group = '{}-{}{}{}'.format(group_data[0],
                                                               next_semester_number, group_number, items[1])

                                # Бакалавриат
                                if items[1] == 'Б' and next_semester_number <= 8:
                                    change_flg = True
                                elif items[1] == 'Б' and next_semester_number > 8:
                                    delete_flg = True

                                # Магистратура
                                if items[1] == 'М' and next_semester_number <= 4:
                                    change_flg = True
                                elif items[1] == 'М' and next_semester_number > 4:
                                    delete_flg = True

                                # Специалитет
                                if items[1] == '' and next_semester_number <= 12:
                                    change_flg = True
                                elif items[1] == '' and next_semester_number > 12:
                                    delete_flg = True
                    if change_flg:
                        tag = None

                        for attempt in range(login_attempt):
                            try:
                                tag = update_group(
                                    ip=ip,
                                    port=port,
                                    access_token=access_token,
                                    old_org=org,
                                    old_faculty=faculty,
                                    old_group=group,
                                    new_org=org,
                                    new_faculty=faculty,
                                    new_group=new_group
                                )
                                pass
                            except AccessDeniedError:
                                access_token, refresh_token = login(ip, port, username, password)
                                continue
                            break

                        print('CHANGED: {} {} {} -> {} new tag: {}'.format(org, faculty, group, new_group, tag))
                        update_list.append([org, faculty, group])
                    elif delete_flg:
                        print('CAN BE DELETED: {} {} {}'.format(org, faculty, group))
                        delete_list.append([org, faculty, group])
                    else:
                        print('SKIPPED: {} {} {}'.format(org, faculty, group))
                        skip_list.append([org, faculty, group])

    print('Названия обновлённых групп ({} групп) сохранены в файл updated_groups.json'.format(
        len(update_list)))
    with open('updated_groups.json', 'w') as outfile:
        json.dump(update_list, outfile, indent=4, sort_keys=True)

    print('Названия групп, которые могут быть удалены ({} групп), сохранены в файл can_be_deleted_groups.json'.format(
        len(delete_list)))
    with open('can_be_deleted_groups.json', 'w') as outfile:
        json.dump(delete_list, outfile, indent=4, sort_keys=True)

    print('Названия пропущенных групп ({} групп) сохранены в файл skipped_groups.json'.format(
        len(skip_list)))
    with open('skipped_groups.json', 'w') as outfile:
        json.dump(skip_list, outfile, indent=4, sort_keys=True)
