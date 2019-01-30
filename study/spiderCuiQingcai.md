#### 01. 怎样解决javaScript渲染的问题

- 分析Ajax请求
- Selenium / WebDriver
- Splash
- PyV8、Ghost.py

#### 02. Urllib：Python内置的HTTP请求库【==建议使用Requests代替==】

- 包含的模块
  - `urllib.request`：请求模块
  - `urllib.error`：异常处理模块
  - `urllib.parse`：url解析模块
  - `urllib.robotparser`：robots.txt解析模块
- 常用操作
  - 发送请求：`urllib.request.urlopen`

  - 配置代理

    ```python
    import urllib.request
    
    proxy_handler = urllib.request.ProxyHandler({
        'http': 'http://127.0.0.1:9743',
        'https': 'https://127.0.0.1:9743'
    })
    opener = urllib.request.build_opener(proxy_handler)
    response = opener.open('http://httpbin.org/get')
    print(response.read())
    ```

  - 配置 Cookie

    ```python
    import http.cookiejar, urllib.request
    
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    ```

  - URL 解析

    - `urlencode`：编码

      ```python
      from urllib.parse import urlencode
      
      params = {
          'name': 'germey',
          'age': 22
      }
      base_url = 'http://www.baidu.com?'
      url = base_url + urlencode(params)
      print(url)
      ```

    - `urlparse`：拆分 url

      ```python
      from urllib.parse import urlparse
      
      result = urlparse('http://www.baidu.com/index.html;user?id=5#comment', scheme='https')
      ```

    - `urlunparse`：拼接 url

      ```python
      from urllib.parse import urlunparse
      
      data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
      print(urlunparse(data))
      ```

    - `urljoin`：合并 url

      ```python
      from urllib.parse import urljoin
      
      print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
      print(urljoin('http://www.baidu.com', '?category=2#comment'))
      ```

#### 03. Requests：Python实现的基于urllib3的HTTP库

- get请求

  - 基本：`requests.get('http://httpbin.org/get')`

  - 带参数
    - 拼接到url中：`requests.get('http://httpbin.org/get?name=germey&age=22')`
    - 直接传参（参数为data）：`requests.get('http://httpbin.org/get',params=data)`

  - 解析json：`requests.get('http://httpbin.org/get').json()`

  - 获取二进制数据

    ```python
    import requests
    
    response = requests.get('https://github.com/favicon.ico')
    with open('favicon.ico','wb') as f:
        f.write(response.content)
        f.close()
    ```

  - 添加headers（headers为header）：`requests.get('https://zhihu.com/explore',headers=header)`

- post请求

  ```python
  import requests
  import json
  
  data = {'name': 'germey', 'age': '22'}
  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
  }
  response = requests.post("http://httpbin.org/post", data=data, headers=headers)
  # 如果body需要json形式，需要对data做处理
  # data = json.dumps(data)
  print(response.json())
  ```

- 响应

  - response
    - 状态码：`response.status_code`
    - headers：`response.headers`
    - cookies：`response.cookies`
    - url：`response.url`
    - 请求历史（可用于追踪重定向）：`response.history`

- 高级操作

  - 文件上传

    ```python
    import requests
    
    files = {'file': open('favicon.ico', 'rb')}
    response = requests.post("http://httpbin.org/post", files=files)
    print(response.text)
    ```

  - 获取cookies

    ```python
    import requests
    
    response = requests.get("https://www.baidu.com")
    print(response.cookies)
    for key, value in response.cookies.items():
        print(key + '=' + value)
    ```

  - session：会话维持

    ```python
    import requests
    
    s = requests.Session()
    s.get('http://httpbin.org/cookies/set/number/123456789')
    response = s.get('http://httpbin.org/cookies')
    print(response.text)
    ```

  - 证书验证

    - 不验证证书：`requests.get('https://www.12306.cn', verify=False)`
    - 指定证书：`requests.get('https://www.12306.cn', cert=('/path/server.crt', '/path/key'))`

  - 代理设置：`requests.get("https://www.taobao.com", proxies=proxies)`

    - http/https：

      ```python
      # 不登录
      proxies = {
        "http": "http://127.0.0.1:9743",
        "https": "https://127.0.0.1:9743",
      }
      # 登录
      proxies = {
          "http": "http://user:password@127.0.0.1:9743/",
      }
      ```

    - socks：`pip3 install 'requests[socks]'`

      ```python
      proxies = {
          'http': 'socks5://127.0.0.1:9742',
          'https': 'socks5://127.0.0.1:9742'
      }
      ```

  - 超时设置（timeout）：`requests.get("http://httpbin.org/get", timeout = 0.5)`
  - 认证设置
    - `requests.get('http://120.27.34.24:9001', auth=HTTPBasicAuth('user', '123'))`
    - `requests.get('http://120.27.34.24:9001', auth=('user', '123'))`
  - 异常处理：==建议先捕获子类异常，最后捕获父类异常==

