from flask import current_app as app
import hashlib
import psycopg2
from datetime import datetime

organization_field_length = 15
faculty_field_length = 10
group_field_length = 5


class ScheduleDB:
    def __init__(self, config):
        self.con = psycopg2.connect(
            dbname=config["DB_NAME"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            host=config["DB_HOST"]
        )
        self.cur = self.con.cursor()

        self.user_tag = config["DB_USER_TAG"]

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

    def add_report(self, cid, report):
        try:
            self.cur.execute('INSERT INTO reports (type, user_id, report, date) VALUES(%s, %s, %s, %s)',
                             (self.user_tag, cid, report, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.con.commit()
            return True
        except BaseException as e:
            app.logger.warning('Add report failed. Error: {0}. Data: cid={1}, report={2}'.format(str(e), cid, report))
            return False

    def add_user(self, cid, name, username, tag):
        try:
            self.cur.execute('INSERT INTO users VALUES(%s,%s,%s,%s,%s,null,null)',
                             (self.user_tag, cid, name, username, tag))
            self.con.commit()
            return True
        except BaseException as e:
            app.logger.warning('Add user failed. Error: {0}. Data: cid={1}, name={2}, username={3}, tag={4}'.format(
                str(e), cid, name, username, tag))
            raise e

    def update_user(self, cid, name, username, tag):
        try:
            self.cur.execute('UPDATE users SET "scheduleTag" = (%s) WHERE id = (%s) AND type = (%s)',
                             (tag, cid, self.user_tag))
            self.con.commit()
            return True
        except BaseException as e:
            app.logger.warning('Update user failed. Error: {0}. Data: cid={1}, name={2}, username={3}, tag={4}'.format(
                str(e), cid, name, username, tag))
            raise e

    def find_user(self, cid):
        try:
            self.cur.execute('SELECT "scheduleTag" FROM users WHERE id = (%s) AND type = (%s)',
                             (cid, self.user_tag))
            return self.cur.fetchone()
        except BaseException as e:
            app.logger.warning('Select user failed. Error: {0}. Data: cid={1}'.format(str(e), cid))
            raise e

    def find_users_where(self, auto_posting_time=None, is_today=None):
        try:
            if auto_posting_time is not None and is_today is not None:
                self.cur.execute('SELECT id, "scheduleTag" FROM users '
                                 'WHERE auto_posting_time = %s AND is_today = %s  AND type = (%s)',
                                 (auto_posting_time, is_today, self.user_tag))
                return self.cur.fetchall()
            elif auto_posting_time is not None:
                self.cur.execute('SELECT id, "scheduleTag" FROM users WHERE auto_posting_time = %s AND type = (%s)',
                                 (auto_posting_time, self.user_tag))
                return self.cur.fetchall()
            elif is_today is not None:
                self.cur.execute('SELECT id, "scheduleTag" FROM users WHERE is_today = %s AND type = (%s)',
                                 (is_today, self.user_tag))
                return self.cur.fetchall()
            else:
                self.cur.execute('SELECT id, "scheduleTag" FROM users WHERE type = (%s)', [self.user_tag])
                return self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select users failed. Error: {0}. auto_posting_time={1}'.format(
                str(e), auto_posting_time))
            raise e

    def get_user_info(self, cid):
        try:
            self.cur.execute('SELECT organizations.organization, organizations.faculty, '
                             'organizations.studgroup, users.auto_posting_time, '
                             'users.is_today from organizations, users '
                             'where organizations.tag = (select "scheduleTag" '
                             'from users where id = (%s) and type = (%s)) '
                             'and users.id = (%s) and users.type = (%s)', (cid, self.user_tag, cid, self.user_tag))
            return self.cur.fetchone()
        except BaseException as e:
            app.logger.warning('Select user failed. Error: {0}. Data: cid={1}'.format(str(e), cid))
            raise e

    def get_exams(self, tag):
        exams = []
        try:
            self.cur.execute("SELECT day, title, classroom, lecturer "
                             "FROM examinations WHERE tag = (%s) ORDER BY day", [str(tag)])
            exams = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select exams failed. Error: {0}. Data: tag={1}'.format(str(e), tag))
            raise e
        finally:
            return exams

    def get_schedule(self, tag, day, week_type=-1):
        data = []
        try:
            if week_type != -1:
                self.cur.execute('SELECT number,title,classroom,type FROM schedule \
                            WHERE tag = (%s) AND day = (%s) AND (type = 2 OR type = %s) \
                            ORDER BY number, type ASC', (tag, day, week_type))
            else:
                self.cur.execute('SELECT number,title,classroom,type FROM schedule \
                            WHERE tag = (%s) AND day = (%s) ORDER BY number, type ASC', (tag, day))
            data = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select schedule failed. Error: {0}. Data: tag={1}, day={2}, week_type={3}'.format(
                str(e), tag, day, week_type))
            raise Exception
        finally:
            return data

    def get_lessons_time(self):
        time_arr = []
        try:
            self.cur.execute('SELECT DISTINCT "number", "startTime", "endTime" from schedule ORDER BY "number" ASC;')
            time_arr = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select lessons time failed. Error: {0}'.format(str(e)))
            raise e
        finally:
            return time_arr

    def get_organizations(self, tag=""):
        organizations = []
        try:
            self.cur.execute("SELECT DISTINCT ON (organization) organization, tag FROM organizations "
                             "WHERE tag LIKE %s ORDER BY organization", (str(tag) + '%',))
            organizations = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select schedule failed. Error: {0}. Data: tag={1}'.format(str(e), tag))
            raise e
        finally:
            return organizations

    def get_faculty(self, tag=""):
        faculties = []
        try:
            self.cur.execute("SELECT DISTINCT ON (faculty) faculty, tag FROM organizations "
                             "WHERE tag LIKE %s ORDER BY faculty", (str(tag) + '%',))
            faculties = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select schedule failed. Error: {0}. Data: tag={1}'.format(str(e), tag))
            raise e
        finally:
            return faculties

    def get_group(self, tag=""):
        group = []
        try:
            self.cur.execute("SELECT DISTINCT ON (studGroup) studGroup, tag FROM organizations "
                             "WHERE tag LIKE %s ORDER BY studGroup",
                             (str(tag) + '%',))
            group = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select group failed. Error: {0}. Data: tag={1}'.format(str(e), [tag]))
            raise e
        finally:
            return group

    def get_similar_organizations(self, org_name=""):
        org = []
        try:
            self.cur.execute('''
            SELECT tag,
            (organization || ' ' || faculty || ' ' || studgroup),
            similarity(lower(organization || ' ' || faculty || ' ' || studgroup), lower(%s))
            FROM organizations
            ORDER BY similarity(lower(organization || ' ' || faculty || ' ' || studgroup), lower(%s)) DESC LIMIT 5;''',
                             (org_name, org_name))
            org = self.cur.fetchall()
        except BaseException as e:
            app.logger.warning('Select similar organizations failed. '
                               'Error: {0}. Data: tag={1}'.format(str(e), [org_name]))
            raise e
        finally:
            return org

    def set_auto_post_time(self, cid, time, is_today):
        try:
            self.cur.execute('UPDATE users SET auto_posting_time = %s, is_today = %s \
            WHERE id = %s AND type = (%s)',
                             (time, is_today, cid, self.user_tag))
            self.con.commit()
            return True
        except BaseException as e:
            app.logger.warning('Set auto post time failed. Error: {0}. Data: cid={1}, auto_posting_time={2}'.format(
                str(e), cid, time))
            raise e

    def clear_tables(self):
        try:
            self.cur.execute('TRUNCATE users;')
            self.cur.execute('TRUNCATE organizations;')
            self.cur.execute('TRUNCATE schedule;')
            self.cur.execute('TRUNCATE reports;')
            self.con.commit()

            old_isolation_level = self.con.isolation_level
            self.con.set_isolation_level(0)

            self.cur.execute('VACUUM')
            self.con.commit()

            self.con.set_isolation_level(old_isolation_level)

            return True
        except BaseException as e:
            app.logger.warning('clear tables failed. Error: {0}.'.format(
                str(e)))
            raise e
