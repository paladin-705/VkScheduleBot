from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

import os

app = Flask(__name__)

app.config.from_pyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'), silent=True)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api/v1')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
