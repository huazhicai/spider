import json
import re
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from json.decoder import JSONDecodeError
from soufang.config import *


# 获取索引页的html
def get_index_page(city, page):
    url = 'http://newhouse.{0}.fang.com/house/s/b9{1}/'.format(city, page)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('[{0}] Get index {1}'.format(city, url))
            return response.text
        return None
    except RequestException:
        print('{0} 请求索引页失败: {1}'.format(city, url))


# 获取总页码
def get_total_page(city):
    url = 'http://newhouse.{}.fang.com/house/s/'.format(city)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                page_pattern = re.compile(r'<a class="last" .*?/b9(\d+)/".*?</a>', re.S)
                total = page_pattern.search(response.text).group(1)
                return total
            except:
                return 1
        return None
    except RequestException:
        print('获取总页失败: {}'.format(url))


# 解析索引页，评论路由
def parser_index_page(html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.select('div.nlcd_name > a')
    for url in results:
        yield url.get('href')


# 获取评论页的html
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('请求评论页失败: {}'.format(url))


# 解析评论页，获取newcode， 和city
def parser_comment(html):
    html_doc = html.encode('ISO-8859-1')
    soup = BeautifulSoup(html_doc, 'lxml')
    newcode_pattern = re.compile(r"var .*?ewcode = .*?(\d+).*?;", re.S)
    city_pattern = re.compile(r"var .*?city = .*?(\w+).*?;", re.S)
    print(soup.text)
    city = city_pattern.search(soup.text, re.S).group(1)
    newcode = newcode_pattern.search(soup.text).group(1)
    return city, newcode


# 获取评论
def get_comments(item, city, newcode):
    url = '{}house/ajaxrequest/dianpingList_201501.php'.format(item)
    page = 1
    while True:
        payload = {
            'city': city,
            'newcode': newcode,
            'jiajing': 0,
            'page': page,
            'tid': '',
            'pagesize': 20,
            'starnum': 6,
            'shtag': -1,
        }
        try:
            response = requests.get(url, params=payload)
            try:
                data = json.loads(response.text)
                if data and data['list']:
                    print('[{0}] Crawl {1}'.format(city, response.url))
                    for item in data.get('list'):
                        if item:
                            write_to_file(city, item.get('content'))
                    page += 1
                else:
                    break
            except JSONDecodeError as e:
                print("json解析失败", str(e))
                break
        except RequestException as e:
            print('请求失败', str(e))


# 保存到文件中
def write_to_file(city, content):
    with open('comments/{}.txt'.format(city), 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n\n')


def main(city):
    total = int(get_total_page(city))
    page = 10
    while page <= 10:
        html = get_index_page(city, page)
        if html:
            for item in parser_index_page(html):
                item = re.search(r'http://.*?\.fang\.com/', item).group()  # 正则匹配消掉无效的路径
                print(item)
                url = item + 'dianping/'
                html = get_one_page(url)
                urban, newcode = parser_comment(html)
                get_comments(item, urban, newcode)
            page += 1


if __name__ == '__main__':
    main('sy')
    # pool = Pool(processes=4)                        # 设置进程池中的进程数
    # pool.map(main, CITYS)                # 将列表中的每个对象应用到get_page_list函数
    # pool.close()                         # 等待进程池中的进程执行结束后再关闭pool
    # pool.join()
