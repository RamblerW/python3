> DataFrame

- 配置
  - 显示全部数据：`pandas.set_option('display.max_rows',None)`
- 查看部分数据
  - `head(count)`：查看前 count 条数据，默认 count = 5
  - `tail(count)`：查看后 count 条数据，默认 count = 5
  - `sample(count)`：随机抽样 count 条数据，默认 count = 1
- 排序
  - 按值排序：`DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')`
- 格式转换
  - 转 datetime ：`df['colName'] = pd.to_datetime(df['colName'], format='%Y-%m-%d')`
- 字符串操作
  - 多列拼接：`df['colName1'].str.cat(df['colName2'])`