# # 导入pymysql模块
# import pymysql
# # 连接database
# conn = pymysql.connect(
#     host="127.0.0.1",
#     port=53306,
#     user="root",
#     password="password",
#     database="test",
#     charset="utf8")
# # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
# # 获取一个光标
# cursor = conn.cursor()
# print(cursor)


import time

from selenium import webdriver

from selenium.webdriver.common.touch_actions import TouchActions




from ArticleSpider.settings import BASE_DIR
import os
import pickle
import time

chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:1087")

"""设置手机的大小"""

mobileEmulation = {'deviceName': 'Apple iPhone 5'}
chromeOptions.add_experimental_option('mobileEmulation', mobileEmulation)


browser = webdriver.Chrome(
    executable_path="/Users/xiao/PycharmProjects/ArticleSpider/chrome_nocdc/chromedriver",
)
browser.get("https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110")
res = browser.find_element_by_id("email").send_keys("facebook@lisunlou.com")
browser.find_element_by_id("pass").send_keys("~q13lYbCy0jI76{M")
browser.find_element_by_id("loginbutton").click()

# time.sleep(10)
cookies = browser.get_cookies()
print(cookies)





browser.get('https://m.facebook.com/BBCChinese/posts/?ref=page_internal&mt_nav=0')

browser.maximize_window()

"""定位操作元素"""

button = browser.find_element_by_xpath('/html/head/title')

time.sleep(3)

Action = TouchActions(browser)

"""从button元素像下滑动200元素，以50的速度向下滑动"""

Action.flick_element(button, 0, 1000, 50).perform()

time.sleep(3)

browser.close()