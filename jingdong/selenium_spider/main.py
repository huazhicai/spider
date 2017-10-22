import json
import re
from multiprocessing.pool import Pool

import requests
from requests import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from jingdong.config import *
import pymongo
from json.decoder import JSONDecodeError
import time

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Firefox()
browser.maximize_window()
wait = WebDriverWait(browser, 30)


def search(brand):
    print('正在搜索')
    try:
        browser.get('https://www.jd.com/')
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))
        )
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > div.form > button > i'))
        )
        input.send_keys(KEYWORD+brand)
        submit.click()
        total = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        urls = get_detail_urls()
        return total.text, urls
    except TimeoutException:
        return search(brand)


# 翻页获取所需要的url
def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page_number)))
        urls = get_detail_urls()
        return urls
    except TimeoutException:
        next_page(page_number)


# 在索引页中获取详情页url
def get_detail_urls():
    wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList .gl-warp .gl-item'))
    )
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('a', href=re.compile(r'^//item\.jd\.com/.+?\.html$'))
    results = [i['href'] for i in items]
    return results


# 爬取详情页
def get_detail_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('请求详情页失败')


# 获取特定商品信息
def get_products(url):
    html = get_detail_page(url)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    title = soup.find('div', class_='sku-name').text
    # price = soup.select('.dd')
    introduce = soup.find('ul', class_='parameter2').text
    # href = "//item.jd.com/1318093.html"
    # total = int(re.compile('(\d+)').search(total).group(1))
    product_id = re.compile(r'(\d+)').search(url).group(1)
    questions = get_questions(product_id)
    product = {
        'title': title,
        'introduce': introduce,
        'url': url,
        'questions': questions
    }
    # print(product)
    save_to_mongo(product)


# 解析问答页
def get_questions(id):
    dialogs = []
    page = 1
    while True:
        url = 'https://question.jd.com/question/getQuestionAnswerList.action?page={0}&productId={1}'.format(page, id)
        html = get_detail_page(url)
        try:
            data = json.loads(html)  # 将json转换为字典格式
            if data and data['questionList']:
                for item in data.get('questionList'):
                    question = item['content']
                    answerList = [i['content'] for i in item['answerList']]
                    dialog = {
                        'question': question,
                        'answerList': answerList
                    }
                    dialogs.append(dialog)
                page += 1
            else:
                break
        except JSONDecodeError:
            pass
    return dialogs


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongo成功', result)
    except Exception:
        print('存储到mongo失败', result)


# 获取某个品牌所有详情页的url
def get_all_urls(brand):
    detail_urls = []
    total, urls = search(brand)
    total = int(total)
    detail_urls.extend(urls)
    for i in range(2, 2 + 1):
        result = next_page(i)
        detail_urls.extend(result)
        # break
    return detail_urls


def main(brand):
    urls = get_all_urls(brand)
    for url in set(urls):
        url = 'http:' + url
        get_products(url)


if __name__ == '__main__':
    brands = []
    pool = Pool(processes=3)                                     # 设置进程池中的进程数
    pool.map(main, brands)                           # 将列表中的每个对象应用到get_page_list函数
    pool.close()                                                 # 等待进程池中的进程执行结束后再关闭pool
    pool.join()
    # main()