#### 04. 正则表达式：字符串的一种过滤逻辑

- 常见匹配模式

  | 模式     | 描述                                                         |
  | -------- | ------------------------------------------------------------ |
  | \w       | 匹配字母数字及下划线                                         |
  | \W       | 匹配非字母数字下划线                                         |
  | \s       | 匹配任意空白字符，等价于 [\t\n\r\f]                          |
  | \S       | 匹配任意非空字符                                             |
  | \d       | 匹配任意数字，等价于 [0-9]                                   |
  | \D       | 匹配任意非数字                                               |
  | \A       | 匹配字符串开始                                               |
  | \Z       | 匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串   |
  | \z       | 匹配字符串结束                                               |
  | \G       | 匹配最后匹配完成的位置                                       |
  | \n       | 匹配一个换行符                                               |
  | \t       | 匹配一个制表符                                               |
  | ^        | 匹配字符串的开头                                             |
  | $        | 匹配字符串的末尾                                             |
  | .        | 匹配除了换行符的任意字符，当re.DOTALL标记被指定时，则可以匹配任意字符 |
  | [...]    | 用来表示一组字符，单独列出：[amk] 匹配 'a'，'m'或'k'         |
  | [^...]   | 不在[]中的字符：[\^abc] 匹配除了a,b,c之外的字符              |
  | *        | 匹配0个或多个的表达式                                        |
  | +        | 匹配1个或多个的表达式，默认为贪婪方式                        |
  | ?        | 匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式         |
  | {n}      | 精确匹配n个前面表达式                                        |
  | {n, m}   | 匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式         |
  | a&#124;b | 匹配a或b                                                     |
  | ( )      | 匹配括号内的表达式，也表示一个组                             |

- `re.match(pattern, string, flags=0)`：从字符串==起始位置==开始匹配

  - 匹配时忽略换行符：`re.match(pattern, string, re.S)`
  - 获取匹配结果：`result.group(index)`，index为匹配模式中括号的位置，从1开始

- `re.search(pattern, string, flags=0)`：扫描整个字符串并返回第一个成功的匹配

==总结：为匹配方便，能用search就不用match==

- `re.findall(pattern, string, flags=0)`：搜索字符串，以列表形式返回全部能匹配的子串，每一组子串为一个元组
- `re.sub(pattern, repl, string)`：替换字符串中所有匹配的子串后，返回替换后的字符串
- `re.compile(pattern, flags=0)`：将正则表达式编译成正则对象，以==便于复用==

#### 05. BeautifulSoup：灵活又方便的网页解析库

- 解析器

  - `BeautifulSoup(markup, "html.parser")`：python内置标准库
  - `BeautifulSoup(markup, "lxml")`：lxml HTML解析器，速度快、容错能力强
  - `BeautifulSoup(markup, "xml")`：lxml XML解析器，速度快、唯一支持XML的解析器
  - `BeautifulSoup(markup, "html5lib")`：html5lib解析器，容错能力最强、速度慢

- 基本使用

  ```python
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html, 'lxml')
  # 格式化输出(会自动补全缺失的闭合标签)
  print(soup.prettify())
  # 支持嵌套选择(对查找到的结果再进行bs4查找)
  print(soup.head.title.string)
  ```

