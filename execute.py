from scrapy import cmdline

#cmdline.execute('scrapy crawl Document'.split())  #获取所有的页面连接
cmdline.execute('scrapy crawl mbg'.split())  #获取书连接
# cmdline.execute('scrapy check test'.split())  #测试
# cmdline.execute('scrapy settings --get CONCURRENT_REQUESTS'.split())  #查看爬虫并发




