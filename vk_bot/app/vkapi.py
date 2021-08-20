from flask import current_app as app
import vk
import time

session = vk.Session()
api = vk.API(session, v='5.131')


def send_message(data, token, message, attachment='', keyboard=''):
    try:
        random_id = int(time.time()*1000) & 0xffffffff
        
        if keyboard != '':
            api.messages.send(access_token=token,
                              from_id=str(data['from_id']),
                              peer_id=str(data['peer_id']),
                              random_id=random_id,
                              message=message,
                              attachment=attachment,
                              keyboard=keyboard)
        else:
            api.messages.send(access_token=token,
                              from_id=str(data['from_id']),
                              peer_id=str(data['peer_id']),
                              random_id=random_id,
                              message=message,
                              attachment=attachment)
    except BaseException as e:
        app.logger.warning('send_message: {}\n{}'.format(str(e), str(data)))


def send_auto_posting_message(user_id, token, message, attachment=""):
    try:
        random_id = int(time.time()*1000) & 0xffffffff
        
        api.messages.send(access_token=token,
                          from_id=str(user_id),
                          peer_id=str(user_id),
                          random_id=random_id,
                          message=message,
                          attachment=attachment)
    except BaseException as e:
        app.logger.warning('send_auto_posting_message: {}\n{}'.format(str(e), str(message)))


def send_error_message(token, message, attachment=""):
    try:
        random_id = int(time.time()*1000) & 0xffffffff
        
        if app.config['ADMIN_VK_ID']:
            api.messages.send(access_token=token,
                              user_id=str(app.config['ADMIN_VK_ID']),
                              random_id=random_id,
                              message=message,
                              attachment=attachment)
    except BaseException as e:
        app.logger.warning('send_error_message: {}\n{}'.format(str(e), str(message)))
