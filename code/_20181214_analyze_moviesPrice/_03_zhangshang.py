#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 爬取招行掌上生活APP电影票价
# author: rambler
# datetime: 2019/1/20 18:26
# software: PyCharm
import requests
import datetime
import time
import random
import warnings

import util

# 不输出警告信息
warnings.filterwarnings("ignore")

startTime = datetime.datetime.now()
print('🎉🎉🎉🎉🎉🎉🎉🎉%s🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉' % startTime)

list_result = []
# 获取电影院
url_cinemas = 'https://movie.o2o.cmbchina.com/MovieApi/cinema/allcinema.json'
params_cinemas = {
    'channelId': 1,
    'cityId': 241 # 西安
}
json_cinemas = requests.post(url_cinemas,data=params_cinemas, verify=False).json()
list_cinemas = json_cinemas['respData']['cinemaList']
for item_cinema in list_cinemas:
    id = item_cinema['cinemaId']

    # 获取电影院详情
    url_detail = 'https://movie.o2o.cmbchina.com/MovieApi/cinema/playTime.json'
    params_detail = {
        'channelId': 1,
        'cinemaId': id
    }
    json_detail = ''
    try:
        json_detail = requests.post(url_detail,data=params_detail, verify=False).json()
        time.sleep(random.uniform(5, 10))  # 随机休眠
    except Exception as e:
        # 被禁后休眠60秒再爬
        time.sleep(60)
        json_detail = requests.post(url_detail,data=params_detail, verify=False).json()
    cinema_id = id
    cinema_name = json_detail['respData']['cinemaDetail']['cinemaName']
    # 电影详情
    for item_movie in json_detail['respData']['filmScheduleList']:
        movie_name = item_movie['filmDetail']['filmName']

        # 上映日期
        for item_date in item_movie['scheduleDay']:
            show_date = item_date['playDate']

            # 场次
            for item_time in item_date['scheduleTime']:
                show_time = item_time['startTime']
                price = item_time['salePrice']

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
util.saveData(list_result, 'zhangshang')
endTime = datetime.datetime.now()
print('🎉🎉🎉🎉🎉🎉🎉🎉%s🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉' % endTime)
print('耗时：%s 分钟'%(((endTime - startTime).seconds)/60))