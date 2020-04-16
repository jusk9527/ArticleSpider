import time

from selenium import webdriver

from selenium.webdriver.common.touch_actions import TouchActions

"""设置手机的大小"""

mobileEmulation = {'deviceName': 'Apple iPhone 5'}

options = webdriver.ChromeOptions()

options.add_experimental_option('mobileEmulation', mobileEmulation)

driver = webdriver.Chrome(executable_path="/Users/xiao/PycharmProjects/ArticleSpider/chrome_nocdc/chromedriver",
)



# driver.get("https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110 ")
# driver.find_element_by_id("email").send_keys("facebook@lisunlou.com")
# driver.find_element_by_id("pass").send_keys("~q13lYbCy0jI76{M")
# driver.find_element_by_id("loginbutton").click()
#
driver.get('https://www.baidu.com')

driver.maximize_window()

"""定位操作元素"""

button = driver.find_element_by_xpath('/html/head/title')

time.sleep(3)

Action = TouchActions(driver)

"""从button元素像下滑动200元素，以50的速度向下滑动"""

Action.flick_element(button, 0, 200, 50).perform()

time.sleep(3)

driver.close()
