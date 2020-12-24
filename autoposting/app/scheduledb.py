import configparser
import logging
import psycopg2
from datetime import datetime


class ScheduleDB:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')

        self.con = psycopg2.connect(
            dbname=config.get('bot', 'DB_NAME'),
            user=config.get('bot', 'DB_USER'),
            password=config.get('bot', 'DB_PASSWORD'),
            host=config.get('bot', 'DB_HOST')
        )
        self.cur = self.con.cursor()

        logging.basicConfig(format='%(asctime)-15s [ %(levelname)s ] %(message)s',
                            filemode='a',
                            filename=config.get('bot', 'LOG_DIR_PATH') + "log-{0}.log".format(
                                datetime.now().strftime("%Y-%m")))
        self.logger = logging.getLogger('db-logger')

        self.user_tag = config.get('bot', 'DB_USER_TAG')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.commit()
        self.con.close()

    def find_users_where(self, auto_posting_time=None, is_today=None):
        try:
            if auto_posting_time is not None and is_today is not None:
                self.cur.execute('SELECT id, "scheduleTag" FROM users '
                                 'WHERE auto_posting_time = %s AND is_today = %s  AND type = (%s)',
                                 (auto_posting_time, is_today, self.user_tag ))
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
