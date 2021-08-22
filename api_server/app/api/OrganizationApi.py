from flask import make_response, jsonify
from flask.views import MethodView
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.api import bp
from app.api.helpers import del_end_space
from app.scheduledb import ScheduleDB


class OrganizationApi(MethodView):
    # /api/<organization>
    error = {
        "getFail": {
            "error_code": 201,
            "message": "Select organization failed"
        },
        "deleteFail": {
            "errorCode": 202,
            "errorMessage": "Delete organization failed"
        }
    }

    def get(self, organization):
        # Return the faculties list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_faculty(organization)

            if db_data is None:
                return make_response(jsonify(self.error["getFail"]), 400)

            data = []
            for row in db_data:
                data.append(del_end_space(row[0]))

            return make_response(jsonify(data), 200)
        except BaseException as e:
            app.logger.warning('OrganizationApi get: {}'.format(str(e)))
            return make_response(jsonify(self.error["getFail"]), 400)

    @jwt_required()
    def delete(self, organization):
        # Delete the entire organizations
        try:
            with ScheduleDB(app.config) as db:
                db.delete_organization(organization)
            return make_response(jsonify({}), 200)
        except BaseException as e:
            app.logger.warning('OrganizationApi delete: {}'.format(str(e)))
            return make_response(jsonify(self.error["deleteFail"]), 400)


bp.add_url_rule('/<organization>', view_func=OrganizationApi.as_view('organization_api'))
