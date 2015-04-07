# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ProfitlyBrokersItem(Item):
    # define the fields for your item here like:
    company = Field()
    href = Field()
    profit = Field()
    pass

class ProfitlyUsersItem(Item):
    # define the fields for your item here like:
    user = Field()
    href = Field()
    profit = Field()
    rank = Field()
    img = Field()
    pass

class ProfitlyTradesItem(Item):
    # define the fields for your item here like:
    profit = Field()
    ticker = Field()
    bias = Field()
    trader = Field()
    entrycomment = Field()
    exitcomment = Field()
    datetime = Field()
    broker = Field()
    pass
