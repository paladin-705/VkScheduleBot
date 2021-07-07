import json
import requests


class AccessDeniedError(Exception):
    def __init__(self, message):
        self.message = message


class ApiError(Exception):
    def __init__(self, message):
        self.message = message


class GroupAlreadyExistError(Exception):
    def __init__(self, message):
        self.message = message


def login(ip, port, username, password, timeout=120):
    data = {
        'username': username,
        'password': password
    }
    link = 'http://{}:{}/api/auth/login'.format(ip, port)
    res = requests.post(link, json=data, verify=False, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))

    answer = json.loads(res.text)
    return answer.get('access_token', None), answer.get('refresh_token', None)


def get_orgs(ip, port, access_token, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/'.format(ip, port)
    res = requests.get(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))
    return json.loads(res.text)


def get_facultys(ip, port, access_token, org, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}'.format(ip, port, org)
    res = requests.get(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))

    return json.loads(res.text)


def get_groups(ip, port, access_token, org, faculty, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}'.format(ip, port, org, faculty)
    res = requests.get(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))

    return json.loads(res.text)


def get_group_info(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}'.format(ip, port, org, faculty, group)
    res = requests.get(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))

    return json.loads(res.text)


def get_schedule(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}/schedule'.format(ip, port, org, faculty, group)
    res = requests.get(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))

    return json.loads(res.text)


def get_exams(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}/exams'.format(ip, port, org, faculty, group)
    res = requests.get(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))

    return json.loads(res.text)


def add_group(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}'.format(ip, port, org, faculty, group)
    res = requests.post(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            code = json.loads(res.text).get('error_code', None)
            if code == 403:
                raise GroupAlreadyExistError(str(res.text))
            else:
                raise ApiError(str(res.text))
    return json.loads(res.text)


def add_schedule(ip, port, access_token, org, faculty, group, schedule, timeout=120):
    data = {'data': schedule}
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}/schedule'.format(ip, port, org, faculty, group)
    res = requests.post(link, headers={'Authorization': header}, json=data, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))
    return json.loads(res.text)


def add_exams(ip, port, access_token, org, faculty, group, schedule, timeout=120):
    data = {'data': schedule}
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}/exams'.format(ip, port, org, faculty, group)
    res = requests.post(link, headers={'Authorization': header}, json=data, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))
    return json.loads(res.text)


def update_group(ip, port, access_token,
                 old_org, old_faculty, old_group,
                 new_org, new_faculty, new_group,
                 timeout=120):
    data = {
        'new_organization': new_org,
        'new_faculty': new_faculty,
        'new_group': new_group
    }
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}'.format(ip, port, old_org, old_faculty, old_group)
    res = requests.put(link, headers={'Authorization': header}, json=data, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))
    return json.loads(res.text)


def delete_all_orgs(ip, port, access_token, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/'.format(ip, port)
    res = requests.delete(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))


def delete_org(ip, port, access_token, org, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}'.format(ip, port, org)
    res = requests.delete(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))


def delete_faculty(ip, port, access_token, org, faculty, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}'.format(ip, port, org, faculty)
    res = requests.delete(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))


def delete_group(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}'.format(ip, port, org, faculty, group)
    res = requests.delete(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))


def delete_group_schedule(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}/schedule'.format(ip, port, org, faculty, group)
    res = requests.delete(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))


def delete_group_exams(ip, port, access_token, org, faculty, group, timeout=120):
    header = 'Bearer {}'.format(access_token)
    link = 'http://{}:{}/api/v1/{}/{}/{}/exams'.format(ip, port, org, faculty, group)
    res = requests.delete(link, headers={'Authorization': header}, timeout=timeout)

    if res.status_code != 200:
        if res.status_code == 401:
            raise AccessDeniedError(str(res.text))
        else:
            raise ApiError(str(res.text))
