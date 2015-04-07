from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from profitly.items import ProfitlyItem

class BrokersSpider(CrawlSpider):
    name = 'brokers'
    allowed_domains = ['profit.ly']
    start_urls = ['http://profit.ly/leaderboard/broker/top/alltime']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/leaderboard/broker/top/alltime\?page=[\d]+&size=[\d]+'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=brokers -c parse_item 'http://profit.ly/leaderboard/broker/top/alltime'
    def parse_item(self, response):
        
        hxs = HtmlXPathSelector(response)
        items = []
        company_names = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/a/text()').extract()
        hrefs = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/a/@href').extract()
        profits = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[3]/div/span/text()').extract()        

        for com, href, profit in zip(company_names, hrefs, profits):
            href = href.replace('/broker/', '')
            # modify $123k and $1.23M to float format
            profit = profit.replace(',', '')            
            profit = profit.replace('$', '')            
            try:    profit = float(profit.replace('k', ''))*1000
            except: profit = float(profit.replace('M', ''))*1000000
            #print [com]
            items.append(ProfitlyItem(company=com, href=href, profit=profit))
        return items
