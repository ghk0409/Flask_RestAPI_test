import config
import pymysql

conn = pymysql.connect(
            host=config.Developer_config['host'],
            user=config.Developer_config['user'],
            password=config.Developer_config['password'],
            database=config.Developer_config['database'],
            port=config.Developer_config['port'],
            cursorclass=pymysql.cursors.DictCursor,
        )

class find_user:

    @staticmethod
    def select_user_table(user_idx):
        cursor = conn.cursor()

        sql = f'''
                    SELECT u.idx, u.nickname
                    FROM user AS u
                    WHERE u.idx = {user_idx}
            '''

        cursor.execute(sql)
        res = cursor.fetchall()

        if res:
            return 1
        else:
            return 0