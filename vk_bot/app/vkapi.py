from flask import current_app as app
import vk

session = vk.Session()
api = vk.API(session, v='5.131')


def send_message(data, token, message, attachment='', keyboard=''):
    try:
        if keyboard != '':
            api.messages.send(access_token=token,
                              from_id=str(data['from_id']),
                              peer_id=str(data['peer_id']),
                              message=message,
                              attachment=attachment,
                              keyboard=keyboard)
        else:
            api.messages.send(access_token=token,
                              from_id=str(data['from_id']),
                              peer_id=str(data['peer_id']),
                              message=message,
                              attachment=attachment)
    except BaseException as e:
        app.logger.warning('send_message: {}\n{}'.format(str(e), str(data)))


def send_auto_posting_message(user_id, token, message, attachment=""):
    try:
        api.messages.send(access_token=token,
                          from_id=str(user_id),
                          peer_id=str(user_id),
                          message=message,
                          attachment=attachment)
    except BaseException as e:
        app.logger.warning('send_auto_posting_message: {}\n{}'.format(str(e), str(message)))


def send_error_message(token, message, attachment=""):
    try:
        if app.config['ADMIN_VK_ID']:
            api.messages.send(access_token=token,
                              user_id=str(app.config['ADMIN_VK_ID']),
                              message=message,
                              attachment=attachment)
    except BaseException as e:
        app.logger.warning('send_error_message: {}\n{}'.format(str(e), str(message)))
