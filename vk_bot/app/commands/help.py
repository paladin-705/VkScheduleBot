from flask import current_app as app
from app import command_system

# Статистика
from app.statistic import track


def help(uid, key, data=""):
    # Статистика
    track(app.config['STATISTIC_TOKEN'], uid, key, 'help')

    message = 'Список команд:\n'

    for c in command_system.command_list:
        message += '{}: {}\n\n'.format(c.keys[0], c.description)

    return message, '', ''


help_command = command_system.Command()

help_command.keys = ['помощь', 'команды', '/help', 'help']
help_command.description = 'Выводит информацию о боте и список доступных команд'
help_command.process = help
