from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from profitly.items import ProfitlyTradesItem
import re

class TradesSpider(CrawlSpider):
    name = 'trades'
    allowed_domains = ['profit.ly']
    start_urls = [
        'http://profit.ly/user/timothysykes/trades',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/user/[\w]+/trades'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'/user/[\w]+/trades\?page=[\d]+&size=[\d]+'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=trades -c parse_item 'http://profit.ly/user/timothysykes/trades?page=2&size=10'
    def parse_item(self, response):
        
        hxs = HtmlXPathSelector(response)
        items = []
        profits = hxs.select('//div/div/div[2]/div[3]/div[1]/a[1]/text()').extract()
        tickers = hxs.select('//div/div/div[2]/div[3]/div[1]/a[2]/text()').extract()
        biases = hxs.select('//div/div/div[2]/div[3]/div[1]/span[1]/text()').extract()
        traders = hxs.select('//div/div/div[2]/div[3]/div[1]/a[3]/text()').extract()
        entrycomments = hxs.select('//div/div[3]/div/div/div[2]/div[3]/p[1]/text()').extract()
        exitcomments = hxs.select('//div/div[3]/div/div/div[2]/div[3]/p[2]/text()').extract()
        datetimes = hxs.select('//div/div[3]/div/div/div[2]/div[3]/div[4]/a/text()').extract()
        brokers = hxs.select('//div/div[3]/div/div/div[2]/div[3]/div[6]/ul/li[4]/a/@href').extract()
        
        for profit, ticker, bias, entrycomment, exitcomment, trader, datetime, broker in zip(profits, tickers, biases, entrycomments, exitcomments, traders, datetimes, brokers):
            # modify $123k and $1.23M to float format
            profit = profit.replace(' profit', '')
            profit = profit.replace('$', '')
            profit = profit.replace(',', '')
            
            #tr = '(576) loss'
            try:
                gr = re.match(re.compile(r'\(([\d]+)\) loss'), profit).groups()
                profit = "-{0}".format(gr[0])
            except:
                ''
            #profit = float(profit)
            #try:    profit = int(float(profit.replace('k', ''))*1000)
            #except: profit = int(float(profit.replace('M', ''))*1000000)
            #print [profit]
            broker = broker.replace('/broker/', '')
            items.append(ProfitlyTradesItem(profit=profit, ticker=ticker, bias=bias, entrycomment=entrycomment, exitcomment=exitcomment, trader=trader, datetime=datetime, broker=broker))
        return items
