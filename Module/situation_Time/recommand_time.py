import sys
sys.path.append('../../venv/Lib/site-packages/')
import pandas as pd
import config
import pymysql
from datetime import datetime as dt

tag_list = {
    1 : [81, 139, 420, 786],
    2 : [82, 85, 110 ,129, 133, 316, 771],
    3 : [70, 79, 158, 243, 772],
    4 : [113, 122, 124, 396, 461, 773, 774, 782],
    5 : [58, 63, 765, 773, 782],
}
conn = pymysql.connect(
            host=config.Developer_config['host'],
            user=config.Developer_config['user'],
            password=config.Developer_config['password'],
            database=config.Developer_config['database'],
            port=config.Developer_config['port'],
            cursorclass=pymysql.cursors.DictCursor,
        )

class time_module:
    '''
    Module for channel recommand system by time
    '''

    # Initialize time_idx
    def __init__(self):
        time = dt.now().hour

        if 7 < time < 12:
            self.time_idx = 1
        elif 12 <= time < 18:
            self.time_idx = 2
        elif 18 <= time < 21:
            self.time_idx = 3
        elif 21 <= time:
            self.time_idx = 4
        else:
            self.time_idx = 5

    # Recommand channel_list through tag_list by time
    def time_channel_idx(self):
        tags = ','.join(map(str, tag_list[self.time_idx]))
        cursor = conn.cursor()

        sql = config.time_sql['time_channel_idx'].format(tags)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        ch_idx = list(df.sample(n=2)['idx'])

        return ch_idx

    # comment_list by time
    def time_comment_idx(self):
        cursor = conn.cursor()

        sql = config.time_sql['time_comment_idx'].format(self.time_idx)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        result = df.sample(n=1).reset_index()

        return result['image'], result['comment'], result['tagline']
