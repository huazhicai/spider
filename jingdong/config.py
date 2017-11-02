MONGO_URL = 'localhost'
MONGO_DB = 'jingdong'

# KEYWORD = '面膜御泥坊'
# SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']



# 面膜
MONGO_TABLE = 'facemask'
base_url = 'https://search.jd.com/Search?keyword=%E6%B4%97%E9%9D%A2%E5%A5%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%B4%97%E9%9D%A2%E5%A5%B6&'


# # 洗面奶
# base_url = 'https://search.jd.com/Search?keyword=%E6%B4%97%E9%9D%A2%E5%A5%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%B4%97%E9%9D%A2%E5%A5%B6&'
# MONGO_TABLE = 'clean_milk'
{'keyword': keyword,
               'enc': 'utf-8',
               'qrst': '1',
               'rt': '1',
               'stop': '1',
               'vt': '2',
               'suggest': '1.his.0.0',
               'page': page}