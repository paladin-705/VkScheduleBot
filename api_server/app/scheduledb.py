from flask import current_app as app
import hashlib
import psycopg2

organization_field_length = 15
faculty_field_length = 10
group_field_length = 5


class ScheduleDB:
    def __init__(self, config):
        self.con = psycopg2.connect(
            dbname=config["SCHEDULE_DB_NAME"],
            user=config["SCHEDULE_DB_USER"],
            password=config["SCHEDULE_DB_PASSWORD"],
            host=config["SCHEDULE_DB_HOST"])
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.commit()
        self.con.close()

    @staticmethod
    def create_tag(organization, faculty, group):
        org_hash = hashlib.sha256(organization.encode('utf-8')).hexdigest()
        faculty_hash = hashlib.sha256(faculty.encode('utf-8')).hexdigest()
        group_hash = hashlib.sha256(group.encode('utf-8')).hexdigest()
        return org_hash[:organization_field_length] + \
               faculty_hash[:faculty_field_length] + \
               group_hash[:group_field_length]

    def add_lesson(self, tag, day, number, week_type, time_start, time_end, title, classroom, lecturer):
        try:
            self.cur.execute('INSERT INTO schedule(tag, day, "number", type, "startTime", "endTime", \
                             title, classroom, lecturer) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                             (tag, day, number, week_type, time_start, time_end, title, classroom, lecturer))
            self.con.commit()
            return True
        except BaseException as e:
            app.logger.warning('Add to schedule failed. Error: {0}. Data:\
                            tag={1},\
                            day={2},\
                            number={3},\
                            week_type={4},\
                            time_start={5},\
                            time_end={6},\
                            title={7},\
                            classroom={8},\
                            lecturer={9}'.format(
                str(e), tag, day, number, week_type, time_start, time_end, title, classroom, lecturer))
            return False

    def add_exam(self, tag, title, classroom, lecturer, day):
        try:
            self.cur.execute("INSERT INTO examinations(tag, title, classroom, lecturer, day) "
                             "VALUES(%s,%s,%s,%s,to_date(%s, 'DD.MM.YYYY'));",
                             (tag, title, classroom, lecturer, day))
            self.con.commit()
            return tag
        except BaseException as e:
            app.logger.warning("Add exam failed. Error: {0}. Data:\
                            tag={1},\
                            title={2},\
                            classroom={3},\
                            lecturer={4},\
                            day={5}".format(str(e), tag, title, classroom, lecturer, day))
            return None

    def add_organization(self, organization, faculty, group):
        tag = self.create_tag(organization, faculty, group)

        try:
            self.cur.execute("INSERT INTO organizations(organization, faculty, studgroup, tag) VALUES(%s,%s,%s,%s);",
                             (organization, faculty, group, tag))
            self.con.commit()
            return tag
        except BaseException as e:
            app.logger.warning("Add organization failed. Error: {0}. Data:\
                            organization={1},\
                            faculty={2},\
                            group={3},\
                            tag={4}".format(str(e), organization, faculty, group, tag))
            return None

    def get_exams(self, tag):
        exams = None
        try:
            self.cur.execute("SELECT day, title, classroom, lecturer FROM examinations "
                             "WHERE tag = (%s) ORDER BY day", (tag, ))
            exams = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select exams failed. Error: {0}. Data: tag={1}'.format(str(e), tag))
            raise e
        finally:
            return exams

    def get_schedule(self, tag):
        data = None
        try:
            self.cur.execute('SELECT "number", title, classroom, type, "startTime", "endTime", lecturer, day FROM schedule \
                                WHERE tag = (%s) ORDER BY day ASC, number ASC', (tag, ))
            data = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select schedule failed. Error: {0}. Data: tag={1}'.format(
                str(e), tag))
            raise Exception
        finally:
            return data

    def get_organizations(self):
        organizations = None
        try:
            self.cur.execute("SELECT DISTINCT ON (organization) organization, tag FROM organizations "
                             "ORDER BY organization")
            organizations = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select organization failed. Error: {0}'.format(str(e)))
            raise e
        finally:
            return organizations

    def get_faculty(self, organization):
        faculties = None
        try:
            self.cur.execute("SELECT DISTINCT ON (faculty) faculty, tag FROM organizations "
                             "WHERE organization = %s ORDER BY faculty", (organization,))
            faculties = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select faculty failed. Error: {0}. Data: organization={1}'.format(
                str(e), organization))
            raise e
        finally:
            return faculties

    def get_group_list(self, organization, faculty):
        group = None
        try:
            self.cur.execute("SELECT DISTINCT ON (studgroup) studgroup, tag FROM organizations "
                             "WHERE organization = %s AND faculty = %s ORDER BY studgroup",
                             (organization, faculty))
            group = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select group failed. Error: {0}. Data: organization={1} faculty={2}'.format(
                str(e), organization, faculty))
            raise e
        finally:
            return group

    def get_group(self, organization, faculty, group):
        data = None
        try:
            self.cur.execute("SELECT studgroup, tag FROM organizations "
                             "WHERE organization = %s AND faculty = %s AND studgroup = %s",
                             (organization, faculty, group))
            data = self.cur.fetchone()
        except BaseException as e:
            app.logger.warning('Select group failed. Error: {0}. '
                                'Data: organization={1} faculty={2} group={3}'.format(
                str(e), organization, faculty, group))
            raise e
        finally:
            return data

    def delete_all_organizations(self):
        try:
            self.cur.execute("DELETE FROM organizations")
        except BaseException as e:
            app.logger.warning('Delete all organization failed. Error: {0}'.format(str(e)))
            raise e

    def delete_organization(self, organization):
        try:
            self.cur.execute("DELETE FROM organizations WHERE organization = %s", (organization,))
        except BaseException as e:
            app.logger.warning('Delete organization failed. Error: {0}. Data: organization={1}'.format(
                str(e), organization))
            raise e

    def delete_faculty(self, organization, faculty):
        try:
            self.cur.execute("DELETE FROM organizations WHERE organization = %s AND faculty = %s",
                             (organization, faculty))
        except BaseException as e:
            app.logger.warning('Delete faculty failed. Error: {0}. Data: organization={1} faculty={2}'.format(
                str(e), organization, faculty))
            raise e

    def delete_group(self, organization, faculty, group):
        try:
            self.cur.execute("DELETE FROM organizations WHERE organization = %s AND faculty = %s AND studgroup = %s",
                             (organization, faculty, group))
        except BaseException as e:
            app.logger.warning('Delete group failed. Error: {0}. Data: organization={1} faculty={2} group ={3}'.format(
                str(e), organization, faculty, group))
            raise e

    def delete_schedule(self, tag):
        try:
            self.cur.execute("DELETE FROM schedule WHERE tag = (%s)", (tag,))
        except BaseException as e:
            app.logger.warning('Delete schedule failed. Error: {0}. Data: tag={1}'.format(
                str(e), tag))
            raise e

    def delete_exams(self, tag):
        try:
            self.cur.execute("DELETE FROM examinations WHERE tag = (%s)", [str(tag)])
        except BaseException as e:
            app.logger.warning('Delete exams failed. Error: {0}. Data: tag={1}'.format(str(e), tag))
            raise e
