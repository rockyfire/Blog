# BlogDemo

上个月学习Django 真的只是学习而已,很多东西学完就忘记了.从八月头开始学习爬虫,学习的路径:[从零开始写Python爬虫](https://zhuanlan.zhihu.com/Ehco-python)

这位博主是个文科生还和我同一届,羞愧,回首我这三年都学了啥,好像什么都没学.算了还是一本正经的说计划吧

学了十几天的爬虫,浅读requests和beautifulsoup4文档,爬取百度贴吧的图片,了解IP代理和User-agent,
使用Scrapy爬取天气信息.使用Selenium登入学校的正方教务系统.尝试在电脑上安装python的验证码识别工具tesseract失败,原因是giflib库太高级使用不了.

现在才开始讲重点,看到博主的[requests+django实现微信公众号](https://zhuanlan.zhihu.com/p/27625233)于是萌生了一个想法

大三下学期学习Liunx,Git,重温MySQL,个人建站的笔记,大部分以笔记的形式保存在印象笔记中,每次要看的时候都要打开印象笔记APP,麻烦.

不如把这些笔记转移到自己开发的Django博客中,微信公众号和博客对接,这样以后开微信就可以看到,方便

第一步,博客                              

第二步,微信公众号 

通过微信服务器转发到你的自己的服务器,这中间可能有个小错误要注意一下,Django有一个csrf保护机制([跨站点伪造请求](http://www.cnblogs.com/lins05/archive/2012/12/02/2797996.html)),验证Token的时候没有事情,是因为是使用Get请求发送的,但是post请求发送的就不行了,这就必须在weixin/views.py中加入@csrf_exempt

在我的项目中启用了Django的loggings,loggings指定的输出文件中最好不要修改其内容,修改的话要重启Django开可以重新写入日志.

第三步,搬运笔记

本来是想调用印象笔记的API,快速写入到我的博客中,但是印象笔记开放的测试API是对 https://sandbox.evernote.com 这个网站的不是https://www.yinxiang.com/ 这就很尴尬了.

第四步,博客和微信公众号对接


参考

[追梦人的博客](http://zmrenwu.com/)

[安装web.py出错解决](https://github.com/webpy/webpy/issues/396)

