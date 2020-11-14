import json
import logging
import sys

from api import login
from api import get_group_info
from api import (add_group, add_schedule, add_exams)
from api import GroupAlreadyExistError, AccessDeniedError

from menu_helpers import input_org_info


def load_schedule(ip, port, username, password, json_data, login_attempt=10):
    logger = logging.getLogger('main-logger')
    logger.setLevel(logging.INFO)

    logFormatter = logging.Formatter('%(asctime)-15s [ %(levelname)s ] %(message)s')

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    # log_file = 'main-{}.log'.format(strftime('%Y-%m-%d-%H.%M.%S'))
    # fileHandler = logging.FileHandler(mode='a', filename=log_file)
    # fileHandler.setFormatter(logFormatter)
    # logger.addHandler(fileHandler)

    access_token, refresh_token = login(ip, port, username, password)
    failed_data = {}
    failed_data_len = 0
    for org in json_data:
        failed_data[org] = {}
        for faculty in json_data[org]:
            failed_data[org][faculty] = {}
            for group in json_data[org][faculty]:
                for attempt in range(login_attempt):
                    logger.info('Load {} | {} | {}'.format(org, faculty, group))
                    try:
                        add_group(ip, port, access_token, org, faculty, group)
                        logger.info('Add group data')
                    except GroupAlreadyExistError:
                        get_group_info(ip, port, access_token, org, faculty, group)
                        logger.info('Get group data')
                    except AccessDeniedError:
                        access_token, refresh_token = login(ip, port, username, password)
                        logger.info('Refresh access token')
                        continue
                    break
                logger.info('Load schedule')
                schedule = json_data[org][faculty][group]
                for attempt in range(login_attempt):
                    try:
                        result = add_schedule(ip, port, access_token, org, faculty, group, schedule)
                    except AccessDeniedError:
                        access_token, refresh_token = login(ip, port, username, password)
                        continue
                    break
                failed = result['failed']
                if len(failed) != 0:
                    failed_data[org][faculty][group] = failed
                    failed_data_len += len(failed)
                logger.info('Failed: {}'.format(len(failed)))
    return failed_data, failed_data_len


def load_exams(ip, port, username, password, json_data, login_attempt=10):
    logger = logging.getLogger('main-logger')
    logger.setLevel(logging.INFO)

    logFormatter = logging.Formatter('%(asctime)-15s [ %(levelname)s ] %(message)s')

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    # log_file = 'main-{}.log'.format(strftime('%Y-%m-%d-%H.%M.%S'))
    # fileHandler = logging.FileHandler(mode='a', filename=log_file)
    # fileHandler.setFormatter(logFormatter)
    # logger.addHandler(fileHandler)

    access_token, refresh_token = login(ip, port, username, password)
    failed_data = {}
    failed_data_len = 0
    for org in json_data:
        failed_data[org] = {}
        for faculty in json_data[org]:
            failed_data[org][faculty] = {}
            for group in json_data[org][faculty]:
                for attempt in range(login_attempt):
                    logger.info('Load {} | {} | {}'.format(org, faculty, group))
                    try:
                        add_group(ip, port, access_token, org, faculty, group)
                        logger.info('Add group data')
                    except GroupAlreadyExistError:
                        get_group_info(ip, port, access_token, org, faculty, group)
                        logger.info('Get group data')
                    except AccessDeniedError:
                        access_token, refresh_token = login(ip, port, username, password)
                        logger.info('Refresh access token')
                        continue
                    break
                logger.info('Load exams')
                schedule = json_data[org][faculty][group]
                for attempt in range(login_attempt):
                    try:
                        result = add_exams(ip, port, access_token, org, faculty, group, schedule)
                    except AccessDeniedError:
                        access_token, refresh_token = login(ip, port, username, password)
                        continue
                    break
                failed = result['failed']
                if len(failed) != 0:
                    failed_data[org][faculty][group] = failed
                    failed_data_len += len(failed)
                logger.info('Failed: {}'.format(len(failed)))
    return failed_data, failed_data_len


def menu_add_schedule(ip, port, username, password):
    file_name = input('Введите имя json файла: ')

    with open(file_name) as json_file:
        json_data = json.load(json_file)

    failed_data, failed_data_len = load_schedule(ip, port, username, password, json_data)

    if failed_data_len == 0:
        print('Все данные загружены успешно')
    else:
        with open('failed_schedule.json', 'w') as outfile:
            json.dump(failed_data, outfile, indent=4, sort_keys=True)
        print('Часть данных не удалось загрузить')
        print('Незагруженные данные сохранены в файл failed_schedule.json')


def menu_add_exams(ip, port, username, password):
    pass
    file_name = input('Введите имя json файла: ')

    with open(file_name) as json_file:
        json_data = json.load(json_file)

    failed_data, failed_data_len = load_exams(ip, port, username, password, json_data)

    if failed_data_len == 0:
        print('Все данные загружены успешно')
    else:
        with open('failed_schedule.json', 'w') as outfile:
            json.dump(failed_data, outfile, indent=4, sort_keys=True)
        print('Часть данных не удалось загрузить')
        print('Незагруженные данные сохранены в файл failed_schedule.json')


def menu_add_group(ip, port, username, password):
    org, faculty, group = input_org_info()
    access_token, refresh_token = login(ip, port, username, password)
    tag = add_group(ip, port, access_token, org, faculty, group)
    print('Группа добавлена')
    print('Тег группы: {}'.format(tag))