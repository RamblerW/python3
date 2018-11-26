#### Q：报错 SSL: CERTIFICATE_VERIFY_FAILED

R：当使用urllib.urlopen打开一个 https 链接时，会验证一次 SSL 证书。

A：针对urllib.urlopen，增加参数```context=context```

```python
import ssl
context = ssl._create_unverified_context()
webPage = urllib.request.urlopen(req,context=context)
```
针对 requests.get/post，增加参数```verify=False```
```python
response_result = requests.get(url,data,verify=False)
```

#### Q：报错 UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte

R：请求的header中含有'Accept-Encoding': 'gzip, deflate'，这句话的意思是本地接收压缩格式的数据，浏览器能够自动解压，程序却不能自动解压。

A：删掉 header 中的 Accept-Encoding

#### Q： pandas 的 to_csv() 方法写入csv中文乱码

A：to_csv()中添加参数 _encoding='utf_8_sig'

#### Q：pandas 表格显示不全，只显示了部分行或者部分列

A：通过```pd.set_option('display.max_rows', None)```设置pandas显示的最大行数，None 为不限制

#### Q：wordcloud 词云图中文显示为方块

R：wordcloud默认是不支持中文的

A：通过```font_path```给wordcloud指定一种支持中文的字体文件

```python
wordcloud = WordCloud(font_path='resources/msyh.ttf')
```

#### Q：wordcloud 底图不能识别

R：png格式图片作为底图是不能被识别的，即使强行把图片后缀改为jpg也不行

A：（最好）找jpg格式的图片作为底图

#### Q：Mac 安装pyecharts时报错 failed building wheel for dukpy

A：需要安装一个xcode的命令行工具，链接：https://developer.apple.com/download/more/?name=for%20Xcode，如果还不行的话，再安装一下xcode。

#### Q：pyecharts 使用 for 循环画折线图，图表不显示

A：创建 Page 对象，将每个 Line 添加到 Page 中来显示。
```python
page = pyecharts.Page()
line = pyecharts.Line("多折线图")
for item in df1.columns:
    line.add(item,df1.index.tolist(),df1[item].tolist(),is_datazoom_show=True)
    page.add(line)
page
```