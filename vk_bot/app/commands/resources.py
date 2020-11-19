from flask import current_app as app
from app import command_system
from app.helpers import get_other_keyboard
from app.messages import resources_message

# Статистика
from app.statistic import track


def resources(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'resources')

    return resources_message, '', get_other_keyboard()


resources_command = command_system.Command()

resources_command.keys = ['ресурсы', '/resources', 'resources']
resources_command.description = 'Ресурсы'
resources_command.process = resources
