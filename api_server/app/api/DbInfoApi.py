from flask import make_response, jsonify
from flask.views import MethodView
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.api import bp
from app.api.helpers import del_end_space
from app.scheduledb import ScheduleDB


class DbInfoApi(MethodView):
    # /api/<organization>
    error = {
        "getFail": {
            "error_code": 101,
            "message": "Select organizations failed"
        },
        "deleteFail": {
            "errorCode": 102,
            "errorMessage": "Delete organizations failed"
        }
    }

    @jwt_required
    def get(self):
        # Return the faculties list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_organizations()

            if db_data is None:
                return make_response(jsonify(self.error["getFail"]), 400)

            data = []
            for row in db_data:
                data.append(del_end_space(row[0]))

            return make_response(jsonify(data), 200)
        except BaseException as e:
            print(str(e))
            return make_response(jsonify(self.error["getFail"]), 400)

    @jwt_required
    def delete(self):
        # Delete the entire organizations
        try:
            with ScheduleDB(app.config) as db:
                db.delete_all_organizations()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify(self.error["deleteFail"]), 400)

bp.add_url_rule('/', view_func=DbInfoApi.as_view('db_info__api'))
