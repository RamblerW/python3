#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 爬取微信端猫眼电影票价
# author: rambler
# datetime: 2019/1/20 16:02
# software: PyCharm
import requests
import datetime
import time
import random
import warnings

import util

# 不输出警告信息
warnings.filterwarnings("ignore")

list_result = []

startTime = datetime.datetime.now()
print('🎉🎉🎉🎉🎉🎉🎉🎉%s🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉' % startTime)
# 获取电影院
url_cinemas = 'https://wx.maoyan.com/hostproxy/mmcs/cinema/v1/select/movie/cinemas.json?ci=42&cityId=42&limit=1000'
list_cinemas = requests.get(url_cinemas, verify=False).json()['data']['cinemas']
for item in list_cinemas:
    id = item['id']

    # 获取电影院详细信息
    url_detail = 'https://wx.maoyan.com/hostproxy/mmcs/show/v2/cinema/shows.json?&ci=42&cinemaId=' + str(id)
    json_detail = ''
    try:
        json_detail = requests.get(url_detail, verify=False).json()['data']
    except Exception as e:
        try:
            # 被禁后休眠60秒再爬
            time.sleep(60)
            json_detail = requests.get(url_detail, verify=False).json()['data']
        except Exception as e:
            # 被禁后休眠60秒再爬
            time.sleep(60)
            json_detail = requests.get(url_detail, verify=False).json()['data']
    cinema_id = id
    cinema_name = json_detail['cinemaName']
    # 电影详情
    for item_movie in json_detail['movies']:
        movie_name = item_movie['nm']

        # 上映日期
        for item_date in item_movie['shows']:
            show_date = item_date['showDate']

            # 场次
            for item_time in item_date['plist']:
                show_time = item_time['tm']
                price = item_time['sellPr']

                # 保存数据
                item_result = {
                    '_id': len(list_result),
                    'cinema_id': cinema_id,
                    'cinema_name': cinema_name,
                    'movie_name': movie_name,
                    'show_date': show_date,
                    'show_time': show_time,
                    'price': price
                }
                list_result.append(item_result)
                print(len(list_result), datetime.datetime.now(), cinema_name, movie_name, show_date, show_time)
# 保存到数据库
util.saveData(list_result, 'maoyan_wechat')
endTime = datetime.datetime.now()
print('🎉🎉🎉🎉🎉🎉🎉🎉%s🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉' % endTime)
print('耗时：%s 分钟'%(((endTime - startTime).seconds)/60))
