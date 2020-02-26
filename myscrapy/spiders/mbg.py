import scrapy,json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from myscrapy.items import BookItem,BookinfoItem,SectionItem,ContentItem
from scrapy.loader import *
from scrapy.loader.processors import *
from scrapy.http.request.form import FormRequest
from scrapy.http import Request
from urllib.parse import urljoin
from myscrapy.utils.common import get_md5
from redis import Redis

class MbgSpider(CrawlSpider):
    name='mbg'
    allowed_domains = ['imiaobige.com']
    start_urls = ['https://www.imiaobige.com/all/1.html']
    rules=(
        Rule(LinkExtractor(allow=r'all/([1-9]\d?|100).html'),callback='parse_all',follow=True),
       # Rule(LinkExtractor(allow=r'all/(2).html'),callback='parse_all',follow=True),
    )
    def parse_all(self,response):
        item_loader=ItemLoader(item=BookItem(),response=response)
        item_loader.add_xpath('bookurl','//*[@id="main"]/div/ul/li/a/@href')
        info_item=item_loader.load_item()
        for url in info_item['bookurl']:
            yield scrapy.Request(urljoin('https://www.imiaobige.com/',url),callback=self.parse_book)
    def parse_book(self,response):
        book_loader=ItemLoader(item=BookinfoItem(),response=response)
        book_loader.add_value('book_id',get_md5(response.url))
        book_loader.add_xpath('author','//*[@id="author"]/a/text()')
        book_loader.add_xpath('book_info','//*[@id="bookintro"]/text()')
        book_loader.add_xpath('book_name','//*[@id="bookinfo"]/div[2]/div[1]/h1/text()')
        book_loader.add_xpath('book_url','//*[@id="bookinfo"]/div[3]/a[1]/@href')
        book_loader.add_xpath('image_url','//*[@id="bookimg"]/img/@src')
        book_loader.add_xpath('style','//*[@id="bookinfo"]/div[2]/div[2]/ul/li[1]/span/text()')
        book_loader.add_xpath('update','//*[@id="bookinfo"]/div[2]/div[5]/span[2]/text()')
        book_loader.add_xpath('status','//*[@id="bookinfo"]/div[2]/div[2]/ul/li[2]/span/text()')
        book_loader.add_value('source','mbg')
        book_item=book_loader.load_item()
        if book_item['status'][0] == "连载中":
            book_item['status']="1"
        else:
            book_item['status']="0"
        for bookinfo in book_item:
            book_item[bookinfo]=book_item[bookinfo][0]
            if bookinfo == 'book_url':
                book_item['book_url']=urljoin('https://www.imiaobige.com/',book_item['book_url'])
                yield scrapy.Request(book_item['book_url'],meta={'book_id':book_item['book_id']},callback=self.parse_section)
        yield book_item
    def parse_section(self,response):
        sectioninfo=[]
        section_namelist=response.xpath('//*[@id="readerlists"]/ul[position()>1]/li/a/text()').extract()
        section_urllist=response.xpath('//*[@id="readerlists"]/ul[position()>1]/li/a/@href').extract()
        infolist=list(zip(section_namelist,section_urllist))
        for info in infolist:
            sectiondict={}
            sectiondict['book_id']=response.meta['book_id']
            sectiondict['section_id']=get_md5(info[1])
            sectiondict['section_name']=info[0]
            sectiondict['section_url']=urljoin('https://www.imiaobige.com/',info[1])
            sectioninfo.append(sectiondict)
            yield scrapy.Request(sectiondict['section_url'],meta={'section_id':sectiondict['section_id'],'section_name':info[0]},callback=self.parse_content)
        sectionitem=SectionItem()
        for info in sectioninfo:
            sectionitem['book_id']=info['book_id']
            sectionitem['section_id']=info['section_id']
            sectionitem['section_name']=info['section_name']
            sectionitem['section_url']=info['section_url']
            yield sectionitem
    def parse_content(self,response):
        content_loader=ItemLoader(item=ContentItem(),response=response)
        content_loader.add_value('section_id',response.meta['section_id'])
        content_loader.add_value('section_name',response.meta['section_name'])
        content_loader.add_xpath('content_text','//*[@id="content"]/p[position()>1]/text()')
        content_item=content_loader.load_item()
        content_item['section_id']=content_item['section_id'][0]
        content_item['section_name']=content_item['section_name'][0]
        yield content_item
          








    
