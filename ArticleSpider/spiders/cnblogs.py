import re
import json
from urllib import parse

import scrapy
from scrapy import Request
#scrapy是异步io框架， 没有多线程， 没有引入消息队列
import requests

from ArticleSpider.utils import common

from ArticleSpider.items import JobBoleArticleItem
from selenium import webdriver
class JobboleSpider(scrapy.Spider):
    name = 'bokeyuan'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']
    #学习完以后不要去设想立马就能下载所有的新闻

    # def __init__(self):
    #     # 当使用selelum时browser放入到spider中，与middleware相连
    #     self.browser = webdriver.Chrome(
    #         executable_path="C:/Users/Administrator/Downloads/spider-master/ArticleSpider/chrome_nocdc/chromedriver.exe"
    #     )
    #     super(JobboleSpider, self).__init__()

    def parse(self, response):
        """
        1. 获取新闻列表页中的新闻url并交给scrapy进行下载后调用相应的解析方法
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse继续跟进
        """
        post_nodes = response.css('#news_list .news_block')
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            if image_url.startswith("//"):
                image_url = "https:"+image_url
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.group(1)

            article_item = JobBoleArticleItem()
            title = response.css("#news_title a::text").extract_first("")
            create_date = response.css("#news_info .time::text").extract_first("")
            match_re = re.match(".*?(\d+.*)", create_date)
            if match_re:
                create_date = match_re.group(1)
            content = response.css("#news_content").extract()[0]
            tag_list = response.css(".news_tags a::text").extract()
            tags = ",".join(tag_list)
            article_item["title"] = title
            article_item["create_date"] = create_date
            article_item["content"] = content
            article_item["tags"] = tags
            article_item["url"] = response.url
            if response.meta.get("front_image_url", ""):
                article_item["front_image_url"] = [response.meta.get("front_image_url", "")]
            else:
                article_item["front_image_url"] = []

            article_item["url_object_id"] = common.get_md5(response.url)

            yield article_item

