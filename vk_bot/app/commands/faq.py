from flask import current_app as app
from app import command_system
from app.helpers import get_other_keyboard
from app.messages import faq_message

# Статистика
from app.statistic import track


def faq(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'faq')

    return faq_message, '', get_other_keyboard()


faq_command = command_system.Command()

faq_command.keys = ['faq', '/faq']
faq_command.description = 'FAQ'
faq_command.process = faq
