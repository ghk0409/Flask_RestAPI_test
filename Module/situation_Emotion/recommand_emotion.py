import sys
sys.path.append('../../venv/Lib/site-packages/')
import pandas as pd
import config
import pymysql

tag_list = {
    1 : [60, 99, 131, 212, 223, 242, 252, 260, 350, 354, 388, 395, 437, 438, 484, 513, 769, 842],
    2 : [55, 70, 75, 132, 193, 198, 235, 248, 323, 324, 360, 366, 408, 489],
    3 : [24, 25, 104, 140, 160, 194, 205, 292, 300, 427, 428, 476, 500, 615],
    4 : [70, 95, 132, 156, 163, 212, 249, 258, 259, 318, 360, 366, 396, 519, 539, 555, 584, 601],
    5 : [95, 122, 129, 132, 156, 161, 163, 249, 263, 318, 360, 366, 539, 555, 584],
    6 : [60, 99, 131, 223, 242, 252, 260, 350, 354, 388, 437, 438, 484, 513, 842],
    7 : [18, 61, 130, 137, 183, 201, 219, 221, 226, 228, 229, 231, 257, 368],
    8 : [18, 61, 130, 183, 201, 219, 221, 226, 227, 228, 229, 230, 231, 261, 470],
    9 : [63, 64, 67, 117, 219, 222, 239, 270, 284, 496],
    10 : [37, 38, 40, 97, 104, 140, 152, 160, 162, 194, 237, 238, 243,
          256, 340, 416, 417, 563, 577, 580, 615, 626, 635, 840],
}

main_emotion_type = {
    1: ['d'],
    2: ['h'],
    3: ['c'],
    4: ['h'],
    5: ['h'],
    6: ['a'],
    7: ['b', 'f'],
    8: ['f', 'g'],
    9: ['e', 'f'],
    10: ['c'],
}

conn = pymysql.connect(
            host=config.Developer_config['host'],
            user=config.Developer_config['user'],
            password=config.Developer_config['password'],
            database=config.Developer_config['database'],
            port=config.Developer_config['port'],
            cursorclass=pymysql.cursors.DictCursor,
        )

# get user_idx return user's artist_idx
def user_artist_idx(user_idx):
    cursor = conn.cursor()

    sql = config.emotion_sql['user_artist_idx'].format(user_idx)
    cursor.execute(sql)
    res = cursor.fetchall()
    df = pd.DataFrame(res)
    artist_idx = list(df['tag_idx'])

    return artist_idx

# return channel_list by user's emotion tag and artist
def channel_list(tag_idx, artist_idx):
    cursor = conn.cursor()

    sql = config.emotion_sql['channel_list'].format(tag_idx, artist_idx)
    cursor.execute(sql)
    res = cursor.fetchall()

    if res:
        df = pd.DataFrame(res)
        return ','.join(map(str,list(df['idx'])))
    else:
        return 0

# return channel_list & channel's emotion
def channel_idx_feel(channel_idx):
    cursor = conn.cursor()

    sql = config.emotion_sql['channel_idx_feel'].format(channel_idx)
    cursor.execute(sql)
    res = cursor.fetchall()

    if res:
        df = pd.DataFrame(res)
        return df
    else:
        return 0

# return channel_list & channel's emotion by user's emotion tag
def channel_idx_feel_noneAritst(tag_idx):
    cursor = conn.cursor()

    sql = config.emotion_sql['channel_idx_feel_noneAritst'].format(tag_idx)
    cursor.execute(sql)
    res = cursor.fetchall()
    df = pd.DataFrame(res)

    return df

def rank_emotion_channel(df, emotion_type):
    # 메인 감정 1개일 경우
    if len(emotion_type) == 1:
        df_rank = df.sort_values(by=emotion_type, ascending=False)

        if len(df_rank) > 20:
            return df_rank[:20].sample(n=2)
        else:
            return df_rank.sample(n=2)
    # 메인 감정이 2개일 경우 각각 채널 뽑도록 할 예정
    else:
        df_rank = df.sort_values(by=emotion_type, ascending=False)

        if len(df_rank) > 20:
            return df_rank[:20].sample(n=2)
        else:
            return df_rank.sample(n=2)

class emotion_module:
    '''
    Module for channel recommand system by emotion
    '''

    # Initialize season_idx and hour
    def __init__(self, user_idx, emotion_idx):
        self.user_idx = user_idx
        self.emotion_idx = emotion_idx
        self.artist_idx = user_artist_idx(self.user_idx)
        self.main_emotion_type = main_emotion_type[emotion_idx]

    def emotion_channel_idx(self):
        tag_idx = ','.join(map(str, tag_list[self.emotion_idx]))
        artist_idx = ','.join(map(str, self.artist_idx))
        ch_list = channel_list(tag_idx, artist_idx)

        if ch_list != 0:
            df = channel_idx_feel(ch_list)
            # df 결과에서 메인 감정값이 사용자 감정과 일치하는 채널 idx 반환
            result_df = rank_emotion_channel(df, self.main_emotion_type)

        else:
            df = channel_idx_feel_noneAritst(tag_idx)
            # df 결과에서 메인 감정값이 사용자 감정과 일치하는 채널 idx 반환
            result_df = rank_emotion_channel(df, self.main_emotion_type)

        ch_idx = list(result_df['channel_idx'])

        return ch_idx

    # comment_list by emotion
    def emotion_comment_idx(self):
        cursor = conn.cursor()

        sql = config.emotion_sql['emotion_comment_idx'].format(self.emotion_idx)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        result = df.sample(n=1).reset_index()

        return result['background'], result['title'], result['tagLine']