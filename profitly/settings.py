# Scrapy settings for profitly project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'profitly'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['profitly.spiders']
NEWSPIDER_MODULE = 'profitly.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = {
    'profitly.pipelines.CsvExportPipeline': 2000,
    'profitly.pipelines.JsonWithEncodingPipeline': 3000,
    'profitly.pipelines.MongoDBBrokerPipeline':3001,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = BOT_NAME # db name
