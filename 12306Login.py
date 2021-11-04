"""
12306模拟登录
使用selenium与chromedriver相结合
主要需要解决的是滑动验证的问题
"""
import selenium.webdriver
import time
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 处理chrome驱动伪装，重点处理window.navigator.webdriver被识别为True导致访问失败
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
s = Service('./chromedriver')
browser = selenium.webdriver.Chrome(service=s, options=option)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

# 登录目标地址
browser.get('https://kyfw.12306.cn/otn/resources/login.html')

# 选择“账号登录”
browser.find_element(By.CLASS_NAME, 'login-hd-account').click()

# 输入12306账号密码并提交
browser.find_element(By.ID, 'J-userName').send_keys('12306账号')
browser.find_element(By.ID, 'J-password').send_keys('12306密码')
time.sleep(2)
browser.find_element(By.ID, 'J-login').click()
time.sleep(1)

# 定位滑动验证的滑块并将滑块滑动至最右侧完成验证
span = browser.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
action = ActionChains(browser)
action.click_and_hold(span)
action.move_by_offset(300, 0).perform()
action.release()

time.sleep(10)
print("Login success!")
browser.quit()