#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File Name: launch.py
    Date: 09/21/2017
    Author: hackrflov
    Email: hackrflov@gmail.com
    Python Version: 2.7
"""

import requests
import json
import sys
import argparse
import time
from datetime import datetime
import pandas as pd
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
logging.basicConfig(format="%(asctime)s; %(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger('bike_crawler')

RETRY_TIMES = 3
AREAS = [
    # ===== Main Area ===== #
    (121.496061,31.258024),  # 久耕小区
    (121.496487,31.257221),  # 久耕小区
    (121.496954,31.256592),  # 久耕小区
    (121.497637,31.256913),  # 久耕小区
    (121.498226,31.257156),  # 久耕小区
    (121.498378,31.257970),  # 久耕小区
    (121.498419,31.258919),  # 久耕小区
    (121.497323,31.258541),  # 久耕小区
    (121.498872,31.259031),  # 春阳住宅小区
    (121.498796,31.258194),  # 春阳住宅小区
    (121.498549,31.257221),  # 春阳住宅小区
    (121.499277,31.257360),  # 春阳住宅小区
    (121.500157,31.257499),  # 春阳住宅小区
    (121.500166,31.258317),  # 春阳住宅小区
    (121.500197,31.259085),  # 春阳住宅小区
    (121.499537,31.259046),  # 春阳住宅小区
    (121.498553,31.256531),  # 东余杭路214弄
    (121.499286,31.256014),  # 东余杭路214弄
    (121.499748,31.256303),  # 东余杭路214弄
    (121.500233,31.256527),  # 东余杭路214弄
    (121.500134,31.257052),  # 东余杭路214弄
    (121.497372,31.255859),  # 九龙路余杭路
    (121.497978,31.255165),  # 九龙路余杭路
    (121.498634,31.255597),  # 九龙路余杭路
    (121.499007,31.255851),  # 九龙路余杭路
    (121.498311,31.256353),  # 九龙路余杭路
    (121.498711,31.255022),  # 九龙路幼儿园
    (121.498738,31.254266),  # 九龙路幼儿园
    (121.498747,31.253606),  # 九龙路幼儿园
    (121.499497,31.253312),  # 九龙路幼儿园
    (121.500000,31.253759),  # 九龙路幼儿园
    (121.499740,31.254361),  # 九龙路幼儿园
    (121.499466,31.254975),  # 九龙路幼儿园
    (121.499649,31.255315),  # 扬子江大厦
    (121.499932,31.254574),  # 扬子江大厦
    (121.500350,31.253895),  # 扬子江大厦
    (121.500880,31.254200),  # 扬子江大厦
    (121.501495,31.254451),  # 扬子江大厦
    (121.501446,31.255153),  # 扬子江大厦
    (121.500732,31.255253),  # 扬子江大厦
    (121.500224,31.255685),  # 扬子江大厦
    (121.499604,31.256006),  # 扬子江大厦
    (121.501900,31.255462),  # 白金府邸
    (121.501572,31.256087),  # 白金府邸
    (121.501720,31.256762),  # 白金府邸
    (121.501720,31.256762),  # 白金府邸
    (121.500902,31.256631),  # 白金府邸
    (121.500979,31.253424),  # 百福小区
    (121.501549,31.253004),  # 百福小区
    (121.501864,31.252514),  # 百福小区
    (121.502591,31.252822),  # 百福小区
    (121.503332,31.253146),  # 百福小区
    (121.502919,31.253826),  # 百福小区
    (121.502304,31.254790),  # 百福小区
    (121.499182,31.253007),  # 南浔路134弄小区
    (121.499380,31.252799),  # 南浔路134弄小区
    (121.499726,31.252382),  # 南浔路134弄小区
    (121.499977,31.251923),  # 南浔路134弄小区
    (121.500759,31.252043),  # 南浔路134弄小区
    (121.501109,31.252197),  # 南浔路134弄小区
    (121.500705,31.252575),  # 南浔路134弄小区
    (121.500121,31.252942),  # 南浔路134弄小区
    (121.499708,31.253212),  # 南浔路134弄小区
    (121.501545,31.252375),  # 平安里
    (121.501329,31.252791),  # 平安里
    (121.500705,31.253204),  # 平安里
    (121.500184,31.253586),  # 平安里
    # ===== Surrounding Area ===== #
    (121.494152,31.259127),  # 吴淞路哈尔滨路
    (121.494394,31.258850),  # 吴淞路哈尔滨路
    (121.495239,31.259154),  # 吴淞路哈尔滨路
    (121.495948,31.259409),  # 吴淞路哈尔滨路
    (121.496676,31.259822),  # 吴淞路哈尔滨路
    (121.496034,31.260019),  # 吴淞路哈尔滨路
    (121.495463,31.260189),  # 吴淞路哈尔滨路
    (121.494906,31.259729),  # 吴淞路哈尔滨路
    (121.494857,31.258209),  # 吴淞路海宁路
    (121.495212,31.257650),  # 吴淞路海宁路
    (121.497642,31.259552),  # 吴淞路海宁路
    (121.495594,31.256707),  # 东兴小区
    (121.495818,31.255909),  # 太保大厦
    (121.496406,31.256203),  # 太保大厦
    (121.496016,31.255345),  # 耀江国际广场
    (121.496218,31.254724),  # 耀江国际广场
    (121.496447,31.253767),  # 耀江国际广场
    (121.497130,31.254435),  # 耀江国际广场
    (121.49726,31.2537410),  # 宝矿国际大厦
    (121.497974,31.253714),  # 宝矿国际大厦
    (121.497974,31.254181),  # 宝矿国际大厦
    (121.496366,31.253119),  # 公安大楼
    (121.496927,31.253042),  # 公安大楼
    (121.497543,31.252899),  # 公安大楼
    (121.497776,31.253262),  # 公安大楼
    (121.496267,31.252625),  # 吴淞路天潼路
    (121.496155,31.251584),  # 吴淞路天潼路
    (121.497139,31.251607),  # 吴淞路天潼路
    (121.497314,31.252305),  # 吴淞路天潼路
    (121.497889,31.251927),  # 吴淞路天潼路
    (121.498369,31.252267),  # 吴淞路天潼路
    (121.498055,31.252637),  # 吴淞路天潼路
    (121.498104,31.251769),  # 上海外滩茂悦大酒店
    (121.498451,31.251337),  # 上海外滩茂悦大酒店
    (121.498823,31.250843),  # 上海外滩茂悦大酒店
    (121.499303,31.250252),  # 上海外滩茂悦大酒店
    (121.499937,31.250588),  # 上海外滩茂悦大酒店
    (121.500525,31.250924),  # 上海外滩茂悦大酒店
    (121.500224,31.251414),  # 上海外滩茂悦大酒店
    (121.499348,31.251796),  # 上海外滩茂悦大酒店
    (121.498899,31.251591),  # 上海外滩茂悦大酒店
    (121.498535,31.252070),  # 上海外滩茂悦大酒店
    (121.501226,31.251267),  # 上海外滩茂悦大酒店
    (121.501972,31.251757),  # 国际港务大厦
    (121.502771,31.252066),  # 国际港务大厦
    (121.504590,31.253760),  # 金光新外滩
    (121.505681,31.254292),  # 金光新外滩
    (121.506984,31.254945),  # 金光新外滩
    (121.506548,31.255662),  # 金光新外滩
    (121.506144,31.256314),  # 金光新外滩
    (121.505484,31.256129),  # 金光新外滩
    (121.504738,31.255878),  # 金光新外滩
    (121.504127,31.255709),  # 金光新外滩
    (121.503296,31.255330),  # 金光新外滩
    (121.503840,31.256164),  # 上海一方大厦
    (121.503579,31.256558),  # 上海一方大厦
    (121.502888,31.256272),  # 上海一方大厦
    (121.502290,31.255998),  # 上海一方大厦
    (121.503301,31.256943),  # 公益里
    (121.503013,31.257298),  # 公益里
    (121.502322,31.257001),  # 公益里
    (121.502735,31.257688),  # 名江七星城
    (121.502479,31.258039),  # 名江七星城
    (121.501599,31.257819),  # 名江七星城
    (121.500867,31.257669),  # 名江七星城
    (121.502196,31.258502),  # 前进小区
    (121.502209,31.259000),  # 前进小区
    (121.502232,31.259509),  # 前进小区
    (121.501468,31.259228),  # 前进小区
    (121.500889,31.259147),  # 前进小区
    (121.500229,31.259872),  # 1933老场坊
    (121.500089,31.260698),  # 1933老场坊
    (121.498365,31.260980),  # 1933老场坊
    (121.498239,31.260343),  # 1933老场坊
    (121.498217,31.259660),  # 1933老场坊
    (121.495674,31.260412),  # 1933老场坊
    (121.496222,31.260972),  # 1933老场坊
    (121.496784,31.261562),  # 1933老场坊
    (121.497224,31.261145),  # 1933老场坊
]

def areas_job():
    data = [[t[0],t[1],50] for t in AREAS]
    df = pd.DataFrame(data, columns=['longitude','latitude','total'])
    path = '/var/www/html/data/bike.json'
    df.to_json(path, orient='records')

def fetch_ofo(lo, la):
    url = 'https://san.ofo.so/ofo/Api/nearbyofoCar'
    headers = {
        'content-type': 'multipart/form-data; boundary=--------FormData44674',
    }
    token = 'e3a4c350-cf2e-11e6-b1c1-a36dafadcafa'
    data = '----------FormData44674\x0d\x0aContent-Disposition: form-data; name=\"token\";\x0d\x0a\x0d\x0a{token}\x0d\x0a----------FormData44674\x0d\x0aContent-Disposition: form-data; name=\"lat\";\x0d\x0a\x0d\x0a{la}\x0d\x0a----------FormData44674\x0d\x0aContent-Disposition: form-data; name=\"lng\";\x0d\x0a\x0d\x0a{lo}\x0d\x0a----------FormData44674--'.format(token=token, la=la, lo=lo)

    r = requests.post(url, headers=headers, data=data, timeout=5)
    data = json.loads(r.text).get('values')
    if not data:
        log.info(r.text)
    else:
        bikes = [{'lo':bike['lng'],'la':bike['lat'],'id':bike['carno']} for bike in data['info']['cars']]
        log.info('Fetch ofo at [{0}, {1}], get {2} bikes in total'.format(lo, la, len(bikes)))
        return bikes

def fetch_mobike(lo, la):
    url = 'https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'https://servicewechat.com/wx80f809371ae33eda/116/',
    }
    data = 'speed=0&errMsg=getLocation%3Aok&longitude={0}&verticalAccuracy=0&latitude={1}&accuracy=30&horizontalAccuracy=30&citycode=021'.format(lo, la)
    r = requests.post(url, headers=headers, data=data, timeout=5)
    data = json.loads(r.text).get('object')
    if not data:
        log.info(r.text)
    else:
        bikes = [{'lo':bike['distX'],'la':bike['distY'],'id':bike['distId']} for bike in data]
        log.info('Fetch mobike at [{0}, {1}], get {2} bikes in total'.format(lo, la, len(bikes)))
        return bikes

def bike_job():
    """
    length = 0.0007
    steps = 20
    min_lo, max_la = 121.494041, 31.264781
    max_lo, min_la = 121.507761, 31.249334
    board = []
    for i in range(steps):
        for j in range(steps):
            lo = min_lo + i * length
            la = max_la - j * length
            box = { 'lo': lo, 'la': la, 'ofo': [], 'mobike': [] }
            board.append(box)
    """
    board = [{'lo':t[0], 'la':t[1], 'ofo':[], 'mobike': []} for t in AREAS]
    for brand in ['mobike', 'ofo']:
        for point in board:
            lo, la = point['lo'], point['la']
            bikes = []
            for i in range(RETRY_TIMES):
                try:
                    if brand == 'mobike':
                        bikes = fetch_mobike(lo, la)
                    if brand == 'ofo':
                        bikes = fetch_ofo(lo, la)
                    break
                except:
                    continue
            for bike in bikes:
                bike_lo = bike['lo']
                bike_la = bike['la']
                bike_id = bike['id']
                min_d = 99999999
                index = None
                for i, point in enumerate(board):
                    dis = (bike_lo-point['lo'])**2 + (bike_la-point['la'])**2
                    if dis < min_d:
                        min_d = dis
                        index = i
                if bike_id not in board[index][brand]:
                    board[index][brand].append(bike_id)
            time.sleep(0.04)
        log.info('Finish fetching {}!'.format(brand))

    t = datetime.now().strftime('%m-%d:%H')
    center_list = [[t, p['lo'], p['la'], len(p['mobike']), len(p['ofo']), len(p['ofo'])+len(p['mobike'])] for p in board]
    path = 'bike_log.xls'
    try:
        history = pd.read_excel(path)
    except:
        history = pd.DataFrame([])
    df = pd.DataFrame(center_list, columns=['create_date','longitude','latitude','mobike','ofo','total'])
    new = pd.concat([history, df])
    new.to_excel(path, index=False)
    new.to_json('/var/www/html/data/bike.json', orient='values')


if __name__ == '__main__':
    if len(sys.argv) >= 2:# and sys.argv[1] == 'test':  # In Test Environment
        log.info('in test')
        during_test = True
        job_name = sys.argv[1] + '_job()'
        eval(job_name)
    else:
        sched = BlockingScheduler()
        bike_trigger = CronTrigger(day_of_week='0-6', hour='0-23')
        sched.add_job(bike_job, bike_trigger)
        sched.start()





