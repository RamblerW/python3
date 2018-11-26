#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 通过tushare获取2018年电影数据
# author: rambler
# datetime: 2018/11/6 19:51
# software: PyCharm

import numpy as np
import pandas as pd
import tushare as ts

# tushare数据集
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
# 设置token
ts.set_token(TOKEN)
# 初始化接口
pro = ts.pro_api()
# 按月取票房数据
dfTushare = pd.DataFrame()
dateList = ['20180101','20180201','20180301','20180401','20180501','20180601',
            '20180701','20180801','20180901','20181001','20181101']
for i in dateList:
    monthDf = pro.bo_monthly(date=i)
    dfTushare = pd.concat([dfTushare,monthDf])
# 过滤掉“其他”
dfTushare = dfTushare[dfTushare['name']!='其他']
#将上映日期转换为日期类型
dfTushare['list_date'] = pd.to_datetime(dfTushare['list_date'])
# 将上映日期设置为index
dfTushare = dfTushare.set_index('list_date')
# 只保留上映日期为2018年的
dfTushare = dfTushare['2018'].sort_values(by='name')
# 把场均人次转为float，用于求平均值
dfTushare['p_pc'] = dfTushare['p_pc'].astype(float)
# 因为数据是按月统计的，所以同一电影可能会有多条记录，所以根据电影名称进行合并
# 删除不需要的字段：月度排名、月内天数、月度占比
dfTushare = dfTushare.drop(['rank','list_day','m_ratio'], axis=1)
# 票房求和（为保留list_date列，所以此处以name和list_date来进行分组）
df1 = dfTushare.groupby(by=['name','list_date'])['month_amount'].sum().reset_index(name='amount')
# 票价、场均人次、口碑指数求均值
df2 = dfTushare.groupby(by='name')['avg_price','p_pc','wom_index'].mean()
# 合并df1和df2
df = pd.merge(df1,df2,left_on='name',right_on='name')

# 保存
df.to_csv('dataTushare2018-11-01.csv',encoding='utf_8_sig')