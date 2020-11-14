from flask import make_response, jsonify, request
from flask import current_app as app
from flask_jwt_extended import (
    create_access_token,create_refresh_token,
    jwt_refresh_token_required, get_jwt_identity
)

from app import bcrypt
from app.auth import bp
from app.ApiSettingsDB import ApiSettingsDB

error = {
    "missing_json": {
        "error_code": 701,
        "message": "Missing json in request"
    },
    "missing_username": {
        "error_code": 702,
        "message": "Missing username parameter"
    },
    "missing_password": {
        "errorCode": 703,
        "errorMessage": "Missing password parameter"
    },
    "bad_login": {
        "errorCode": 704,
        "errorMessage": "Bad username or password"
    },
    "unknown_error": {
        "errorCode": 705,
        "errorMessage": "Unknown error"
    }
}


@bp.route('/login', methods=['POST'])
def login():
    try:
        if not request.is_json:
            return make_response(jsonify(error["missing_json"]), 400)

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return make_response(jsonify(error["missing_username"]), 400)
        if not password:
            return make_response(jsonify(error["missing_password"]), 400)

        with ApiSettingsDB(app.config) as db:
            user_info = db.get_user_info(username)

        if user_info is None:
            return make_response(jsonify(error["bad_login"]), 401)

        pw_hash = user_info[2]

        if not bcrypt.check_password_hash(pw_hash, password):
            return make_response(jsonify(error["bad_login"]), 401)

        ret = {
            'access_token': create_access_token(identity=username),
            'refresh_token': create_refresh_token(identity=username)
        }
        return make_response(jsonify(ret), 200)
    except:
        return make_response(jsonify(error["unknown_error"]), 400)


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return make_response(jsonify(ret), 200)
