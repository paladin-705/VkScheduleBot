import vk

session = vk.Session()
api = vk.API(session, v='5.80')


def send_auto_posting_message(user_id, token, message, attachment=""):
    try:
        api.messages.send(access_token=token,
                          from_id=str(user_id),
                          peer_id=str(user_id),
                          message=message,
                          attachment=attachment)
    except:
        pass


def send_error_message(admin_vk_id, token, message, attachment=""):
    try:
        if admin_vk_id:
            api.messages.send(access_token=token,
                              user_id=str(admin_vk_id),
                              message=message,
                              attachment=attachment)
    except:
        pass
