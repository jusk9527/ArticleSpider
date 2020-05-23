# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))
# execute(["scrapy", "crawl", "douban"])
# execute(["scrapy","crawl","jobboless"])
# execute(["scrapy", "crawl", "douYu"])
# execute(["scrapy", "crawl", "wzSun"])
# execute(["scrapy", "crawl", "bokeyuan"])
# execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])
# execute(["scrapy", "crawl", "facebook"])
# execute(["scrapy", "crawl", "face"])
# execute(["scrapy", "crawl", "meizi"])
# execute(["scrapy", "crawl", "hj_spider"])
execute(["scrapy", "crawl", "github_login"])

