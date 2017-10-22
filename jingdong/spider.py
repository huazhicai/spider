import json
import re
from multiprocessing.pool import Pool

import pymongo
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from json.decoder import JSONDecodeError
from config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


# 提取索引页的html
def get_page_index(page):
    # 向路由中出入参数
    url = base_url + 'page={}'.format(page)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None


# 解析索引页的html，并提取详情页url, price
def parse_page_index(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('.p-name a[href^="//item.jd.com/"]')
    prices = soup.select('.p-price i')
    for item, price in zip(items, prices):
        yield ('http:' + item['href'], price.text)


# 获取详情页面的html代码
def get_page_detail(url):
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None


# 解析详情页面并提取product_name, brand, price, product_id
def parse_page_detail(html, url, price=None):
    soup = BeautifulSoup(html, 'lxml')
    # 爬取过程中有商品brand为空，所以加了try
    try:
        brand = soup.select('#parameter-brand a')[0].text
    except:
        brand = None
    name = soup.select('title')[0].get_text()
    introduction = [i.text for i in soup.select('.parameter2 li')]
    product_id = re.compile(r'(\d+)').search(url).group(1)
    questions = get_questions(product_id)
    product = {
        'brand': brand,
        'name': name,
        'price': price,
        'url': url,
        'introduction': introduction,
        'questions': questions
    }
    return product


# 解析问答页, 提取问题和问题id号
def get_questions(id):
    dialogs = []
    page = 1
    while True:
        url = 'https://question.jd.com/question/getQuestionAnswerList.action?page={0}&productId={1}'.format(page, id)
        html = get_page_detail(url)
        try:
            data = json.loads(html)  # 将json转换为字典格式
            if data and data['questionList']:
                for item in data.get('questionList'):
                    question_id = item['id']
                    question = item['content']
                    answerList = get_answers(question_id)
                    dialog = {
                        'question': question,
                        'answerList': answerList
                    }
                    dialogs.append(dialog)
                page += 1
            else:
                break
        except Exception:
            pass
    return dialogs


# 解析回答页，提取所有的答案
def get_answers(id):
    answers = []
    page = 1
    while True:
        url = 'https://question.jd.com/question/getAnswerListById.action?page={0}&questionId={1}'.format(page, id)
        html = get_page_detail(url)
        try:
            data = json.loads(html)  # 将json转换为字典格式
            if data and data['answers']:
                answer_list = [answer['content'] for answer in data['answers']]
                answers.extend(answer_list)
                page += 1
            else:
                break
        except JSONDecodeError:
            pass
    return answers


# 把详情页面的url和标题（title)以及组图的地址list保存到mongo中
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False


def main(page):
    html = get_page_index(page)
    parse_page_index(html)
    for url, price in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url, price)
            if result: save_to_mongo(result)


if __name__ == '__main__':
    # main(1)
    pages = [2 * i + 1 for i in range(100)]
    pool = Pool(processes=3)  # 设置进程池中的进程数
    pool.map(main, pages)  # 将列表中的每个对象应用到get_page_list函数
    pool.close()  # 等待进程池中的进程执行结束后再关闭pool
    pool.join()
