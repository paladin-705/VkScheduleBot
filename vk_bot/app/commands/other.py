from flask import current_app as app
from app import command_system
from app.helpers import get_other_keyboard
from app.messages import other_message

# Статистика
from app.statistic import track


def other(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'other')

    return other_message, '', get_other_keyboard()


other_command = command_system.Command()

other_command.keys = ['прочее', '/other', 'other']
other_command.description = 'Прочее'
other_command.process = other
