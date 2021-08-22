from flask import make_response, jsonify, request
from flask.views import MethodView
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.api import bp
from app.api.helpers import del_end_space
from app.scheduledb import ScheduleDB


class ExamsApi(MethodView):
    # /api/<organization>/<faculty>/<group>/exams
    error = {

        "getFail": {
            "error_code": 601,
            "message": "Select exams failed"
        },
        "deleteFail": {
            "errorCode": 602,
            "errorMessage": "Delete exams failed"
        },
        "postFail": {
            "error_code": 603,
            "message": "Create exams failed"
        },
        "postFail_empty": {
            "error_code": 604,
            "message": "Empty data"
        },
        "unknownGroup": {
            "error_code": 605,
            "message": "Unknown group"
        }
    }

    def get(self, organization, faculty, group):
        # Return the exams list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

            if db_data is None:
                return make_response(jsonify(self.error["unknownGroup"]), 400)

            tag = db_data[1]

            with ScheduleDB(app.config) as db:
                schedule = db.get_exams(tag)

            data = []
            for row in schedule:
                data.append({
                    'day': row[0],
                    'title': del_end_space(row[1]),
                    'classroom': del_end_space(row[2]),
                    'lecturer': del_end_space(row[3])
                })

            return make_response(jsonify(data), 200)
        except BaseException as e:
            app.logger.warning('ExamsApi get: {}'.format(str(e)))
            return make_response(jsonify(self.error["getFail_unknown"]), 400)

    @jwt_required()
    def post(self, organization, faculty, group):
        # Add exams to DB
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

            if db_data is None:
                return make_response(jsonify(self.error["unknownGroup"]), 400)

            tag = db_data[1]
            body = request.get_json().get('data', None)

            if body is None:
                return make_response(jsonify(self.error["postFail_empty"]), 400)

            answer = {'failed': []}
            with ScheduleDB(app.config) as db:
                for exam in body:
                    # Обязательные параметры запроса
                    day = exam.get('day', None)
                    title = exam.get('title', None)

                    # Необязательные параметры
                    classroom = exam.get('classroom', None)
                    lecturer = exam.get('lecturer', None)

                    if day is None or  title is None:
                        answer['failed'].append(exam)
                        continue
                    else:
                        if not db.add_exam(tag, title, classroom, lecturer, day):
                            answer['failed'].append(exam)
            return make_response(jsonify(answer), 200)
        except BaseException as e:
            app.logger.warning('ExamsApi post: {}'.format(str(e)))
            return make_response(jsonify(self.error["postFail"]), 400)

    @jwt_required()
    def delete(self, organization, faculty, group):
        # Delete the entire exams
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

            if db_data is None:
                return make_response(jsonify(self.error["unknownGroup"]), 400)

            tag = db_data[1]

            with ScheduleDB(app.config) as db:
                db.delete_exams(tag)

            return make_response(jsonify({}), 200)
        except BaseException as e:
            app.logger.warning('ExamsApi delete: {}'.format(str(e)))
            return make_response(jsonify(self.error["deleteFail"]), 400)


bp.add_url_rule('/<organization>/<faculty>/<group>/exams', view_func=ExamsApi.as_view('exams_api'))
