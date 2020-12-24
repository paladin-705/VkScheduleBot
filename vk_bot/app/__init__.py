from flask import Flask, request, json
from logging.config import dictConfig
from app import messageHandler
import os
from app import vkapi

app = Flask(__name__)

app.config.from_pyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'), silent=True)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)-15s] [ %(levelname)s ] in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': app.config['LOG_DIR_PATH'] + 'vk_bot.log',
        'formatter': 'default',
        'maxBytes': 4096,
        'backupCount': 5
    }},
    'root': {
        'level': 'WARNING',
        'handlers': ['file']
    }
})


@app.route(app.config['FLASK_ROUTE_PATH'], methods=['POST'])
def processing():
    try:
        data = json.loads(request.data)
        if 'type' not in data.keys():
            return 'not vk'
        if data['type'] == 'confirmation':
            return app.config['CONFIRMATION_TOKEN']
        elif data['type'] == 'message_new':
            messageHandler.create_answer(data['object'])
            return 'ok'
        elif data['type'] == 'message_deny':
            messageHandler.message_deny_handler(data['object'])
            return 'ok'
    except BaseException as e:
        app.logger.warning('processing: {}\n{}'.format(str(e), str(data)))
        vkapi.send_error_message(app.config['TOKEN'], '__init__.py: ' + str(e) + '\n' + str(data))
        return 'ok'
