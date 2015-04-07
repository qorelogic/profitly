# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.contrib.exporter import CsvItemExporter

import pymongo
from settings import *

class ProfitlyPipeline(object):
    def __init__(self):
        self.proj = BOT_NAME
        
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(ProfitlyPipeline):

    def __init__(self):
        super(JsonWithEncodingPipeline, self).__init__()
        self.suffix = 'json'
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('{0}_{1}.{2}'.format(spider.name, self.proj, self.suffix), 'w+b')
        self.files[spider] = file
        #self.exporter = JsonItemExporter(file)
        self.exporter = JsonLinesItemExporter(file)        
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class CsvExportPipeline(ProfitlyPipeline):

    def __init__(self):
        super(CsvExportPipeline, self).__init__()
        self.suffix = 'csv'
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('{0}_{1}.{2}'.format(spider.name, self.proj, self.suffix), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)        
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MongoDBBrokerPipeline(ProfitlyPipeline):
    def __init__(self):
        super(MongoDBBrokerPipeline, self).__init__()
        connection = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
        self.db = connection[MONGODB_DB]
        self.collections = {}
        self.collections['brokers'] = self.db['brokers']
        self.collections['users']   = self.db['users']
        self.collections['trades']   = self.db['trades']
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.collections[spider.name] = self.db[spider.name]
        # remove all for clean insertion
        self.collections[spider.name].remove()

    def spider_closed(self, spider):
        stub=''

    def process_item(self, item, spider):
        #if not isinstance(item, items.ProfitlyItem):
        #return item # return the item to let other pipeline to handle it
        self.collections[spider.name].insert(dict(item))
        return item # return the item to let other pipeline to handle it
