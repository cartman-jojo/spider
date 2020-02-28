# -*- coding: utf-8 -*-
import scrapy,os
# from bs4 import BeautifulSoup
from myscrapy.items import BookinfoItem,SectionItem
from urllib.parse import urljoin
from myscrapy.utils.common import get_md5
from scrapy.http import Request
import json
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class DocumentSpider(RedisCrawlSpider):
    name = 'Document'
    allowed_domains = ['imiaobige.com']
    # start_urls = ['https://www.imiaobige.com/all/1.html']
    redis_key="mbg"
    rules = (
        Rule(LinkExtractor(allow=r'all/([1-9]\d?|100).html'),follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='main']/div/ul/li/a/..",)),callback="parse_book"),
    )  
    def parse_book(self, response):
        item = BookinfoItem()
        item['book_id']=get_md5(response.url)
        item['book_name']=response.xpath('//*[@id="bookinfo"]/div[2]/div[1]/h1/text()').extract_first()
        item['author']=response.xpath('//*[@id="author"]/a/text()').extract_first()
        item['book_info']=response.xpath('//*[@id="bookintro"]/text()').extract_first()
        item['book_url']=urljoin('https://www.imiaobige.com/',response.xpath('//*[@id="bookinfo"]/div[3]/a[1]/@href').extract_first())
        item['image_url']=response.xpath('//*[@id="bookimg"]/img/@src').extract_first()
        item['style']=response.xpath('//*[@id="bookinfo"]/div[2]/div[2]/ul/li[1]/span/text()').extract_first()
        item['update']=response.xpath('//*[@id="bookinfo"]/div[2]/div[5]/span[2]/text()').extract_first()
        item['source']='mbg'
        if response.xpath('//*[@id="bookinfo"]/div[2]/div[2]/ul/li[2]/span/text()').extract_first() == "连载中":
            item['status']="1"
        else:
            item['status']="0"
        yield scrapy.Request(item['book_url'],meta={'book_id':item['book_id']},callback=self.parse_section)
        yield item
    def parse_section(self, response):
        section_list=response.xpath('//*[@id="readerlists"]/ul[position()>1]/li')
        for section in section_list:
            section_item={}
            section_item['book_id']=response.meta['book_id']
            section_item['section_name']=section.xpath('./a/text()').extract_first()
            section_item['section_url']=urljoin('https://www.imiaobige.com/',section.xpath('./a/@href').extract_first())
            yield scrapy.Request(section_item['section_url'],meta={'section':section_item},callback=self.parse_content)
    def parse_content(self, response):
        # print(type(response.meta['section']))
        citem=SectionItem()
        content_item=response.meta['section']
        content_item['content_text']=response.xpath('//*[@id="content"]/p[position()>1]/text()').extract()
        citem['book_id']=content_item['book_id']
        citem['section_name']=content_item['section_name']
        citem['section_url']=content_item['section_url']
        citem['content_text']=content_item['content_text']
        yield citem



