# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from myscrapy.items import BookinfoItem,SectionItem

class MyscrapyPipeline(object):
    def __init__(self,mongo_db,mongo_uri,mongo_user,mongo_pwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_pwd = mongo_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_user=crawler.settings.get('MONGO_UER'),
            mongo_pwd=crawler.settings.get('MONGO_PWD'),
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        if isinstance(item,BookinfoItem):
            # self.db.book_info.update({'book_id':item['book_id']},{'$set':dict(item)},True)
            self.db.book_info.insert(dict(item))
            # return item
        elif isinstance(item,SectionItem):
            # self.db.section_info.update({'section_id':item['section_id']},{'$set':dict(item)},True)
            self.db.section_info.insert(dict(item))
            # return item
        # elif isinstance(item,ContentItem):
            # self.db.content_info.update({'section_id':item['section_id']},{'$set':dict(item)},True)
            # self.db.content_info.insert(dict(item))
            # return item
