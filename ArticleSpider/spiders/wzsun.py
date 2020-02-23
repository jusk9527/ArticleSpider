# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     wzsun
   Description :
   Author :       jusk?
   date：          2020/2/19
-------------------------------------------------
   Change Activity:
                   2020/2/19:
-------------------------------------------------
"""
import scrapy

from ArticleSpider.items import wzSunItem

class WzsunSpider(scrapy.Spider):
    """
    阳光问政平台
    """
    name = "wzSun"
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0
    start_urls = [url+str(offset)]

    def parse(self, response):
        # 取出每个页面立帖子的链接列表
        links = response.xpath("//tr/td/a[@class='news14']/@href").extract()
        # 迭代发送每个帖子的请求，调用parse_item方法处理
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)

        if self.offset <= 71130:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
    # 处理每个帖子
    def parse_item(self, response):
        item = wzSunItem()

        # 标题
        item['title'] = response.xpath("//td[2]/span[1]/text()").extract()

        # 编号
        item['number'] = response.xpath("//tr/td[2]/span[2]/text()").extract()
        # 文字内容，默认先取出有图片情况下的文字内容列表
        content = response.xpath("//td/text()").extract()
        item['content'] = content

        item['url'] = response.url

        yield item