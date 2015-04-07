from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from profitly.items import ProfitlyUsersItem

class UsersSpider(CrawlSpider):
    name = 'users'
    allowed_domains = ['profit.ly']
    start_urls = [
        'http://profit.ly/leaderboard/user/verified/alltime',
        'http://profit.ly/leaderboard/user/top/alltime',
        'http://profit.ly/leaderboard/user/perc/alltime',
        'http://profit.ly/leaderboard/user/pop/alltime',
        'http://profit.ly/leaderboard/user/trust/alltime',
        'http://profit.ly/leaderboard/user/madoff/alltime',
        'http://profit.ly/leaderboard/user/followed/alltime',
        'http://profit.ly/leaderboard/user/chats/alltime',
        'http://profit.ly/leaderboard/user/karma/alltime',
        'http://profit.ly/leaderboard/newsletter/top/alltime',
        'http://profit.ly/leaderboard/newsletter/pop/alltime',
        'http://profit.ly/leaderboard/broker/top/alltime',
        'http://profit.ly/leaderboard/broker/pop/alltime',
        'http://profit.ly/leaderboard/ticker/top/alltime',
        'http://profit.ly/leaderboard/ticker/pop/alltime',
        'http://profit.ly/leaderboard/ticker/chats/alltime',
        'http://profit.ly/leaderboard/trade/pop/alltime',
        'http://profit.ly/leaderboard/trade/trust/alltime',
        'http://profit.ly/leaderboard/trade/madoff/alltime',
        'http://profit.ly/leaderboard/post/karma/alltime',
        'http://profit.ly/leaderboard/content/rated/alltime',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/leaderboard/user/[\w]+/alltime\?page=[\d]+&size=[\d]+'), callback='parse_item', follow=True),
    )

    # scrapy parse --spider=brokers -c parse_item 'http://profit.ly/leaderboard/broker/top/alltime'
    def parse_item(self, response):
        
        hxs = HtmlXPathSelector(response)
        items = []
        users = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/a/text()').extract()
        hrefs = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/a/@href').extract()
        profits = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[3]/div/span/text()').extract()
        ranks = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[1]/text()').extract()
        imgs = hxs.select('/html/body/div[2]/div[3]/div/div[1]/div/div[3]/div/div/div/div[2]/img/@src').extract()

        for user, href, profit, rank, img in zip(users, hrefs, profits, ranks, imgs):
            # modify $123k and $1.23M to float format
            profit = profit.replace(',', '')            
            profit = profit.replace('$', '')            
            try:    profit = int(float(profit.replace('k', ''))*1000)
            except: profit = int(float(profit.replace('M', ''))*1000000)
            #print [com]
            items.append(ProfitlyUsersItem(user=user, href=href, profit=profit, rank=rank, img=img))
        return items
