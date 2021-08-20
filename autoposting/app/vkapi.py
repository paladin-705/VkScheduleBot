import vk
import time

session = vk.Session()
api = vk.API(session, v='5.131')


def send_auto_posting_message(user_id, token, message, attachment=""):
    try:
        random_id = int(time.time()) & 0xffffffff
        
        api.messages.send(access_token=token,
                          from_id=str(user_id),
                          peer_id=str(user_id),
                          random_id=random_id,
                          message=message,
                          attachment=attachment)
    except BaseException as e:
        pass


def send_error_message(admin_vk_id, token, message, attachment=""):
    try:
        random_id = int(time.time()) & 0xffffffff
        
        if admin_vk_id:
            api.messages.send(access_token=token,
                              user_id=str(admin_vk_id),
                              random_id=random_id,
                              message=message,
                              attachment=attachment)
    except BaseException as e:
        pass
