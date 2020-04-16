# -*- coding: utf-8 -*-
import scrapy
import os
import time

import pickle
from ArticleSpider.settings import BASE_DIR

name = 'mafengwo'
host = "https://www.facebook.com/"
username = "facebook@lisunlou.com"  # 帐号
password = "~q13lYbCy0jI76{M"  # 密码
headerData = {
    "authority": "www.facebook.com",
    'scheme':'https',
    'path':'/login/device-based/regular/login/?login_attempt=1&lwv=110',
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-language':'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests':'1',
    'cache-control':'max-age=0',
    'content-type':'application/x-www-form-urlencoded',
    'origin':'https://www.facebook.com',
    'referer':'https://www.facebook.com/',
}

class FacebookSpider(scrapy.Spider):
    """
    根据人物爬取数据
    """
    name = 'facebook'
    allowed_domains = ['https://www.facebook.com/']
    start_urls = ['https://www.facebook.com/']



    # 爬虫运行的起始位置
    # 第一步：爬取登录页面
    def start_requests(self):
        print("start mafengwo clawer")
        # 登录页面
        mafengwoLoginPage = "https://www.facebook.com/"
        loginIndexReq = scrapy.Request(
            url=mafengwoLoginPage,
            headers=self.headerData,
            callback=self.parseLoginPage,
            dont_filter=True,  # 防止页面因为重复爬取，被过滤了
        )
        yield loginIndexReq



    # 第二步：分析登录页面，取出必要的参数，然后发起登录请求POST
    def parseLoginPage(self, response):
        print(f"完蛋 = {response.url}" + "==========================")
        # 如果这个登录页面含有一些登录必备的信息，那么就在这个函数里面进行信息提取( response.text )
        loginPostUrl = "https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110"


        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=loginPostUrl,
            headers=self.headerData,
            method="POST",
            # post的具体数据
            formdata={
                "jazoest": "2635",
                "lsd": "AVpC9O0y",
                "email": self.username,
                "pass": self.password,
                "timezone": "-480",
                "lgndim": "eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNDAsImMiOjI0fQ==",
                "lgnrnd": "000725_pmuo",
                "lgnjs": "1547193922",
                "locale": "zh_CN",
                "next": "https://www.facebook.com/",
                "login_source": "login_bluebar",
                "prefill_contact_point": self.username,
                "prefill_source": self.password,
                "skstamp": "eyJyb3VuZHMiOjUsInNlZWQiOiJhN2RmZTVlNDQ0NmRkNmFlNzA2NjFlODJlNWI3NzlhZiIsInNlZWQyIjoiMjU0MzdiZTU2YmMzNjAwMzJhMmMzNTI3NWYzZGJiYWUiLCJoYXNoIjoiNDY0YjI3YmFjNzYzMmM5NDU1MjFjZDVkYmQ5NjA3MDYiLCJoYXNoMiI6IjkwNzQ1ZTZkMDgzZTBmOTA2MTI3MjIyN2EzN2RiOWI1IiwidGltZV90YWtlbiI6MTM2Nzk5LCJzdXJmYWNlIjoibG9naW4ifQ==",
                # "other": "other",
            },
            callback=self.loginResParse,
            dont_filter=True,
        )



    # 第三步：分析登录结果，然后发起登录状态的验证请求
    def loginResParse(self, response):
        print(f"loginResParse: url = {response.url}")
        # 这个页面，只有登录过的用户，才能访问。否则会被重定向(302) 到登录页面
        routeUrl = "https://www.facebook.com/"
        # 下面有两个关键点
        # 第一个是header，如果不设置，会返回500的错误
        # 第二个是dont_redirect，设置为True时，是不允许重定向，用户处于非登录状态时，是无法进入这个页面的，服务器返回302错误。
        #       dont_redirect，如果设置为False，允许重定向，进入这个页面时，会自动跳转到登录页面。会把登录页面抓下来。返回200的状态码
        yield scrapy.Request(
            url=routeUrl,
            headers=self.headerData,
            meta={
                'dont_redirect': True,  # 禁止网页重定向302, 如果设置这个，但是页面又一定要跳转，那么爬虫会异常
                # 'handle_httpstatus_list': [301, 302]      # 对哪些异常返回进行处理
            },
            callback=self.isLoginStatusParse,
            dont_filter=True,
        )

    def isLoginStatusParse(self,response):
        Cookie = response.request.headers.getlist('Cookie')
        print("Cookies"+str(Cookie))

        yield scrapy.Request(url=routeUrl, callback=self.parse)



    def parse(self, response):
        pass