from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from logging.config import dictConfig

import os

app = Flask(__name__)

app.config.from_pyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'), silent=True)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)-15s] [ %(levelname)s ] in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': app.config['LOG_DIR_PATH'] + 'vk_bot_api.log',
        'formatter': 'default',
        'maxBytes': 4096,
        'backupCount': 5
    }},
    'root': {
        'level': 'WARNING',
        'handlers': ['file']
    }
})

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api/v1')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
