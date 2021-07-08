'''
receive: gps (latitude, longitude)
return: channel_idx
'''
import sys
sys.path.append('../../venv/Lib/site-packages/')
import pandas as pd
import config
import json
import requests
import pymysql
from datetime import datetime as dt

type_list = {
            200 : 4,
            201 : 4,
            202 : 4,
            210 : 4,
            211 : 4,
            212 : 4,
            221 : 4,
            230 : 4,
            231 : 4,
            232 : 4,
            300 : 3,
            301 : 3,
            302 : 3,
            310 : 3,
            311 : 3,
            312 : 3,
            313 : 3,
            314 : 3,
            321 : 3,
            500 : 3,
            501 : 3,
            502 : 4,
            503 : 4,
            504 : 4,
            511 : 3,
            520 : 3,
            521 : 3,
            522 : 4,
            531 : 3,
            600 : 5,
            601 : 5,
            602 : 5,
            611 : 5,
            612 : 5,
            613 : 5,
            615 : 5,
            616 : 5,
            620 : 5,
            621 : 5,
            622 : 5,
            701 : 7,
            711 : 7,
            721 : 6,
            731 : 6,
            741 : 7,
            751 : 6,
            761 : 6,
            762 : 6,
            771 : 3,
            781 : 4,
            800 : 1,
            801 : 1,
            802 : 2,
            803 : 2,
            804 : 2,
        }
tag_list = {
            1 : [16, 59, 131, 776, 794],
            2 : [789, 795, 367, 309, 67],
            3 : [48, 236, 270, 309, 317, 784, 789, 795],
            4 : [48, 236, 270, 309, 317, 784, 789, 795],
            5 : [96, 768, 779, 792],
            6 : [285, 778],
            7 : [787, 795],
        }
conn = pymysql.connect(
            host=config.Developer_config['host'],
            user=config.Developer_config['user'],
            password=config.Developer_config['password'],
            database=config.Developer_config['database'],
            port=config.Developer_config['port'],
            cursorclass=pymysql.cursors.DictCursor,
        )

class weatherType_api:
    '''
    openweathers api를 이용
    gps 좌표를 입력하여 해당 지역 날씨 데이터 return
    '''
    # gps 좌표 및 api 연동 위한 초기화
    def __init__(self, x, y):
        self.latitude = x
        self.longitude = y
        self.api_key = config.api_keys['openweather']

    # openweathers api를 이용하여 해당 gps weather return
    def weather_type(self):
        '''
        openweathers api 결과값을 통해 db 내 weather type 분류
        맑음	1
        구름	2
        비	3
        폭우/뇌우 4
        눈	5
        미세먼지	6
        안개	7
        '''
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}'
        res = requests.get(url).text
        res_json = json.loads(res)

        weather = res_json['weather'][0]['id']
        temp = res_json['main']['temp'] - 273.15
        temp_mean = res_json['main']['temp_min'] - 273.15

        self.result = {
            'weather': weather,
            'temp': temp,
            'temp_mean': temp_mean,
        }
        weather_type = type_list[self.result['weather']]

        return weather_type

class weather_module:
    '''
    Module for channel recommand system by weather
    '''

    # Initialize type_idx by weather and hour
    def __init__(self, type_idx):
        self.type_idx = type_idx

        time = dt.now().hour
        if 7 < time < 12:
            self.hour = 7
        elif 12 <= time < 18:
            self.hour = 12
        elif 18 <= time < 24:
            self.hour = 18
        else:
            self.hour = 0

    # recommand channel_list through tag_list by weather
    def weather_channel_idx(self):
        tags = ','.join(map(str, tag_list[self.type_idx]))
        cursor = conn.cursor()

        sql = config.weather_sql['weather_channel_idx'].format(tags)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        ch_idx = list(df.sample(n=2)['idx'])

        return ch_idx

    # comment_list by weather
    def weather_comment_idx(self):
        cursor = conn.cursor()

        sql = config.weather_sql['weather_comment_idx'].format(self.type_idx, self.hour)
        cursor.execute(sql)
        res = cursor.fetchall()
        df = pd.DataFrame(res)
        result = df.sample(n=1).reset_index()

        return result['image'], result['comment'], result['tagline']
