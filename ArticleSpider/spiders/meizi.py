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
from ArticleSpider.items import MzituItem
from scrapy import Request
# 妹子图片等图像下载，记住图片下载header 需要加Referer，不需要什么，只要加这个参数即可
class MeiziSpider(scrapy.Spider):


    name = 'meizi'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/all/',]
    custom_settings = {
        "ITEM_PIPELINES": {
                'ArticleSpider.pipelines.meizipiplines.MeiziPipeline' : 300,

        },

        "DOWNLOAD_DELAY": 2,

    }

    def parse(self, response):
        a_xpath = response.xpath("//ul[@class='archives']/li/p[2]/a")
        for i in a_xpath:
            a_word = i.xpath("text()").extract_first()
            a_href = i.xpath("@href").extract_first()
            yield Request(a_href,meta={"a_word":a_word,"a_href":a_href},callback=self.parse_detail)

    def parse_detail(self,response):

        item = MzituItem()

        # 最大值
        max_value = response.xpath("//div[@class='pagenavi']/a[5]/span/text()").extract_first()

        a_word = response.meta["a_word"]
        a_href = response.meta["a_href"]
        images_url = response.xpath("//div[@class='main-image']/p/a/img/@src").extract_first()

        datatime = response.xpath("//div[@class='main-meta']/span[2]/text()").extract_first()

        category = response.xpath('//span/a[@rel="category tag"]/text()').extract_first()
        item["title"] = a_word
        item["datatime"] = datatime
        # item["image_urls"] = [images_url]
        item["base_url"] = response.url
        item["max_images"] = max_value
        item["category"] = category
        print("=======a_href"+str(a_href))


        for i in range(0, int(max_value)+1):
            # print(str(a_href)+"/"+str(i))
            if i == 1:
                pass
            else:
                yield Request(str(a_href)+"/"+str(i),meta={"item":item,"i":i,
                                                       "max_images":max_value},callback=self.parse_next_detail)






    def parse_next_detail(self,response):
        i = response.meta["i"]
        max_images = response.meta.get("max_images", 0)
        item = response.meta.get("item")
        images_url = response.xpath("//div[@class='main-image']/p/a/img/@src").extract_first()
        # print("response"+response.url)
        item["image_urls"] = images_url
        # print(item["base_url"] + "/" + str(i))

        yield item





