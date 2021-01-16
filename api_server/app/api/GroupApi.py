from flask import make_response, request, jsonify
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
        },
        "putFail_missing_json": {
            "error_code": 405,
            "message": "Missing json in request"
        },
        "putFail_missing_organization": {
            "error_code": 406,
            "message": "Missing new_organization parameter"
        },
        "putFail_missing_faculty": {
            "error_code": 407,
            "message": "Missing new_faculty parameter"
        },
        "putFail_missing_group": {
            "error_code": 408,
            "message": "Missing new_group parameter"
        },
        "putFail_unknown": {
            "error_code": 409,
            "message": "Change group failed"
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
    def put(self, organization, faculty, group):
        # Update the group
        try:
            if not request.is_json:
                return make_response(jsonify(self.error["putFail_missing_json"]), 400)

            new_organization = request.json.get('new_organization', None)
            new_faculty = request.json.get('new_faculty', None)
            new_group = request.json.get('new_group', None)

            if not new_organization:
                return make_response(jsonify(self.error["putFail_missing_organization"]), 400)
            if not new_faculty:
                return make_response(jsonify(self.error["putFail_missing_faculty"]), 400)
            if not new_group:
                return make_response(jsonify(self.error["putFail_missing_group"]), 400)

            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

                if db_data is None:
                    return make_response(jsonify(self.error["putFail_unknown"]), 400)

                old_tag = db_data[1]

                if old_tag is not None:
                    new_tag = db.update_organization(new_organization, new_faculty, new_group, old_tag)

                    if new_tag is not None:
                        return make_response(jsonify(new_tag), 200)
                    else:
                        return make_response(jsonify(self.error["putFail_unknown"]), 400)
                else:
                    return make_response(jsonify(self.error["putFail_unknown"]), 400)
        except BaseException as e:
            app.logger.warning('GroupApi put: {}'.format(str(e)))
            return make_response(jsonify(self.error["putFail_unknown"]), 400)

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
