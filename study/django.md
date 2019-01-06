- 安装环境

  - django：`pip install django`
  - 查看django版本：`python -m django --version`
  - django rest framework：`pip install djangorestframework`
  - markdown：`pip install markdown`（Markdown support for the browsable API）
  - django filter：`pip install django-filter`（Filtering support）
  - mysql驱动：`pip install mysqlclient`
  - （可选）图片处理包：`pip install pillow`

- 新建项目

  - PyCharm：New Project → Django
  - 命令行：`django-amdin startproject 项目名`

- 项目结构

  - 项目名：项目的一个容器，包含项目最基本的一些配置
    - \_\_init_\_.py：python中声明模块的文件，内容默认为空
    - settings.py：总配置文件，包含了数据库、Web应用、时间等各种配置
    - urls.py：URL配置文件，配置项目中所有地址页面的URL
    - wsgi.py：python服务器网关接口，python应用与web服务器的接口
  - templates：用于放置html文件
  - manage.py：项目管理器，与项目进行交互的命令行工具集入口
    - `python manage.py`：用于查看所有命令
    - `python manage.py runserver [端口号，默认8000]`：启动服务器

- 新建APP：==创建完成后，添加应用名到settings.py中的 INSTALLED_APPS 中==

  - PyCharm：Tools → Run manage.py Task…，`startapp app名`
  - 命令行：`python manage.py startapp app名`

- 应用结构

  - migrations：数据移植（迁移）模块，内容自动生成
    - \_\_init_\_.py
  - \_\_init_\_.py
  - admin.py：该应用的后台管理系统配置
  - apps.py：该应用的一些配置，django1.9以后自动生成
  - models.py：数据模块，使用ORM框架，类似于MVC中的models
  - tests.py：自动化测试模块，用于编写测试脚本
  - views.py：执行响应、处理逻辑的代码

- Templates

  - HTML文件
  - 默认使用Django模板语言（Django Template Language, DTL）
  - 可以使用第三方模板（如 Jinja2）
  - 常用操作
    - 引用变量：`{{变量名}}`
    - for循环：`{% for i in 数据集 %}`、`{% endfor %}`
    - 超链接地址：`{% url 'app_name:url_name' param %}`
    - 过滤器：`{{ value | filter1 | filter2 …… }}`

- Models

  - 通常，一个Model对应数据库的一张表
  - Django中Models以类的形式表现
  - 它包含了一些基本字段以及数据的一些行为

- Admin

  - Django自带的自动化数据管理界面

  - 被授权的用户可直接在Admin中管理数据库

  - Django提供了许多针对Admin的定制功能

  - 常用操作

    - 创建超级用户：`python manage.py createsuperuser`

    - 访问地址：http://localhost:8000/admin

    - 设置语言为中文：settings.py中`LANGUAGE_CODE = 'zh_Hans'`

    - 配置应用

      1. 在应用下admin.py中引入自身的models模块
      2. 编辑admin.py：`admin.site.register(模块名)`

    - 修改Admin页面中数据默认显示

      ```python
      # models.py中
      def __str__(self):
          # 返回要显示的字段，如
          return self.title
      ```

- Django shell：django项目命令交互工具，启动命令：`python manage.py shell`

- ==注意==

  - ==配置URL时注意在末尾加 /==
  - ==APP下Templates中创建以APP命名的目录来存放html文件，避免Templates冲突==
  - ==post表单提交CSRF问题处理：form中添加语句==`{% csrf_token %}`

---

参考资料：

1. 慕课网课程 | Django入门与实践：https://www.imooc.com/learn/790
2. 慕课网实战课程 | Python前后端分离开发Vue+Django REST framework实战：https://coding.imooc.com/class/131.html
3. django Rest Framework官方文档：https://www.django-rest-framework.org/