# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     douyu
   Description :
   Author :       jusk?
   date：          2020/2/19
-------------------------------------------------
   Change Activity:
                   2020/2/19:
-------------------------------------------------
"""
# -*- coding: utf-8 -*-
import scrapy
import json
from ArticleSpider.items import DouyuItem

# 斗鱼主播等图像下载
class DouyuSpider(scrapy.Spider):
    name = "douYu"
    allowed_domains = ["capi.douyucdn.cn"]
    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    start_urls = [url+str(offset)]

    def parse(self, response):
        data = json.loads(response.text)["data"]

        for each in data:
            item = DouyuItem()
            item["room_id"] = each["room_id"]
            item["room_name"] = each["room_name"]
            item["game_name"] = each["game_name"]
            item["anchor_city"] = each["anchor_city"]
            item["name"] = each["nickname"]
            item["imagesUrls"] = each["vertical_src"]
            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)