from flask import current_app as app
import psycopg2


class ApiSettingsDB:
    def __init__(self, config):
        self.con = psycopg2.connect(
            dbname=config["API_DB_NAME"],
            user=config["API_DB_USER"],
            password=config["API_DB_PASSWORD"],
            host=config["API_DB_HOST"])
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.commit()
        self.con.close()

    def add_user(self, username, pw_hash):
        try:
            self.cur.execute('INSERT INTO api_users(username, pw_hash) VALUES(%s,%s);',
                             (username, pw_hash))
            self.con.commit()
            return True
        except BaseException as e:
            app.logger.warning('Add user failed. Error: {0}. Data: username={1}'.format(
                str(e), username))
            return False

    def get_user_info(self, username):
        data = None
        try:
            self.cur.execute("SELECT id, username, pw_hash FROM api_users WHERE username = (%s)", (username, ))
            data = self.cur.fetchone()
        except BaseException as e:
            app.logger.warning('Select user failed. Error: {0}. Data: username={1}'.format(str(e), username))
            raise e
        finally:
            return data
