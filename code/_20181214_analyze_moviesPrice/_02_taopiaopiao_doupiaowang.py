#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 爬取淘票票电影票价（淘票票太难爬了，爬取交行APP中电影的数据-来源于斗票网）
# author: rambler
# datetime: 2019/1/20 17:48
# software: PyCharm
import requests
import urllib
import datetime
import time
import random
import warnings
from lxml.html import etree

import util

# 不输出警告信息
warnings.filterwarnings("ignore")

startTime = datetime.datetime.now()
print('🎉🎉🎉🎉🎉🎉🎉🎉%s🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉' % startTime)

list_result = []

# 获取电影院
url_cinemas = 'https://bankcomm.doupiaowang.com/xbankcommfilm/cinema/cinemas?cityId=12&longitude=121.4834974484&latitude=31.237037783&sort=1&orderType=2'
list_cinemas = requests.post(url_cinemas, verify=False).json()['data']['cinemalist']
# {
#     "compareCount": 2,
#     "address": "高新区瑞达路木兰里9号睿达广场3楼",
#     "distance": 837.2,
#     "latitude": "121.4834974484",
#     "showTime": "2019-01-29 12:35:00",
#     "comparedNames": [
#         "baidu",
#         "taobao"
#     ],
#     "lowPrice": 2790,
#     "price": 27.9,
#     "minPrice": 27.9,
#     "jbzShowTime": "2019-01-29 12:35",
#     "name": "中影星美国际影城（郑州睿达店）",
#     "id": "817450",
#     "longitude": "31.237037783"
# }
for item in list_cinemas:
    cinema_id = item['id']
    cinema_name = item['name']

    # 获取电影院详细信息
    url_detail = 'https://bankcomm.doupiaowang.com/xbankcommfilm/cinema/films?cinemaId=' + str(cinema_id)
    json_detail = requests.post(url_detail, verify=False).json()['data']
    # 电影详情
    for item_movie in json_detail['films']:
        movie_name = item_movie['name']
        movie_id = item_movie['id']

        # 上映日期
        url_showDate = 'https://bankcomm.doupiaowang.com/xbankcommfilm/cinema/filmshowdates?cinemaId=' + str(cinema_id)+'&filmId='+str(movie_id)
        json_showDate = requests.post(url_showDate, verify=False).json()['data']['filmShowDates']
        for item_date in json_showDate:

            # 场次
            url_time = 'https://bankcomm.doupiaowang.com/xbankcommfilm/cinema/filmshows?cinemaId=' + str(cinema_id)+'&filmId='+str(movie_id)+'&date='+ str(item_date)
            json_time = requests.post(url_time, verify=False).json()['data']
            for item_time in json_time['filmShows']:
                for item_session in item_time['showItems']:
                    # {
                    #     "showId": "617615074",
                    #     "showDate": "2019-01-29",
                    #     "showTime": "2019-01-29 10:00",
                    #     "type": "taobao",
                    #     "language": null,
                    #     "price": 26.9,
                    #     "orderPrice": 26.9,
                    #     "hallName": "3号激光厅（前台入会首张免费）",
                    #     "dimensional": "国语 2D",
                    #     "cinemaId": "57720",
                    #     "filmId": "1289939",
                    #     "hallId": null,
                    #     "imax": null,
                    #     "vip": null,
                    #     "love": null,
                    #     "priority": 1
                    # }
                    type = item_session['type']
                    if(type != 'taobao'):
                        continue
                    show_time = item_session['showTime']
                    price = item_session['price']
                    # 保存数据
                    item_result = {
                        '_id': len(list_result),
                        'cinema_id': cinema_id,
                        'cinema_name': cinema_name,
                        'movie_name': movie_name,
                        'show_date': item_date,
                        'show_time': show_time,
                        'price': price
                    }
                    list_result.append(item_result)
                    print(len(list_result), datetime.datetime.now(), cinema_name, movie_name, item_date, show_time)
# 保存到数据库
util.saveData(list_result, 'taopiaopiao_doupiaowang')
endTime = datetime.datetime.now()
print('🎉🎉🎉🎉🎉🎉🎉🎉%s🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉' % endTime)
print('耗时：%s 分钟'%(((endTime - startTime).seconds)/60))