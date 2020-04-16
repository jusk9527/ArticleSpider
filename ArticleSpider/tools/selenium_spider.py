# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     selenium_spider
   Description :
   Author :       jusk?
   date：          2020/2/21
-------------------------------------------------
   Change Activity:
                   2020/2/21:
-------------------------------------------------
"""
from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="D:/Temp/chromedriver.exe")

# browser.get("https://www.zhihu.com/#signin")
#
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("18782902568")
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("admin125")
#
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()
#selenium 完成微博模拟登录

# browser.get("https://www.oschina.net/blog")
# import time
# time.sleep(5)
# browser.find_element_by_css_selector("#loginname").send_keys("liyao198705@sina.com")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("da_ge_da")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)
# t_selector = Selector(text=browser.page_source)
# print (t_selector.css(".tm-promo-price .tm-price::text").extract())


#设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)


#phantomjs, 无界面的浏览器， 多进程情况下phantomjs性能会下降很严重



# https://blog.csdn.net/djshichaoren/article/details/89850273 版本问题
from selenium import webdriver
import time
from ArticleSpider.settings import BASE_DIR
import os
import pickle
chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:1087")

browser = webdriver.Chrome(
    executable_path="/Users/xiao/PycharmProjects/ArticleSpider/chrome_nocdc/chromedriver"
)
browser.get("https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110 ")
res = browser.find_element_by_id("email").send_keys("facebook@lisunlou.com")
browser.find_element_by_id("pass").send_keys("~q13lYbCy0jI76{M")
browser.find_element_by_id("loginbutton").click()
import time

# time.sleep(10)
cookies = browser.get_cookies()
print(cookies)

if os.path.exists(BASE_DIR+"/cookies/facebook.cookies"):
    cookies = pickle.load(open(BASE_DIR+"/cookies/facebook.cookies", "rb"))


if not cookies:
    pickle.dump(cookies, open(BASE_DIR + "/cookies/facebook.cookies", "wb"))


# 模拟鼠标向下滑动 h5
from selenium.webdriver.common.touch_actions import TouchActions


"""设置手机的大小"""

mobileEmulation = {'deviceName': 'Apple iPhone 5'}

browser.add_experimental_option('mobileEmulation', mobileEmulation)


browser.get("https://m.facebook.com/BBCChinese/posts/?ref=page_internal&mt_nav=0")


browser.maximize_window()


"""定位操作元素"""

button = browser.find_element_by_xpath('/html/head/title')
# 时间
# title = browser.find_element_by_xpath('//*[@class="_5ptz timestamp livetimestamp"]/@title')


browser.execute_script("window.scrollBy(0,1000)")
import time
time.sleep(10)

# 帖子内容
title = browser.find_element_by_xpath('//*[@class="_5pbx userContent _3576"]/p').text

# title = browser.find_element_by_xpath('//*[@class="_1dwg _1w_m _q7o"]/div').f

print(title)
print(type(title))


# //*[@class="_1dwg _1w_m _q7o"]/div





browser.quit()