- 标签选择器（==只会返回第一个匹配结果==）

  - 选择元素：`soup.标签名`（选取的结果中会含有标签）
  - 获取标签名称：`soup.标签名.name`
  - 获取属性：`soup.标签名[属性名]`或`soup.标签名.attrs[属性名]`
  - 获取内容：`soup.标签名.string`
  - 获取子节点
    - 结果为列表：`soup.标签名.contents`
    - 结果为迭代器：`soup.标签名.children`
  - 获取所有后代节点：`soup.标签名.descendants`，先深度遍历再广度遍历
  - 获取父节点
    - 获取直接父节点：`soup.标签名.parent`
    - 获取所有父节点：`soup.标签名.parents`
  - 获取兄弟节点
    - 向前查找：`soup.标签名.previous_siblings`
    - 向后查找：`soup.标签名.next_siblings`

- 标准选择器：可根据标签名、属性、内容查找文档

  - `find_all(name , attrs , recursive , text , **kwargs)`
    - 根据名称获取：`soup.find_all('ul')`
    - 根据属性获取
      - `soup.find_all(attrs={'class': 'element'})`
      - `soup.find_all(class_='element')`
    - 根据内容获取：`soup.find_all(text='Foo')`
  - `find( name , attrs , recursive , text , **kwargs )`：等同于 `find_all(limit=1)`
  - `find_parents()` & `find_parent()`：获取所有祖先节点 & 直接父节点
  - `find_next_siblings()` & `find_next_sibling()`：获取后面所有兄弟节点 & 第一个兄弟节点
  - `find_previous_siblings()` & `find_previous_sibling()`：获取前面所有兄弟节点 & 第一个兄弟节点
  - `find_all_next()` & `find_next()`：获取后面所有符合条件的节点 & 第一个符合条件的节点
  - `find_all_previous` & `find_previous()`：获取前面所有符合条件的节点 & 第一个符合条件的节点

- CSS 选择器：通过`select()`直接传入CSS选择器即可完成选择

  - 基本使用：`soup.select('ul')`、`soup.select('#list-2 .element')`
  - 获取属性：`soup.select('ul').attrs['id']` 或 `soup.select('ul')['id']`
  - 获取内容：`soup.select('li').get_text()`

- ==总结==

  - ==推荐使用lxml解析库，必要时使用html.parser==
  - ==标签选择筛选功能弱但是速度快==
  - ==建议使用find()、find_all() 查询匹配单个结果或者多个结果==
  - ==如果对CSS选择器熟悉建议使用select()==
  - ==记住常用的获取属性和文本值的方法==

#### 06. PyQuery： 类JQuery的Python库

- 初始化：字符串初始化、URL初始化、文件初始化

  ```python
  from pyquery import PyQuery as pq
  # 字符串初始化
  doc = pq(htmlStr)
  # url初始化
  doc = pq(url='http://www.baidu.com')
  # 文件初始化
  doc = pq(filename='demo.html')
  ```

- 基本CSS选择器：`doc('#container .list li')`

- 查找元素

  - 子元素
    - `doc('ul').find('li')`
    - `doc('ul').children()`
    - `doc('li').children('.active')`
  - 父元素
    - `doc('ul').parent()`：获取直接父元素
    - `doc('ul').parents()`：获取所有祖先元素
  - 兄弟元素
    - `doc('ul').siblings()`
    - `doc('ul').siblings('.active')`

- 遍历：`for li in doc('li').items()`

- 获取信息

  - 获取属性：`doc('ul').attr('href')` 或 `doc('ul').attr.href`
  - 获取文本：`doc('ul').text()`
  - 获取html：`doc('ul').html()`

- DOM 操作

  - addClass、removeClass：`doc('li').addClass('avtive')`
  - attr：`doc('li').attr('name','link')`
  - css：`doc('li').css('font-size','14px')`
  - remove：`doc('ul').find('p').remove()`
  - 其他DOM方法：http://pyquery.readthedocs.io/en/latest/api.html

- 伪类选择器

  - 获取第一个元素：`doc('li:first-child')`
  - 获取最后一个元素：`doc('li:last-child')`
  - 获取第二个元素：`doc('li:nth-child(2)')`
  - 获取包含指定文本的元素：`doc('li:contains(second)')`

#### 07. Selenium：自动化测试工具

