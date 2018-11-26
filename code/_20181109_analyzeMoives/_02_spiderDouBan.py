#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 根据tushare电影数据中的电影名称，爬取豆瓣2018年电影数据
# author: rambler
# datetime: 2018/11/2 19:27
# software: PyCharm

import urllib.parse
import urllib.request
import requests
import time
import datetime
import numpy as np
import pandas as pd
from lxml import etree
from selenium import webdriver

# 利用selenium获取网页源码
def getHtml(url):

    driver = webdriver.Chrome(executable_path='/Users/rambler/My/tool/chromedriver') # chromedriver本地路径
    driver.get(url)
    html = driver.page_source
    return html

# 获取json对象
def getJsonResult(url, params):
    # 对请求数据进行编码
    data = urllib.parse.urlencode(params).encode(encoding='UTF8')
    # 发送请求，获取返回结果，并转为json（verify=False，关闭https请求的ssl证书验证）
    response_result = requests.get(url, data, verify=False).json()

    return response_result

if __name__ == '__main__':
    # 每次爬取间隔时间：秒
    sleepSeconds = 2
    # 电影主记录页面url
    masterUrl = 'https://movie.douban.com/subject_search?search_text='
    # 电影主页面详情url
    detailUrl1 = 'https://movie.douban.com/j/subject_abstract'
    # 最终结果集
    resultData = []

    dfTushare = pd.read_csv('dataTushare2018-11-01.csv')
    # 获取tushare数据集中的电影名称，并去重
    movieNameValues = dfTushare.groupby(by='name').size().index
    # 爬取主记录
    for movieName in movieNameValues:
        masterHtml = getHtml(masterUrl+movieName)
        # 获取电影的id
        xpathMasterHtml = etree.HTML(masterHtml)
        id = str(xpathMasterHtml.xpath("//div[@class='title']/a/@href")[0]).split('/')[-2]
        htmlname = str(xpathMasterHtml.xpath("//div[@class='title']/a/text()")[0])

        detailParams1 = {
            'subject_id': id
        }
        detailJsonResult1 = getJsonResult(detailUrl1, detailParams1)

        detail1 = detailJsonResult1['subject']
        # 解析字段
        name = movieName  # 影名（tushare）
        title = htmlname  # 影名（豆瓣）
        rate = detail1['rate']  # 评分
        directors = '|'.join(detail1['directors'])  # 导演
        actors = '|'.join(detail1['actors'])  # 主演
        types = '|'.join(detail1['types'])  # 类型
        region = detail1['region']  # 制片国家/地区
        duration = detail1['duration']  # 片长
        url = detail1['url']  # 链接
        release_year = detail1['release_year']  # 年份

        data = {'name':name,'title': title, 'rate': rate, 'directors': directors, 'actors': actors,
                'types': types, 'region': region, 'duration': duration, 'url': url,
                'release_year': release_year}
        print(str(data))
        resultData.append(data)
        # 间隔一段时间再爬取，避免ip被禁
        time.sleep(sleepSeconds)
    # 将数据写入csv文件
    dataframe = pd.DataFrame(resultData)
    # 将DataFrame存储为csv
    columns = ['name',"title", "rate", "directors", "actors", "types", "region", "duration", "url",
               "release_year"]
    dataframe.to_csv("dataDouban" + str(datetime.date.today()) + ".csv", index=False, columns=columns,
                     encoding='utf_8_sig')
    print('over')
