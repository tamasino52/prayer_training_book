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

version = '3.1'

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
        'mp3': '../static/files/기도훈련집_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '나라를 위한 기도',
        'image': '../static/images/city2.jpg',
        'context': 'context/나라를 위한 기도.html',
        'mp3': '../static/files/나라를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '교회를 위한 기도',
        'image': '../static/images/church2.jpg',
        'context': 'context/교회를 위한 기도.html',
        'mp3': '../static/files/교회를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '담임목사님을 위한 기도',
        'image': '../static/images/church.jpg',
        'context': 'context/담임목사님을 위한 기도.html',
        'mp3': '../static/files/담임목사님을+위한+기도_audio2.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '목장을 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/목장을 위한 기도.html',
        'mp3': '../static/files/목장을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '태신자를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/태신자를 위한 기도.html',
        'mp3': '../static/files/태신자를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '사람을 위한 기도',
        'image': '../static/images/family1.jpg',
        'context': 'context/사람을 위한 기도.html',
        'mp3': '../static/files/사람을+위한+기도_audio2.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '가정을 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/가정을 위한 기도.html',
        'mp3': '../static/files/가정을+위한+기도_audio2.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '남편을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/남편을 위한 기도.html',
        'mp3': '../static/files/남편을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '아내를 위한 기도',
        'image': '../static/images/episode.jpg',
        'context': 'context/아내를 위한 기도.html',
        'mp3': '../static/files/아내를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '부모를 위한 기도',
        'image': '../static/images/contact.jpg',
        'context': 'context/부모를 위한 기도.html',
        'mp3': '../static/files/부모를+위한+기도_audio2.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '자녀를 위한 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/자녀를 위한 기도.html',
        'mp3': '../static/files/자녀를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '개인기도 1',
        'image': '../static/images/forest.jpg',
        'context': 'context/개인기도 1.html',
        'mp3': '../static/files/개인기도+1_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '개인기도 2',
        'image': '../static/images/cloud.jpg',
        'context': 'context/개인기도 2.html',
        'mp3': '../static/files/개인기도+2_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '회개기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/회개기도.html',
        'mp3': '../static/files/회개기도_audio2.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '영적인 힘을 얻기 위한 기도',
        'image': '../static/images/city3.jpg',
        'context': 'context/영적인 힘을 얻기 위한 기도.html',
        'mp3': '../static/files/영적인+힘을+얻기+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '시험이 있을 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/시험이 있을 때 드리는 기도.html',
        'mp3': '../static/files/시험이+있을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '기도가 잘 되지 않을 때 드리는 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/기도가 잘 되지 않을 때 드리는 기도.html',
        'mp3': '../static/files/기도가+잘+되지+않을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '삶에 지칠 때 드리는 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/삶에 지칠 때 드리는 기도.html',
        'mp3': '../static/files/삶에+지칠+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '감사할 때 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/감사할 때 드리는 기도.html',
        'mp3': '../static/files/감사할+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '몸이 아플 때 드리는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/몸이 아플 때 드리는 기도.html',
        'mp3': '../static/files/몸이+아플+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '부부간에 불화가 있을 때 드리는 기도',
        'image': '../static/images/wave.jpg',
        'context': 'context/부부간에 불화가 있을 때 드리는 기도.html',
        'mp3': '../static/files/부부간에+불화가+있을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '물질적인 어려움에 있을 때 드리는 기도',
        'image': '../static/images/wave2.jpg',
        'context': 'context/물질적인 어려움에 있을 때 드리는 기도.html',
        'mp3': '../static/files/물질적인+어려움에+있을+때+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '사업을 위한 기도',
        'image': '../static/images/business.jpg',
        'context': 'context/사업을 위한 기도.html',
        'mp3': '../static/files/사업을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '하루를 시작하며 드리는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/하루를 시작하며 드리는 기도.html',
        'mp3': '../static/files/하루를+시작하며+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    {
        'title': '하루를 마감하며 드리는 기도',
        'image': '../static/images/night.jpg',
        'context': 'context/하루를 마감하며 드리는 기도.html',
        'mp3': '../static/files/하루를+마감하며+드리는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-11-05'
    },
    # 짧은 기도문
    {
        'title': '50일 소원기도문',
        'image': '../static/images/wave2.jpg',
        'context': 'context/소원기도문.html',
        'mp3': '../static/files/소원기도문_audio.mp3',
        'watch': 0,
        'update': '2020-11-23'
    },
    {
        'title': '새신자를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/새신자를 위한 기도.html',
        'mp3': '../static/files/새신자를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-03'
    },
    {
        'title': '영적 대적 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/영적 대적 기도.html',
        'mp3': '../static/files/영적+대적+기도_audio2.mp3',
        'watch': 0,
        'update': '2020-12-03'
    },
    # 기도훈련집 초등부
    {
        'title': '기도훈련집 초등부 전체 한 번에 읽기',
        'image': '../static/images/church.jpg',
        'context': 'context/초등부 기도훈련집.html',
        'mp3': '../static/files/기도훈련집 초등부(음악).mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '개인기도1',
        'image': '../static/images/cross1.jpg',
        'context': 'context/초등부 개인기도1.html',
        'mp3': '../static/files/초등부+개인기도+1_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '개인기도2',
        'image': '../static/images/cross2.jpg',
        'context': 'context/초등부 개인기도2.html',
        'mp3': '../static/files/초등부+개인기도+2_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '아침에 일어나서 하는 기도',
        'image': '../static/images/day.jpg',
        'context': 'context/초등부 아침에 일어나서 하는 기도.html',
        'mp3': '../static/files/초등부+아침에+일어나서+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '자기 전에 하는 기도',
        'image': '../static/images/night.jpg',
        'context': 'context/초등부 자기 전에 하는 기도.html',
        'mp3': '../static/files/초등부+자기+전에+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '식사기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/초등부 식사기도.html',
        'mp3': '../static/files/초등부+식사기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '몸이 아플 때 하는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/초등부 몸이 아플 때 하는 기도.html',
        'mp3': '../static/files/초등부+몸이+아플+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '믿음 생활을 잘하게 해 달라는 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/초등부 믿음 생활을 잘하게 해달라는 기도.html',
        'mp3': '../static/files/초등부+믿음+생활을+잘하게+해+달라는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '전도하기 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/초등부 전도하기 위한 기도.html',
        'mp3': '../static/files/초등부+전도하기+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '목자를 잘하게 해 달라는 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/초등부 목자를 잘하게 해달라는 기도.html',
        'mp3': '../static/files/초등부+목자를+잘하게+해+달라는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '믿음이 떨어졌을 때 영적인 힘을 얻기 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/초등부 믿음이 떨어졌을 때 영적인 힘을 얻기 위한 기도.html',
        'mp3': '../static/files/초등부+믿음이+떨어졌을+때+영적인+힘을+얻기+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '시험이 들었을 때 하는 기도',
        'image': '../static/images/blue.jpg',
        'context': 'context/초등부 시험이 들었을 때 하는 기도.html',
        'mp3': '../static/files/초등부+시험이+들었을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '좋은 친구를 얻기 위한 기도',
        'image': '../static/images/episode.jpg',
        'context': 'context/초등부 좋은 친구를 얻기 위한 기도.html',
        'mp3': '../static/files/초등부+좋은+친구를+얻기+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '이성 친구를 사귀기 위한 기도',
        'image': '../static/images/newsletter.jpg',
        'context': 'context/초등부 이성 친구를 사귀기 위한 기도.html',
        'mp3': '../static/files/초등부+이성+친구를+사귀기+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '친구와 다투고 헤어졌을 때 하는 기도',
        'image': '../static/images/index.jpg',
        'context': 'context/초등부 친구와 다투고 헤어졌을 때 하는 기도.html',
        'mp3': '../static/files/초등부+친구와+다투고+헤어졌을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '친구에게 배신당했을 때 하는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/초등부 친구에게 배신당했을 때 하는 기도.html',
        'mp3': '../static/files/초등부+친구에게+배신당했을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '공부를 잘하게 해 달라는 기도',
        'image': '../static/images/newsletter.jpg',
        'context': 'context/초등부 공부를 잘하게 해달라는 기도.html',
        'mp3': '../static/files/초등부+공부를+잘하게+해+달라는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '공부가 하기 싫을 때 하는 기도',
        'image': '../static/images/newsletter.jpg',
        'context': 'context/초등부 공부가 하기 싫을 때 하는 기도.html',
        'mp3': '../static/files/초등부+공부가+하기+싫을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '부모님께 야단맞았을 때 하는 기도',
        'image': '../static/images/family2.jpg',
        'context': 'context/초등부 부모님께 야단맞았을 때 하는 기도.html',
        'mp3': '../static/files/초등부+부모님께+야단맞았을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '선생님에게 야단맞았을 때 하는 기도',
        'image': '../static/images/wave2.jpg',
        'context': 'context/초등부 선생님에게 야단맞았을 때 하는 기도.html',
        'mp3': '../static/files/초등부+선생님에게+야단맞았을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '형제, 자매와 다투었을 때 하는 기도',
        'image': '../static/images/family1.jpg',
        'context': 'context/초등부 형제, 자매와 다투었을 때 하는 기도.html',
        'mp3': '../static/files/초등부+형제+자매와+다투었을+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '왕자병 치료를 위한 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/초등부 왕자병 치료를 위한 기도.html',
        'mp3': '../static/files/초등부+왕자병+치료를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '공주병 치료를 위한 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/초등부 공주병 치료를 위한 기도.html',
        'mp3': '../static/files/초등부+공주병+치료를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '기분이 나쁠 때 하는 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/초등부 기분이 나쁠 때 하는 기도.html',
        'mp3': '../static/files/초등부+기분이+나쁠+때+하는+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '교회에서 하는 대표기도',
        'image': '../static/images/church2.jpg',
        'context': 'context/초등부 교회에서 하는 대표기도.html',
        'mp3': '../static/files/초등부+교회에서+하는+대표기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '가정에서 하는 대표기도',
        'image': '../static/images/family1.jpg',
        'context': 'context/초등부 가정에서 하는 대표기도.html',
        'mp3': '../static/files/초등부+가정에서+하는+대표기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '목장에서 하는 대표기도',
        'image': '../static/images/cloud.jpg',
        'context': 'context/초등부 목장에서 하는 대표기도.html',
        'mp3': '../static/files/초등부+목장에서+하는+대표기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '가족들 식사 대표기도',
        'image': '../static/images/forest.jpg',
        'context': 'context/초등부 가족들 식사 대표기도.html',
        'mp3': '../static/files/초등부+가족들+식사+대표기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿는 아빠(엄마)를 위하 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/초등부 하나님을 믿는 아빠(엄마)를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿는+아빠(엄마)를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿지 않는 아빠(엄마)를 위한 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/초등부 하나님을 믿지 않는 아빠(엄마)를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿지+않는+아빠엄마를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿는 할아버지(할머니)를 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/초등부 하나님을 믿는 할아버지(할머니)를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿는+할아버지(할머니)를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿지 않는 할아버지(할머니)를 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/초등부 하나님을 믿지 않는 할아버지(할머니)를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿지+않는+할아버지할머니를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿는 형제(자매)를 위한 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/초등부 하나님을 믿는 형제(자매)를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿는+형제자매를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿지 않는 형제(자매)를 위한 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/초등부 하나님을 믿지 않는 형제(자매)를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿지+않는+형제자매를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '담임목사님과 사모님을 위한 기도',
        'image': '../static/images/church2.jpg',
        'context': 'context/초등부 담임목사님과 사모님을 위한 기도.html',
        'mp3': '../static/files/초등부+담임목사님과+사모님을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '부서 담당 목사님(전도사님)을 위한 기도',
        'image': '../static/images/cross1.jpg',
        'context': 'context/초등부 부서 담당 목사님(전도사님)을 위한 기도.html',
        'mp3': '../static/files/초등부+부서+담당+목사님(전도사님)을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '교회 선생님을 위한 기도',
        'image': '../static/images/cross2.jpg',
        'context': 'context/초등부 교회 선생님을 위한 기도.html',
        'mp3': '../static/files/초등부+교회+선생님을+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿는 친구를 위한 기도',
        'image': '../static/images/cross3.jpg',
        'context': 'context/초등부 하나님을 믿는 친구를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿는+친구를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    {
        'title': '하나님을 믿지 않는 친구를 위한 기도',
        'image': '../static/images/cross4.jpg',
        'context': 'context/초등부 하나님을 믿지 않는 친구를 위한 기도.html',
        'mp3': '../static/files/초등부+하나님을+믿지+않는+친구를+위한+기도_audio.mp3',
        'watch': 0,
        'update': '2020-12-09'
    },
    # ---------------------------------------------------------------------------------------
    # revision
    # ---------------------------------------------------------------------------------------
    {
        'title': '기도훈련집 개정판 전체',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/기도훈련집 개정판.html',
        'mp3': '../static/files/revision/기도훈련집 개정판.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '기도훈련집 개정판 2배속',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/기도훈련집 개정판.html',
        'mp3': '../static/files/revision/기도훈련집 개정판 2배속.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '나라를 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/나라를 위한 기도.html',
        'mp3': '../static/files/revision/나라를+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '교회를 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/교회를 위한 기도.html',
        'mp3': '../static/files/revision/교회를+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '담임목사님을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/담임목사님을 위한 기도.html',
        'mp3': '../static/files/revision/담임목사님을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '목장과 목장원을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/목장과 목장원을 위한 기도.html',
        'mp3': '../static/files/revision/목장과+목장원을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '태신자를 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/태신자를 위한 기도.html',
        'mp3': '../static/files/revision/태신자를+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '사람을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/사람을 위한 기도.html',
        'mp3': '../static/files/revision/사람을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '가정을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/가정을 위한 기도.html',
        'mp3': '../static/files/revision/가정을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '남편을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/남편을 위한 기도.html',
        'mp3': '../static/files/revision/남편을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '아내를 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/아내를 위한 기도.html',
        'mp3': '../static/files/revision/아내를+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '부모님을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/부모님을 위한 기도.html',
        'mp3': '../static/files/revision/부모님을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '자녀를 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/자녀를 위한 기도.html',
        'mp3': '../static/files/revision/자녀를+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '개인기도 1',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/개인기도1.html',
        'mp3': '../static/files/revision/개인기도1.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '개인기도 2',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/개인기도2.html',
        'mp3': '../static/files/revision/개인기도2.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '회개기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/회개기도.html',
        'mp3': '../static/files/revision/회개기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '영적인 힘을 얻기 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/영적인 힘을 얻기 위한 기도.html',
        'mp3': '../static/files/revision/영적인+힘을+얻기+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '시험이 있을 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/시험이 있을 때 드리는 기도.html',
        'mp3': '../static/files/revision/시험이+있을+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '기도가 잘 되지 않을 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/기도가 잘 되지 않을 때 드리는 기도.html',
        'mp3': '../static/files/revision/기도가+잘+되지+않을+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '삶에 지칠 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/삶에 지칠 때 드리는 기도.html',
        'mp3': '../static/files/revision/삶에+지칠+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '감사할 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/감사할 때 드리는 기도.html',
        'mp3': '../static/files/revision/감사할+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '몸이 아플 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/몸이 아플 때 드리는 기도.html',
        'mp3': '../static/files/revision/몸이+아플+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '부부간에 불화가 있을 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/부부간에 불화가 있을 때 드리는 기도.html',
        'mp3': '../static/files/revision/부부간에+불화가+있을+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '물질적인 어려움에 있을 때 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/물질적인 어려움에 있을 때 드리는 기도.html',
        'mp3': '../static/files/revision/물질적인+어려움에+있을+때+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '사업을 위한 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/사업을 위한 기도.html',
        'mp3': '../static/files/revision/사업을+위한+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '하루를 시작하며 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/하루를 시작하며 드리는 기도.html',
        'mp3': '../static/files/revision/하루를+시작하며+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '하루를 마감하며 드리는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/하루를 마감하며 드리는 기도.html',
        'mp3': '../static/files/revision/하루를+마감하며+드리는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '마귀를 물리치는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/마귀를 물리치는 기도.html',
        'mp3': '../static/files/revision/마귀를+물리치는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
    {
        'title': '질병을 치료하는 기도',
        'image': '../static/images/blog.jpg',
        'context': 'context/revision/질병을 치료하는 기도.html',
        'mp3': '../static/files/revision/질병을+치료하는+기도.mp3',
        'watch': 0,
        'update': '2021-08-22'
    },
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