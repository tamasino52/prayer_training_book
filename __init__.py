from flask_bootstrap import Bootstrap
from flask import Flask, render_template, make_response, send_from_directory, request, redirect, url_for
import os, pickle

app = Flask(__name__, static_folder='static')
Bootstrap(app)

book_list = [

    {
        'id': 0,
        'title': '나라를 위한 기도',
        'image': '../static/images/city2.jpg',
        'context': 'context/나라를 위한 기도.html',
        'mp3': '../static/files/나라를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 1,
        'title': '교회를 위한 기도',
        'image': '../static/images/church2.jpg',
        'context': 'context/교회를 위한 기도.html',
        'mp3': '../static/files/교회를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 2,
        'title': '담임목사님을 위한 기도',
        'image': '../static/images/church.jpg',
        'context': 'context/담임목사님을 위한 기도.html',
        'mp3': '../static/files/담임목사님을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 3,
        'title': '목장을 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/목장을 위한 기도.html',
        'mp3': '../static/files/목장을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 4,
        'title': '태신자를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/태신자를 위한 기도.html',
        'mp3': '../static/files/태신자를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 5,
        'title': '사람을 위한 기도',
        'image': '../static/images/family1.jpg',
        'context': 'context/사람을 위한 기도.html',
        'mp3': '../static/files/사람을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 6,
        'title': '가정을 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/가정을 위한 기도.html',
        'mp3': '../static/files/가정을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 7,
        'title': '남편을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/남편을 위한 기도.html',
        'mp3': '../static/files/남편을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 8,
        'title': '아내를 위한 기도',
        'image': '../static/images/episode.jpg',
        'context': 'context/아내를 위한 기도.html',
        'mp3': '../static/files/아내를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 9,
        'title': '부모를 위한 기도',
        'image': '../static/images/contact.jpg',
        'context': 'context/부모를 위한 기도.html',
        'mp3': '../static/files/부모를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 10,
        'title': '자녀를 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/자녀를 위한 기도.html',
        'mp3': '../static/files/자녀를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 11,
        'title': '개인기도 1',
        'image': '../static/images/forest.jpg',
        'context': 'context/개인기도 1.html',
        'mp3': '../static/files/개인기도+1_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 12,
        'title': '개인기도 2',
        'image': '../static/images/cloud.jpg',
        'context': 'context/개인기도 2.html',
        'mp3': '../static/files/개인기도+2_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 13,
        'title': '회개기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/회개기도.html',
        'mp3': '../static/files/회개기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 14,
        'title': '영적인 힘을 얻기 위한 기도',
        'image': '../static/images/city3.jpg',
        'context': 'context/영적인 힘을 얻기 위한 기도.html',
        'mp3': '../static/files/영적인+힘을+얻기+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 15,
        'title': '시험이 있을 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/시험이 있을 때 드리는 기도.html',
        'mp3': '../static/files/시험이+있을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 16,
        'title': '기도가 잘 되지 않을 때 드리는 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/기도가 잘 되지 않을 때 드리는 기도.html',
        'mp3': '../static/files/기도가+잘+되지+않을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 17,
        'title': '삶에 지칠 때 드리는 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/삶에 지칠 때 드리는 기도.html',
        'mp3': '../static/files/삶에+지칠+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 18,
        'title': '감사할 때 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/감사할 때 드리는 기도.html',
        'mp3': '../static/files/감사할+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 19,
        'title': '몸이 아플 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/몸이 아플 때 드리는 기도.html',
        'mp3': '../static/files/몸이+아플+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 20,
        'title': '부부간에 불화가 있을 때 드리는 기도',
        'image': '../static/images/wave.jpg',
        'context': 'context/부부간에 불화가 있을 때 드리는 기도.html',
        'mp3': '../static/files/부부간에+불화가+있을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 21,
        'title': '물질적인 어려움에 있을 때 드리는 기도',
        'image': '../static/images/wave2.jpg',
        'context': 'context/물질적인 어려움에 있을 때 드리는 기도.html',
        'mp3': '../static/files/물질적인+어려움에+있을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 22,
        'title': '사업을 위한 기도',
        'image': '../static/images/business.jpg',
        'context': 'context/사업을 위한 기도.html',
        'mp3': '../static/files/사업을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 23,
        'title': '하루를 시작하며 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/하루를 시작하며 드리는 기도.html',
        'mp3': '../static/files/하루를+시작하며+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'id': 24,
        'title': '하루를 마감하며 드리는 기도',
        'image': '../static/images/night.jpg',
        'context': 'context/하루를 마감하며 드리는 기도.html',
        'mp3': '../static/files/하루를+마감하며+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    }
]

if os.path.exists('./stats.pickle'):
    with open('stats.pickle', 'rb') as f:
        pickle_data = pickle.load(f)

    for index, book_info in enumerate(book_list):
        book_info['watch'] = pickle_data[index]
else:
    pickle_data = [0] * book_list.__len__()


@app.route('/')
def domain():
    return redirect('/home')
    

@app.route('/home')
def home():
    resp = make_response(render_template('home.html', book_list=book_list))
    return resp


@app.route('/book/<int:book_id>')
def book(book_id):
    book_list[book_id]['watch'] += 1
    pickle_data[book_id] += 1

    if pickle_data[book_id] % 10 is 0:
        with open('stats.pickle', 'wb') as f:
            pickle.dump(pickle_data, f, pickle.HIGHEST_PROTOCOL)

    resp = make_response(render_template(book_list[book_id]['context'], book_id=book_id, book_list=book_list))
    return resp


@app.route('/information')
def information():
    return make_response(render_template('information.html'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, threaded=True)
