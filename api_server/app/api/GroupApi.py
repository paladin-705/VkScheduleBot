from flask import make_response, jsonify
from flask.views import MethodView
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.api import bp
from app.scheduledb import ScheduleDB


class GroupApi(MethodView):
    # /api/<organization>/<faculty>/<group>
    error = {
        "getFail": {
            "error_code": 401,
            "message": "Select group failed"
        },
        "deleteFail": {
            "errorCode": 402,
            "errorMessage": "Delete group failed"
        },
        "postFail_exist": {
            "error_code": 403,
            "message": "Group already created"
        },
        "postFail_unknown": {
            "error_code": 404,
            "message": "Create group failed"
        }
    }

    @jwt_required
    def get(self, organization, faculty, group):
        # Return the groups list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

            if db_data is None:
                return make_response(jsonify(self.error["getFail"]), 400)

            tag = db_data[1]
            return make_response(jsonify(tag), 200)
        except BaseException as e:
            app.logger.warning('GroupApi get: {}'.format(str(e)))
            return make_response(jsonify(self.error["getFail"]), 400)

    @jwt_required
    def post(self, organization, faculty, group):
        # Return the groups list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

                if db_data is not None:
                    return make_response(jsonify(self.error["postFail_exist"]), 400)

                tag = db.add_organization(organization, faculty, group)

            if tag is not None:
                return make_response(jsonify(tag), 200)
            else:
                return make_response(jsonify(self.error["postFail_unknown"]), 400)
        except BaseException as e:
            app.logger.warning('GroupApi post: {}'.format(str(e)))
            return make_response(jsonify(self.error["postFail_unknown"]), 400)

    @jwt_required
    def delete(self, organization, faculty, group):
        # Delete the group
        try:
            with ScheduleDB(app.config) as db:
                db.delete_group(organization, faculty, group)
            return make_response(jsonify({}), 200)
        except BaseException as e:
            app.logger.warning('GroupApi delete: {}'.format(str(e)))
            return make_response(jsonify(self.error["deleteFail"]), 400)

bp.add_url_rule('/<organization>/<faculty>/<group>', view_func=GroupApi.as_view('group_api'))
