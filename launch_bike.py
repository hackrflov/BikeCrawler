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
log = logging.basicConfig()

def fetch_ofo(lo, la):
    url = 'https://san.ofo.so/ofo/Api/nearbyofoCar'
    headers = {
        'content-type': 'multipart/form-data; boundary=--------FormData44674',
    }
    token = 'e3a4c350-cf2e-11e6-b1c1-a36dafadcafa'
    print 'Fetching ofo: ', lo, la
    data = '----------FormData44674\x0d\x0aContent-Disposition: form-data; name=\"token\";\x0d\x0a\x0d\x0a{token}\x0d\x0a----------FormData44674\x0d\x0aContent-Disposition: form-data; name=\"lat\";\x0d\x0a\x0d\x0a{la}\x0d\x0a----------FormData44674\x0d\x0aContent-Disposition: form-data; name=\"lng\";\x0d\x0a\x0d\x0a{lo}\x0d\x0a----------FormData44674--'.format(token=token, la=la, lo=lo)

    r = requests.post(url, headers=headers, data=data)
    data = json.loads(r.text).get('values')
    if not data:
        print r.text
    else:
        cars = data['info']['cars']
        print 'Fetch {} cars in total'.format(len(cars))
        return cars

def fetch_mobike(lo, la):
    url = 'https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'https://servicewechat.com/wx80f809371ae33eda/116/',
    }
    data = 'speed=0&errMsg=getLocation%3Aok&longitude={0}&verticalAccuracy=0&latitude={1}&accuracy=30&horizontalAccuracy=30&citycode=021'.format(lo, la)
    r = requests.post(url, headers=headers, data=data)
    data = json.loads(r.text).get('object')
    print 'Fetching mobike: ', lo, la
    if not data:
        print r.text
    else:
        cars = data
        print 'Fetch {} cars in total'.format(len(cars))
        return cars

def bike_job():
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
    for point in board:
        bikes = fetch_ofo(point['lo'], point['la'])
        for bike in bikes:
            bike_lo = bike['lng']
            bike_la = bike['lat']
            bike_id = bike['carno']
            min_d = 99999999
            index = None
            for i, point in enumerate(board):
                dis = abs(bike_lo-point['lo'])**2 + abs(bike_la-point['la'])**2
                if dis < min_d:
                    min_d = dis
                    index = i
            if bike_id not in board[index]['ofo']:
                board[index]['ofo'].append(bike_id)
        time.sleep(0.1)
    print 'Finish fetching ofo!'
    for point in board:
        bikes = fetch_mobike(point['lo'], point['la'])
        for bike in bikes:
            bike_lo = bike['distX']
            bike_la = bike['distY']
            bike_id = bike['distId']
            min_d = 99999999
            index = None
            for i, point in enumerate(board):
                dis = abs(bike_lo-point['lo'])**2 + abs(bike_la-point['la'])**2
                if dis < min_d:
                    min_d = dis
                    index = i
            if bike_id not in board[index]['mobike']:
                board[index]['mobike'].append(bike_id)
        time.sleep(0.1)
    print 'Finish fetching mobike!'
    t = datetime.now()
    center_list = [[t, p['lo'], p['la'], len(p['ofo']), len(p['mobike']), len(p['ofo'])+len(p['mobike'])] for p in board]
    path = 'bike_log.xls'
    try:
        history = pd.read_excel(path)
    except:
        history = pd.DataFrame([])
    df = pd.DataFrame(center_list, columns=['create_date','longitude','latitude','mobike','ofo','total'])
    new = pd.concat([history, df])
    new.to_excel(path, index=False)

if __name__ == '__main__':
    if len(sys.argv) >= 2:# and sys.argv[1] == 'test':  # In Test Environment
        print 'in test'
        during_test = True
        job_name = sys.argv[1] + '_job()'
        eval(job_name)
    else:
        sched = BlockingScheduler()
        bike_trigger = CronTrigger(day_of_week='0-6', hour='0-23', minute='0,30')
        sched.add_job(bike_job, bike_trigger)
        sched.start()





