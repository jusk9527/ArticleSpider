# -*- coding: utf-8 -*-
__author__ = 'bobby'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "douban"])
# execute(["scrapy", "crawl", "douYu"])
# execute(["scrapy", "crawl", "wzSun"])
execute(["scrapy", "crawl", "jobbole"])
# execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])