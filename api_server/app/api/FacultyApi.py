from flask import make_response, jsonify
from flask.views import MethodView
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.api import bp
from app.api.helpers import del_end_space
from app.scheduledb import ScheduleDB


class FacultyApi(MethodView):
    # /api/<organization>/<faculty>
    error = {
        "getFail": {
            "error_code": 301,
            "message": "Select faculty failed"
        },
        "deleteFail": {
            "errorCode": 302,
            "errorMessage": "Delete faculty failed"
        }
    }

    @jwt_required
    def get(self, organization, faculty):
        # Return the groups list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group_list(organization, faculty)

            if db_data is None:
                return make_response(jsonify(self.error["getFail"]), 400)

            data = []
            for row in db_data:
                data.append(del_end_space(row[0]))

            return make_response(jsonify(data), 200)
        except:
            return make_response(jsonify(self.error["getFail"]), 400)

    @jwt_required
    def delete(self, organization, faculty):
        # Delete the entire organizations
        try:
            with ScheduleDB(app.config) as db:
                db.delete_faculty(organization, faculty)
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify(self.error["deleteFail"]), 400)

bp.add_url_rule('/<organization>/<faculty>', view_func=FacultyApi.as_view('faculty_api'))
