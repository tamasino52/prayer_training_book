from flask_bootstrap import Bootstrap
from flask import Flask, render_template, make_response, send_from_directory, request, redirect, url_for
import os

app = Flask(__name__, static_folder='static')
Bootstrap(app)

stat_config = {
    'total_watch': 0,
    'passed_session': 0,
    'ongoing_session': 0
}
book_list = [

    {
        'id': 0,
        'title': '나라를 위한 기도',
        'image': '../static/images/city2.jpg',
        'context': 'context/나라를 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 1,
        'title': '교회를 위한 기도',
        'image': '../static/images/church2.jpg',
        'context': 'context/교회를 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 2,
        'title': '담임목사님을 위한 기도',
        'image': '../static/images/church.jpg',
        'context': 'context/담임목사님을 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 3,
        'title': '목장을 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/목장을 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 4,
        'title': '태신자를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/태신자를 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 5,
        'title': '사람을 위한 기도',
        'image': '../static/images/family1.jpg',
        'context': 'context/사람을 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 6,
        'title': '가정을 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/가정을 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 7,
        'title': '남편을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/남편을 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 8,
        'title': '아내를 위한 기도',
        'image': '../static/images/episode.jpg',
        'context': 'context/아내를 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 9,
        'title': '부모를 위한 기도',
        'image': '../static/images/contact.jpg',
        'context': 'context/부모를 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 10,
        'title': '자녀를 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/자녀를 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 11,
        'title': '개인기도 1',
        'image': '../static/images/forest.jpg',
        'context': 'context/개인기도 1.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 12,
        'title': '개인기도 2',
        'image': '../static/images/cloud.jpg',
        'context': 'context/개인기도 2.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 13,
        'title': '회개기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/회개기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 14,
        'title': '영적인 힘을 얻기 위한 기도',
        'image': '../static/images/city3.jpg',
        'context': 'context/영적인 힘을 얻기 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 15,
        'title': '시험이 있을 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/시험이 있을 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 16,
        'title': '기도가 잘 되지 않을 때 드리는 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/기도가 잘 되지 않을 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 17,
        'title': '삶에 지칠 때 드리는 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/삶에 지칠 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 18,
        'title': '감사할 때 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/감사할 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 19,
        'title': '몸이 아플 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/몸이 아플 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 20,
        'title': '부부간에 불화가 있을 때 드리는 기도',
        'image': '../static/images/wave.jpg',
        'context': 'context/부부간에 불화가 있을 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 21,
        'title': '물질적인 어려움에 있을 때 드리는 기도',
        'image': '../static/images/wave2.jpg',
        'context': 'context/물질적인 어려움에 있을 때 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 22,
        'title': '사업을 위한 기도',
        'image': '../static/images/business.jpg',
        'context': 'context/사업을 위한 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 23,
        'title': '하루를 시작하며 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/하루를 시작하며 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    },
    {
        'id': 24,
        'title': '하루를 마감하며 드리는 기도',
        'image': '../static/images/night.jpg',
        'context': 'context/하루를 마감하며 드리는 기도.html',
        'mp3': '../static/files/1.mp3',
        'watch': 0,
        'update': '2020-09-22'
    }
]


@app.route('/')
def domain():
    if request.host == 'cvlab.ipdisk.co.kr':
        return redirect('http://cvlab.ipdisk.co.kr:250')
    if request.host == 'www.xn--ok0bv9hm4dy6wd0o.site':
        return redirect('/home')
    return


@app.route('/home')
def home():
    resp = make_response(render_template('home.html', book_list=book_list, stat_config=stat_config))
    return resp


@app.route('/book/<int:book_id>')
def book(book_id):
    book_list[book_id]['watch'] += 1
    stat_config['total_watch'] += 1
    resp = make_response(render_template(book_list[book_id]['context'], book_id=book_id, book_list=book_list))
    return resp


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, threaded=True)
