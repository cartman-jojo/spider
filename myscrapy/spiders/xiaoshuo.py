# -*- coding: utf-8 -*-
import scrapy,os
# from bs4 import BeautifulSoup
from myscrapy.items import MyscrapyItem,BookItem
from urllib.parse import urljoin
from scrapy.loader import *
from scrapy.loader.processors import *
from scrapy.http.request.form import FormRequest
from scrapy.http import Request
import json


class DocumentSpider(scrapy.Spider):
    name = 'Document'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/']
    def parse(self, response):
        tilelist=[]
        itemloader=ItemLoader(item=MyscrapyItem(),response=response)
        itemloader.add_xpath('title','//*[@id="channel-header"]/div/nav/ul/li/a/text()')
        itemloader.add_xpath('href','//*[@id="channel-header"]/div/nav/ul/li/a/@href')
        tileinfo=dict(zip(itemloader.load_item()['title'],itemloader.load_item()['href']))
        tileinfo.popitem()
        with open('./title.txt','w+') as f:
            for k in tileinfo:
                f.write(k+":"+tileinfo[k]+'\n')
                tilelist.append(tileinfo[k])
        if os.path.exists('./allurl.txt'):
            os.remove('./allurl.txt')
        for url in tilelist:
            yield scrapy.Request((url),callback=self.parse_level2)
    def parse_level2(self,response):
        urlmod=response.xpath('//*[@id="pagelink"]/a[1]/@href').extract()[0]
        indexes=int(response.xpath('//*[@id="pagelink"]/a[last()]/text()').extract()[0])
        with open('./allurl.txt','a+') as f:        
            for i in range(1,indexes+1):
                src=urlmod.replace('1.html',str(i)+'.html').strip()
                f.write(src+'\n')

class BookSpider(scrapy.Spider):
    name = 'Book'
    allowed_domains = ['quanshuwang.com']
    # start_urls = [url.strip() for url in open('./allurl.txt').readlines()]  #获取所有页面连接
    start_urls = ['http://www.quanshuwang.com/book/183/183592','http://www.quanshuwang.com/book/15/15500']  #获取所有页面连接
    # def parse(self, response):
    #     urls=response.xpath('//*[@id="navList"]/section/ul/li/span/a[1]/@href').extract()
    #     if os.path.exists('./bookurl.txt'):
    #         os.remove('./bookurl.txt')
    #     for url in urls:
    #         yield scrapy.Request((url),callback=self.parse_level2)
    # def parse_level2(self,response):
    #     trueurls=response.xpath('//*[@id="container"]/div[2]/section/div/div[1]/div[2]/a[1]/@href').extract()
    #     for url in trueurls:
    #         yield scrapy.Request((url),callback=self.parse_level3)
    def parse(self,response):
        # bookinfo={}
        # chapterinfo={}
        itemloader=ItemLoader(item=BookItem(),response=response)
        itemloader.add_xpath('name','//*[@id="chapter"]/div[3]/div[1]/strong/text()')
        itemloader.add_xpath('author','//*[@id="chapter"]/div[3]/div[1]/span/text()')
        itemloader.add_xpath('chapter','//*[@id="chapter"]/div[3]/div[3]/ul/div[2]/li/a/text()')
        itemloader.add_xpath('url','//*[@id="chapter"]/div[3]/div[3]/ul/div[2]/li/a/@href')
        # chapterinfo['author']=itemloader.load_item()['author'][0][3:]
        # chapterinfo['chapter']=dict(zip(itemloader.load_item()['chapter'],itemloader.load_item()['url']))
        # bookinfo[itemloader.load_item()['name'][0]]=chapterinfo
        # book=json.dumps(bookinfo,ensure_ascii=False)
        # with open('./bookurl.txt','a+') as f:
        #     f.write(book+'\n')
        for url in itemloader.load_item()['url']:
            yield scrapy.Request((url),callback=self.parse_level4)
    def parse_level4(self,response):
        content=str(response.xpath('//*[@id="content"]/text()').extract())
        chapter=response.xpath('//*[@id="directs"]/div[1]/h1/strong/text()').extract()[0][4:]
        bookname=response.xpath('//*[@id="directs"]/div[1]/h1/em/text()').extract()[0][1:-1]
        if not os.path.exists('./'+bookname):
            os.mkdir('./'+bookname)
        with open('./'+bookname+'/'+chapter,'w+') as f:
            f.write(content)
        
        

        
        


# class downloadSpider(scrapy.Spider):
#     name = 'download'
#     allowed_domains = ['quanshuwang.com']
#     with open('./bookurl.txt','r+') as f:

#     start_urls = [url.strip() for url in open('./allurl.txt').readlines()]  #获取所有页面连接



