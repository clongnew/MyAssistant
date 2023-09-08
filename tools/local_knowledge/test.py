from selenium import webdriver
from chromedriver_py import binary_path

from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import time
import random

collection_url = 'https://www.zhihu.com/collection/512864908'
collection_url = 'https://www.zhihu.com/collection/169110374'
collection_url = 'https://www.zhihu.com/collection/338362696'

# binary_path = '/Users/mac/Downloads/chrome-mac-x64'
service = Service(executable_path=binary_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(collection_url)


# 等待页面加载完成

def f(x):
    href = x.get_attribute('href')
    if href and ('answer' in href or 'zhuanlan' in href):
        return href
    else:
        return None


links = []
while True:
    driver.implicitly_wait(10)

    page_links = driver.find_elements(By.CSS_SELECTOR, 'a')
    print('原始 page_links: ', page_links, '\n')
    page_links = [f(x) for x in page_links if f(x)]
    #     page_links = driver.execute_script("""
    #         return Array.from(document.querySelectorAll('a'))
    #             .map(a => a.href)
    #             .filter(href => href.includes('answer') || href.includes('zhuanlan'))
    #     """)
    print(page_links, '---\n')
    links += page_links

    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.PaginationButton-next')))

    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 检查是否找到下一页按钮，如果没有就退出循环
    if not next_button:
        break
    print(next_button)
    # 模拟鼠标点击下一页按钮
    time.sleep(3 + random.random())
    actions = ActionChains(driver)
    actions.move_to_element(next_button).click().perform()
    driver.implicitly_wait(10)

#     next_button.click()
driver.quit()
print('-----length-----: {}'.format(len(links)))
