#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 汇总豆瓣和tushare数据
# author: rambler
# datetime: 2018/11/6 20:36
# software: PyCharm

import numpy as np
import pandas as pd
import re

# 豆瓣数据集
# name:tushare数据集中的电影名称，title：豆瓣网中的电影名，rate：评分，directors：导演，actors：主演，
# types：类型，region：制片国家/地区，duration：片长，url：链接
dfDouban = pd.read_csv('dataDouban2018-11-06.csv')
# 时长转换为数字
durationTime = []
for index, row in dfDouban.iterrows():
    dfDouban.set_value(index,'duration',float(re.sub("\D","",'0' if pd.isnull(row['duration']) else row['duration'])))

# tushare数据集
# date：日期，name：影片名称，list_date：上映日期，avg_price：平均票价，month_amount：当月票房（万），
# list_day：月内天数，p_pc：场均人次，wom_index：口碑指数，m_ratio：月度占比（%），rank：排名
dfTushare = pd.read_csv('dataTushare2018-11-01.csv')

# 合并
df = pd.merge(dfTushare,dfDouban,left_on='name',right_on='name',how='left')
df.to_csv('data2018-11-06.csv',encoding='utf_8_sig')