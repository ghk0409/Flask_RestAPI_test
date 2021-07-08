from Module.situation_Season.recommand_season import season_module
from Module.situation_Time.recommand_time import time_module
from Module.situation_Weather.recommand_weather import weather_module, weatherType_api
from Module.situation_Emotion.recommand_emotion import emotion_module
from Module.module import find_user
from flask import Flask, request, jsonify
import time

# flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/v1/season', methods=['POST'])
def recommand_season():
    if request.method == 'POST':
        start = time.time()
        print(request.get_json())
        if 'user_idx' not in request.get_json():
            print('user_idx 값 없음')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 None입니다. user_idx 값을 보내주세요',
            }
        elif type(request.json['user_idx']) != int:
            print('user_idx 타입 다름')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 올바른 형식이 아닙니다. 올바른 형식의 user_idx를 보내주세요',
            }
        elif find_user.select_user_table(request.json['user_idx']) == 0:
            print('user_idx 없음')
            result = {
                'success': False,
                'data': None,
                'msg': '해당 user_idx가 존재하지 않습니다. 올바른 user_idx 값을 보내주세요',
            }
        else:
            sm = season_module()
            ch_idx = sm.season_channel_idx()
            image, comment, tagline = sm.season_comment_idx()
            end = time.time() - start
            result = {
                'success': True,
                'data': {
                    "background": image[0],
                    "ch_idx": ch_idx,
                    "ment_tagline": tagline[0],
                    "ment_title": comment[0],
                },
                'msg': 'weather',
                'time': end,
            }

        return jsonify(result)

    else:
        return "BAD"

@app.route('/api/v1/time', methods=['POST'])
def recommand_time():
    if request.method == 'POST':
        start = time.time()
        print(request.get_json())
        if 'user_idx' not in request.get_json():
            print('user_idx 값 없음')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 None입니다. user_idx 값을 보내주세요',
            }
        elif type(request.json['user_idx']) != int:
            print('user_idx 타입 다름')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 올바른 형식이 아닙니다. 올바른 형식의 user_idx를 보내주세요',
            }
        elif find_user.select_user_table(request.json['user_idx']) == 0:
            print('user_idx 없음')
            result = {
                'success': False,
                'data': None,
                'msg': '해당 user_idx가 존재하지 않습니다. 올바른 user_idx 값을 보내주세요',
            }
        else:
            tm = time_module()
            ch_idx = tm.time_channel_idx()
            image, comment, tagline = tm.time_comment_idx()
            end = time.time() - start

            result = {
                'success': True,
                'data': {
                    "background": image[0],
                    "ch_idx": ch_idx,
                    "ment_tagline": tagline[0],
                    "ment_title": comment[0],
                },
                'msg': 'weather',
                'time': end,
            }

        return jsonify(result)

    else:
        return "BAD"

@app.route('/api/v1/weather', methods=['POST'])
def recommand_weather():
    if request.method == 'POST':
        start = time.time()
        print(request.get_json())
        if 'user_idx' not in request.get_json():
            print('user_idx 값 없음')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 None입니다. user_idx 값을 보내주세요',
            }
        elif type(request.json['user_idx']) != int:
            print('user_idx 타입 다름')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 올바른 형식이 아닙니다. 올바른 형식의 user_idx를 보내주세요',
            }
        elif find_user.select_user_table(request.json['user_idx']) == 0:
            print('user_idx 없음')
            result = {
                'success': False,
                'data': None,
                'msg': '해당 user_idx가 존재하지 않습니다. 올바른 user_idx 값을 보내주세요',
            }
        else:
            x = request.json['x']
            y = request.json['y']

            api = weatherType_api(y, x)
            # weather_type 메서드를 통해 날씨 id별 type 결과 반환
            weather_type = api.weather_type()

            wm = weather_module(weather_type)
            ch_idx = wm.weather_channel_idx()
            image, comment, tagline = wm.weather_comment_idx()
            end = time.time()-start

            result = {
                'success':True,
                'data':{
                    "background": image[0],
                    "ch_idx": ch_idx,
                    "ment_tagline": tagline[0],
                    "ment_title": comment[0],
                },
                'msg': 'weather',
                'time': end,
            }

        return jsonify(result)

    else:
        return "BAD"

@app.route('/api/v1/emotion', methods=['POST'])
def recommand_emotion():
    if request.method == 'POST':
        start = time.time()
        print(request.get_json())
        if 'user_idx' not in request.get_json():
            print('user_idx 값 없음')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 None입니다. user_idx 값을 보내주세요',
            }
        elif type(request.json['user_idx']) != int:
            print('user_idx 타입 다름')
            result = {
                'success': False,
                'data': None,
                'msg': 'user_idx 값이 올바른 형식이 아닙니다. 올바른 형식의 user_idx를 보내주세요',
            }
        elif find_user.select_user_table(request.json['user_idx']) == 0:
            print('user_idx 없음')
            result = {
                'success': False,
                'data': None,
                'msg': '해당 user_idx가 존재하지 않습니다. 올바른 user_idx 값을 보내주세요',
            }
        else:
            user_idx = request.json['user_idx']
            user_emotion = request.json['user_emotion']

            em = emotion_module(user_idx, user_emotion)
            ch_idx = em.emotion_channel_idx()
            image, comment, tagline = em.emotion_comment_idx()
            end = time.time() - start

            result = {
                'success': True,
                'data': {
                    "background": image[0],
                    "ch_idx": ch_idx,
                    "ment_tagline": tagline[0],
                    "ment_title": comment[0],
                },
                'msg': 'weather',
                'time': end,
            }

        return jsonify(result)

    else:
        return "BAD"

if __name__ == '__main__':
    app.run(host='192.168.137.33', port=8088)