# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookinfoItem(scrapy.Item):
    book_id=scrapy.Field()
    book_name=scrapy.Field()
    author=scrapy.Field()
    book_info=scrapy.Field()
    image_url=scrapy.Field()
    book_url=scrapy.Field()
    style=scrapy.Field()
    update=scrapy.Field()
    status=scrapy.Field()
    source=scrapy.Field()

class SectionItem(scrapy.Item):
    book_id=scrapy.Field()
    section_name=scrapy.Field()
    section_url=scrapy.Field()
    content_text=scrapy.Field()




#动态添加item的Field
# class item():
#     pass