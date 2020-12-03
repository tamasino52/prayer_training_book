import os
import pickle

from flask import Flask, render_template, make_response, send_from_directory, redirect, send_file
from flask_bootstrap import Bootstrap
from flask_caching import Cache

# 플라스크 세팅 (부트스트랩, 캐시 포함)
app = Flask(__name__, static_folder='static')
Bootstrap(app)
cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

version = '2.5'

# 데이터베이스 역할을 하는 리스트
"""
id : 책 번호(기도훈련집 1 : 0~25, 기타 : 26~)
title : 책 이름 (음원 파일명, 사용자에게 보여지는 이름)
image : 책 상단에 보이는 배경화면이 될 이미지 파일
context : 상속받을 템플릿 명
mp3 : 음원
watch : 조회수 (pickle 파일에서 초기화)
update : 최근 갱신일
"""
book_list = [
    {
        'title': '기도훈련집 전체 한 번에 읽기',
        'image': '../static/images/blog.jpg',
        'context': 'context/기도훈련집1.html',
        'mp3': '../static/files/기도훈련집(압축).mp3',
        'bgm': '../static/files/비파와 수금 Vol.2 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-17'
    },
    {
        'title': '나라를 위한 기도',
        'image': '../static/images/city2.jpg',
        'context': 'context/나라를 위한 기도.html',
        'mp3': '../static/files/나라를+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '교회를 위한 기도',
        'image': '../static/images/church2.jpg',
        'context': 'context/교회를 위한 기도.html',
        'mp3': '../static/files/교회를+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '담임목사님을 위한 기도',
        'image': '../static/images/church.jpg',
        'context': 'context/담임목사님을 위한 기도.html',
        'mp3': '../static/files/담임목사님을+위한+기도_audio2.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '목장을 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/목장을 위한 기도.html',
        'mp3': '../static/files/목장을+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '태신자를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/태신자를 위한 기도.html',
        'mp3': '../static/files/태신자를+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '사람을 위한 기도',
        'image': '../static/images/family1.jpg',
        'context': 'context/사람을 위한 기도.html',
        'mp3': '../static/files/사람을+위한+기도_audio2.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '가정을 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/가정을 위한 기도.html',
        'mp3': '../static/files/가정을+위한+기도_audio2.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '남편을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/남편을 위한 기도.html',
        'mp3': '../static/files/남편을+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '아내를 위한 기도',
        'image': '../static/images/episode.jpg',
        'context': 'context/아내를 위한 기도.html',
        'mp3': '../static/files/아내를+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '부모를 위한 기도',
        'image': '../static/images/contact.jpg',
        'context': 'context/부모를 위한 기도.html',
        'mp3': '../static/files/부모를+위한+기도_audio2.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '자녀를 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/자녀를 위한 기도.html',
        'mp3': '../static/files/자녀를+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '개인기도 1',
        'image': '../static/images/forest.jpg',
        'context': 'context/개인기도 1.html',
        'mp3': '../static/files/개인기도+1_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '개인기도 2',
        'image': '../static/images/cloud.jpg',
        'context': 'context/개인기도 2.html',
        'mp3': '../static/files/개인기도+2_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '회개기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/회개기도.html',
        'mp3': '../static/files/회개기도_audio2.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '영적인 힘을 얻기 위한 기도',
        'image': '../static/images/city3.jpg',
        'context': 'context/영적인 힘을 얻기 위한 기도.html',
        'mp3': '../static/files/영적인+힘을+얻기+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '시험이 있을 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/시험이 있을 때 드리는 기도.html',
        'mp3': '../static/files/시험이+있을+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '기도가 잘 되지 않을 때 드리는 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/기도가 잘 되지 않을 때 드리는 기도.html',
        'mp3': '../static/files/기도가+잘+되지+않을+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '삶에 지칠 때 드리는 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/삶에 지칠 때 드리는 기도.html',
        'mp3': '../static/files/삶에+지칠+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '감사할 때 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/감사할 때 드리는 기도.html',
        'mp3': '../static/files/감사할+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '몸이 아플 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/몸이 아플 때 드리는 기도.html',
        'mp3': '../static/files/몸이+아플+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '부부간에 불화가 있을 때 드리는 기도',
        'image': '../static/images/wave.jpg',
        'context': 'context/부부간에 불화가 있을 때 드리는 기도.html',
        'mp3': '../static/files/부부간에+불화가+있을+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '물질적인 어려움에 있을 때 드리는 기도',
        'image': '../static/images/wave2.jpg',
        'context': 'context/물질적인 어려움에 있을 때 드리는 기도.html',
        'mp3': '../static/files/물질적인+어려움에+있을+때+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '사업을 위한 기도',
        'image': '../static/images/business.jpg',
        'context': 'context/사업을 위한 기도.html',
        'mp3': '../static/files/사업을+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '하루를 시작하며 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/하루를 시작하며 드리는 기도.html',
        'mp3': '../static/files/하루를+시작하며+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '하루를 마감하며 드리는 기도',
        'image': '../static/images/night.jpg',
        'context': 'context/하루를 마감하며 드리는 기도.html',
        'mp3': '../static/files/하루를+마감하며+드리는+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.22 - 목마른 사슴 (Guitar 이승배).mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '50일 소원기도문',
        'image': '../static/images/wave2.jpg',
        'context': 'context/소원기도문.html',
        'mp3': '../static/files/소원기도문_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-11-23'
    },
    {
        'title': '새신자를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/새신자를 위한 기도.html',
        'mp3': '../static/files/새신자를+위한+기도_audio.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-12-03'
    },
    {
        'title': '영적 대적 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/영적 대적 기도.html',
        'mp3': '../static/files/영적+대적+기도_audio2.mp3',
        'bgm': '../static/files/비파와 수금 Vol.15 - 내일 일은 난 몰라요 (Piano 유진희).mp3',
        'watch': 0,
        'update': '2020-12-03'
    }
]

for idx, book in enumerate(book_list):
    book['id'] = idx

# pickle 파일에서 마지막으로 저장했던 기존 데이터를 로드
if os.path.exists('./stats.pickle'):
    with open('stats.pickle', 'rb') as f:
        pickle_data = pickle.load(f)

    for index, book_info in enumerate(book_list):
        try:
            book_info['watch'] = pickle_data[index]
        except IndexError:
            pickle_data.append(0)


# 홈페이지 접근 시 메인 홈 페이지로 리다이렉트
@app.route('/')
def domain():
    return redirect('/home')
    

# 메인 홈 페이지
@app.route('/home')
@cache.cached(timeout=3)
def home():
    resp = make_response(render_template('home.html', book_list=book_list, version=version))
    return resp


# 뷰어 페이지
@app.route('/book/<int:book_id>')
def book(book_id):
    book_list[book_id]['watch'] += 1
    pickle_data[book_id] += 1

    if pickle_data[book_id] % 10 is 0:
        with open('stats.pickle', 'wb') as f:
            pickle.dump(pickle_data, f, pickle.HIGHEST_PROTOCOL)

    resp = make_response(render_template(book_list[book_id]['context'], book_id=book_id, book_list=book_list, version=version))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


# 라이센스 정보 페이지
@app.route('/information')
def information():
    return make_response(render_template('information.html'))


# 홈페이지 아이콘
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico')


# 파일 다운로드 경로
@app.route('/download/<int:book_id>')
def download(book_id):
    return send_file(os.path.join("static", book_list[book_id]['mp3']),
                     attachment_filename=book_list[book_id]['title'] + '.mp3', as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, threaded=True)