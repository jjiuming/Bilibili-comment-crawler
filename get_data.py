import time
import pandas as pd
from os import makedirs
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.by import By

# INDEX_URL = "https://t.bilibili.com/774047106626224280"
INDEX_URL = "https://www.bilibili.com/video/BV1Mc411H7zP"

RESULTS_DIR = 'results'
RESULTS_FILE = 'comments.xlsx'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def crawlComments():

    print('hi*1')
    # 反屏蔽选项设置
    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    print('hi*2')
    browser = webdriver.Chrome(options=options)

    print('hi*3')
    try:
        print('hi*4')
        browser.get(INDEX_URL)

        # 判断是否有元素:loading-state 文本：没有更多评论
        js = "window.scrollTo(0,document.body.scrollHeight)"
        end = browser.find_element(By.CSS_SELECTOR, ".loading-state")
        while True:
            browser.execute_script(js)
            time.sleep(2)
            end = browser.find_element(By.CSS_SELECTOR, ".loading-state")
            if end.text == "没有更多评论":
                break

        # 提取评论
        names = browser.find_elements(By.CSS_SELECTOR, ".con > .user > .name")
        texts = browser.find_elements(By.CSS_SELECTOR, ".con > .text")
        times = browser.find_elements(By.CSS_SELECTOR, ".con > .info > .time-location")

        # 将评论转换为数据列表
        data = []

        for i in range(len(names)):
            # 将图标替换为文本
            if texts[i].text == "":
                temp = texts[i].find_element(By.CSS_SELECTOR, "img").get_attribute("alt")
            else:
                temp = texts[i].text
            data.append((names[i].text, temp, times[i].text))

    except Exception:
        print("访问超时")

    # 将评论数据保存到 Excel 文件中
    header = ["ID", "留言", "时间"]
    df = pd.DataFrame(data, columns=header)
    df.to_excel(f'{RESULTS_DIR}/{RESULTS_FILE}', index=False, header=header)

if __name__ == '__main__':
    html = crawlComments()  # 爬取评论