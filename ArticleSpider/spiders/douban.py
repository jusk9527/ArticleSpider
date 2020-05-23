# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     douban
   Description :
   Author :       jusk?
   date：          2020/2/19
-------------------------------------------------
   Change Activity:
                   2020/2/19:
-------------------------------------------------
"""

import scrapy
from ArticleSpider.items import DoubanspiderItem
from scrapy_redis.spiders import RedisSpider

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    url = 'https://movie.douban.com/top250?start='
    start = 0
    end = '&filter='
    start_urls = [url + str(start) + end]


    custom_settings = {
        "ITEM_PIPELINES": {
                'ArticleSpider.pipelines.pipelines.DoubanspiderPipeline' : 300,


        }
    }

    def parse(self, response):
        item = DoubanspiderItem()
        movies = response.xpath("//div[@class=\'info\']")

        for each in movies:
            title = each.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            content = each.xpath('div[@class="bd"]/p/text()').extract()
            score = each.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            info = each.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            item['title'] = title[0]
            # 以;作为分隔，将content列表里所有元素合并成一个新的字符串
            item['content'] = ';'.join(content)
            item['score'] = score[0]
            item['info'] = info[0]
            # 提交item

            yield item

        if self.start <= 225:
            self.start += 25
            yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.parse)