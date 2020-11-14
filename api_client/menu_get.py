import json
from api import login
from api import (get_orgs, get_facultys, get_groups,
                 get_schedule, get_exams)
from menu_helpers import input_org_info


def create_org_structure(ip, port, username, password):
    access_token, refresh_token = login(ip, port, username, password)

    org_struct = {}
    o_res = get_orgs(ip, port, access_token)
    for org in o_res:
        org_struct[org] = {}

        f_res = get_facultys(ip, port, access_token, org)
        for faculty in f_res:
            org_struct[org][faculty] = get_groups(ip, port, access_token, org, faculty)
    return org_struct


def menu_get_org_structure(ip, port, username, password):
    org_structure = create_org_structure(
        ip,
        port,
        username,
        password)
    print('Структура групп в БД:')
    print(json.dumps(org_structure, indent=4, sort_keys=True, ensure_ascii=False))

    with open('org_structure.json', 'w') as outfile:
        json.dump(org_structure, outfile, indent=4, sort_keys=True)
    print('Структура групп сохранена в org_structure.json')


def menu_get_schedule(ip, port, username, password):
    org, faculty, group =  input_org_info()
    access_token, refresh_token = login(ip, port, username, password)
    schedule = get_schedule(ip, port, access_token, org, faculty, group)

    data = {
        org:{
            faculty:{
                group: schedule
            }
        }
    }
    print('Расписание занятий:')
    print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))

    with open('schedule.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print('Расписание занятий группы сохранено в schedule.json')


def menu_get_exams(ip, port, username, password):
    org, faculty, group =  input_org_info()
    access_token, refresh_token = login(ip, port, username, password)
    schedule = get_exams(ip, port, access_token, org, faculty, group)

    data = {
        org:{
            faculty:{
                group: schedule
            }
        }
    }
    print('Расписание экзаменов:')
    print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))

    with open('exams.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print('Расписание занятий группы сохранено в schedule.json')
