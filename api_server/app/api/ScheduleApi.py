from flask import make_response, jsonify, request
from flask.views import MethodView
from flask import current_app as app
from flask_jwt_extended import jwt_required

from app.api import bp
from app.api.helpers import del_end_space
from app.scheduledb import ScheduleDB


class ScheduleApi(MethodView):
    # /api/<organization>/<faculty>/<group>/schedule
    error = {

        "getFail": {
            "error_code": 501,
            "message": "Select schedule failed"
        },
        "deleteFail": {
            "errorCode": 502,
            "errorMessage": "Delete schedule failed"
        },
        "postFail": {
            "error_code": 503,
            "message": "Create schedule failed"
        },
        "postFail_empty": {
            "error_code": 504,
            "message": "Empty data"
        },
        "unknownGroup": {
            "error_code": 505,
            "message": "Unknown group"
        }
    }

    def get(self, organization, faculty, group):
        # Return the schedule list
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

            if db_data is None:
                return make_response(jsonify(self.error["unknownGroup"]), 400)

            tag = db_data[1]

            with ScheduleDB(app.config) as db:
                schedule = db.get_schedule(tag)

            data = []
            for row in schedule:
                data.append({
                    'day': del_end_space(row[7]),
                    'number': row[0],
                    'week_type': row[3],
                    'title': del_end_space(row[1]),
                    'classroom': del_end_space(row[2]),
                    'lecturer': del_end_space(row[6]),
                    'time_start': str(row[4])[:5],
                    'time_end': str(row[5])[:5]
                })

            return make_response(jsonify(data), 200)
        except BaseException as e:
            app.logger.warning('ScheduleApi get: {}'.format(str(e)))
            return make_response(jsonify(self.error["getFail"]), 400)

    @jwt_required()
    def post(self, organization, faculty, group):
        # Add schedule to DB
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
                for lecture in body:
                    # Обязательные параметры запроса
                    day = lecture.get('day', None)
                    number = lecture.get('number', None)
                    week_type_text = lecture.get('week_type', None)
                    title = lecture.get('title', None)

                    if week_type_text == 'odd':
                        week_type = 0
                    elif week_type_text == 'even':
                        week_type = 1
                    elif week_type_text == 'all':
                        week_type = 2
                    else:
                        week_type = None

                    # Необязательные параметры
                    classroom = lecture.get('classroom', None)
                    time_start = lecture.get('time_start', None)
                    time_end = lecture.get('time_end', None)
                    lecturer = lecture.get('lecturer', None)

                    if day is None or number is None or week_type is None or title is None:
                        answer['failed'].append(lecture)
                        continue
                    else:
                        if not db.add_lesson(tag, day, number, week_type,
                                             time_start, time_end, title, classroom, lecturer):
                            answer['failed'].append(lecture)
            return make_response(jsonify(answer), 200)
        except BaseException as e:
            app.logger.warning('ScheduleApi post: {}'.format(str(e)))
            return make_response(jsonify(self.error["postFail"]), 400)

    @jwt_required()
    def delete(self, organization, faculty, group):
        # Delete the entire schedule
        try:
            with ScheduleDB(app.config) as db:
                db_data = db.get_group(organization, faculty, group)

            if db_data is None:
                return make_response(jsonify(self.error["unknownGroup"]), 400)

            tag = db_data[1]

            with ScheduleDB(app.config) as db:
                db.delete_schedule(tag)

            return make_response(jsonify({}), 200)
        except BaseException as e:
            app.logger.warning('ScheduleApi delete: {}'.format(str(e)))
            return make_response(jsonify(self.error["deleteFail"]), 400)


bp.add_url_rule('/<organization>/<faculty>/<group>/schedule', view_func=ScheduleApi.as_view('schedule_api'))