- 基本使用

  ```python
  from selenium import webdriver
  
  browser = webdriver.Chrome()
  # browser = webdriver.Firefox()
  # browser = webdriver.Edge()
  # browser = webdriver.PhantomJS()
  # browser = webdriver.Safari()
  try:
      browser.get('https://www.baidu.com')
      input = browser.find_element_by_id('kw') # 查找元素
      input.send_keys('Python') # 输入文本
      input.send_keys(Keys.ENTER) # 回车
      print(browser.page_source) # 输出网页源代码
  finally:
      browser.close() # 关闭
  ```

- 查找元素（rex为对应的表达式）

  - `browser.find_element_by_id('rex')` 或 `browser.find_element(By.ID, 'rex')`（下同）
  - `browser.find_element_by_name('rex')`
  - `browser.find_element_by_xpath('rex')`
  - `browser.find_element_by_link_text('rex')`
  - `browser.find_element_by_partial_link_text('rex')`
  - `browser.find_element_by_tag_name('rex')`
  - `browser.find_element_by_class_name('rex')`
  - `browser.find_element_by_css_selector('rex')`
  - 查找单个元素：`find_element_by……`
  - 查找多个元素：`find_elements_by……`

- 元素交互操作：对获取的元素调用交互方法

  - 输入：`input.send_keys('iphone')`
  - 清空：`input.clear()`
  - 点击：`button.click()`
  - 更多操作：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement

- 交互动作：将动作附加到动作链中串行执行

  ```python
  source = browser.find_element_by_css_selector('#draggable1')
  target = browser.find_element_by_css_selector('#draggable2')
  actions = ActionChains(browser)
  # 把source元素拖拽到target元素处
  actions.drag_and_drop(source, target)
  # 执行动作
  actions.perform()
  ```

  更多操作： http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains

- 执行 JavaScript：`browser.execute_script('alert("hello world")')`

- 获取元素信息

  - 获取属性：`browser.find_element_by_id('zh-top-link-logo').get_attribute('class')`
  - 获取文本：`browser.find_element_by_id('zh-top-link-logo').text`
  - 获取ID：`browser.find_element_by_id('zh-top-link-logo').id`
  - 获取位置：`browser.find_element_by_id('zh-top-link-logo').location`
  - 获取标签名：`browser.find_element_by_id('zh-top-link-logo').tag_name`
  - 获取大小：`browser.find_element_by_id('zh-top-link-logo').size`

- Frame

  - 跳转到指定Frame：`browser.switch_to.frame('iframeResult')`
  - 跳转到父Frame：`browser.switch_to.parent_frame()`

- 等待

  - 隐式等待：当查找元素或元素并没有立即出现时，隐式等待将等待一段时间后再次查找，默认时间为0

    ```python
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    ```

  - 显式等待：满足指定条件才执行后续代码

    ```python
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')
    wait = WebDriverWait(browser, 10)
    input = wait.until(EC.presence_of_element_located(By.ID, 'q'))
    ```

    - title_is：标题是某内容
    - title_contains ：标题包含某内容
    - presence_of_element_located：元素加载出，传入定位元组，如(By.ID, 'p')
    - visibility_of_element_located ：元素可见，传入定位元组
    - visibility_of：可见，传入元素对象
    - presence_of_all_elements_located：所有元素加载出
    - text_to_be_present_in_element：某个元素文本包含某文字
    - text_to_be_present_in_element_value ：某个元素值包含某文字
    - frame_to_be_available_and_switch_to_it ：frame加载并切换
    - invisibility_of_element_located：元素不可见
    - element_to_be_clickable ：元素可点击
    - staleness_of ：判断一个元素是否仍在DOM，可判断页面是否已经刷新
    - element_to_be_selected ：元素可选择，传元素对象
    - element_located_to_be_selected ：元素可选择，传入定位元组
    - element_selection_state_to_be： 传入元素对象以及状态，相等返回True，否则返回False
    - element_located_selection_state_to_be ：传入定位元组以及状态，相等返回True，否则返回False
    - alert_is_present：是否出现Alert
    - 详细内容：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions

- 前进：`browser.forward()`

- 后退：`browser.back()`

- Cookies：`browser.get_cookies()`

- 选项卡管理

  - 打开新选项卡：`browser.execute_script('window.open()')`
  - 获取所有选项卡：`browser.window_handles`
  - 选择指定选项卡：`browser.switch_to_window(browser.window_handles[0])`