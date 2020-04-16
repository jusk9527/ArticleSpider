
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobbolespiderItem
from scrapy_redis.spiders import RedisSpider
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobboless'
    base_url = "http://blog.jobbole.com"
    allowd_domains = ["blog.jobbole.com"]
    url = 'http://blog.jobbole.com/kaifadou/snews-getajax.php?next='
    start = 0
    end = ''
    start_urls = [url + str(start)]
    i = 0

    def parse(self, response):
        """
        逻辑分析
            1.通过抓取下一页的链接，交给scrapy实现自动翻页,如果没有下一页则爬取完成
            2.将本页面的所有文章url爬下，并交给scrapy进行深入详情页的爬取
        """

        # 全部连接
        a_href = response.xpath(
            "//a[contains(@target,'_blank')]/@href").extract()
        for i in a_href:

            # 如果详情页，parse_detail
            yield Request(url=str(self.base_url + i + "/"), callback=self.parse_detail)

        # 如果存在下一页，则将下一页交给parse自身处理
        yield Request(url=self.url + self.end, callback=self.parse)

        self.end += str(1)

    def parse_detail(self, response):
        """
        将爬虫爬取的数据送到item中进行序列化
        这里通过ItemLoader加载item
        """
        item = JobbolespiderItem()
        item["title"] = response.xpath("//h2").extract()[0]
        item["content"] = response.xpath(
            "//div[contains(@class,'wen_article')]").extract()[0]
        item["datatime"] = response.xpath(
            "//div[contains(@class,'meta')]/span/text()").extract()[0]

        yield item
