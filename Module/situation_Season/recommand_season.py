import sys
sys.path.append('../../venv/Lib/site-packages/')
import pandas as pd
import config
import pymysql
from datetime import datetime as dt

tag_list = {
    1 : [168, 766, 769, 783, 791, 794],
    2 : [3, 417, 471, 481, 591, 788],
    3 : [31, 64, 67, 762, 790],
    4 : [77, 112, 768, 779, 792],
}
conn = pymysql.connect(
            host=config.Developer_config['host'],
            user=config.Developer_config['user'],
            password=config.Developer_config['password'],
            database=config.Developer_config['database'],
            port=config.Developer_config['port'],
            cursorclass=pymysql.cursors.DictCursor,
        )

class season_module:
    '''
    Module for channel recommand system by season
    '''

    # Initialize season_idx and hour
    def __init__(self):
        month = dt.now().month
        day = dt.now().day

        if 3 <= month < 6:
            self.season_idx = 1
        elif 6 <= month < 9 or (month == 9 and day < 15):
            self.season_idx = 2
        elif 10 <= month < 12 or (month == 9 and day >= 15):
            self.season_idx = 3
        else:
            self.season_idx = 4

        time = dt.now().hour
        if 7 < time < 12:
            self.hour = 7
        elif 12 <= time < 18:
            self.hour = 12
        elif 18 <= time < 24:
            self.hour = 19
        else:
            self.hour = 0

    # Recommand channel_list through tag_list by season
    def season_channel_idx(self):
        tags = ','.join(map(str, tag_list[self.season_idx]))
        cursor = conn.cursor()

        sql = config.season_sql['season_channel_idx'].format(tags)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        ch_idx = list(df.sample(n=2)['idx'])

        return ch_idx

    # comment_list by season
    def season_comment_idx(self):
        cursor = conn.cursor()

        sql = config.season_sql['season_comment_idx'].format(self.season_idx, self.hour)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        result = df.sample(n=1).reset_index()

        return result['image'], result['comment'], result['tagline']