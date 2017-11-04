# 爬取房天下的楼盘的评论


# 获取城市名称
import re

import requests
from bs4 import BeautifulSoup


def get_city():
    url = 'http://www.fang.com/SoufunFamily.htm'
    html_content = requests.get(url)
    # <a href="http://gaoling.fang.com/" target="_blank">高陵</a>
    pattern = re.compile(r'<a href="http://(\w+)\.fang\.com/" target="_blank">.+?</a>', re.S)
    items = re.findall(pattern, html_content.text)
    print(len(set(items)))
    print(set(items))


# get_city()

CITYS = ['yt', 'zaozhuang', 'zhongwei', 'qianxi', 'boluo', 'hegang', 'yl', 'yunfu', 'meishan', 'fq', 'yangchun',
         'linzhi', 'rudong', 'mengjin', 'feicheng', 'zhucheng', 'bengbu', 'huainan', 'dongxing', 'xinmi', 'linqu',
         'luanxian', 'jingmen', 'wenan', 'zb', 'huzhou', 'yuzhong', 'xf', 'fenghua', 'us', 'longkou', 'lijiang',
         'ganzi', 'hbjz', 'sz', 'tl', 'hbzy', 'minqing', 'gongzhuling', 'laiwu', 'gxby', 'qingzhen', 'zz', 'anqing',
         'linfen', 'ruian', 'xinghua', 'feixi', 'lujiang', 'njgc', 'anning', 'jxfc', 'tongshan', 'anyang', 'luoning',
         'pingtan', 'shiyan', 'chengde', 'wuzhong', 'zhouzhi', 'liaozhong', 'qingxu', 'zhaotong', 'jm', 'jiaozhou',
         'taishan', 'tc', 'hechi', 'whhn', 'anshun', 'xinyi', 'wuhan', 'huaiyuan', 'xj', 'yingtan', 'jlys', 'ruijin',
         'lyg', 'xlglm', 'changge', 'changli', 'honghe', 'huaibei', 'bazhong', 'longhai', 'chifeng', 'ld', 'macau',
         'heyuan', 'mudanjiang', 'yilan', 'xiangxiang', 'zjfy', 'panzhihua', 'jiujiang', 'tieling', 'xiuwen', 'faku',
         'jinxian', 'hbyc', 'benxi', 'hlbe', 'jiaonan', 'deqing', 'shaoyang', 'bijie', 'shangrao', 'heihe', 'suizhou',
         'nanjing', 'alaer', 'germany', 'jimo', 'anqiu', 'wujiaqu', 'baoji', 'qinzhou', 'wuzhishan', 'guan', 'jiangdu',
         'yuxian', 'liyang', 'xinjin', 'jiayuguan', 'huizhou', 'tongling', 'haiyang', 'jintan', 'gaomi', 'kuitun', 'yc',
         'ruyang', 'erds', 'shangyu', 'xiaogan', 'xinyu', 'dz', 'tmsk', 'zjxs', 'huangshan', 'baishan', 'yongcheng',
         'huidong', 'pengzhou', 'lnta', 'hengxian', 'taizhou', 'ly', 'luanchuan', 'ziyang', 'anshan', 'huadian',
         'qingyang', 'datong', 'st', 'kelamayi', 'tulufan', 'tonghua', 'jiande', 'qianan', 'zhoukou', 'guangrao',
         'yongkang', 'chuzhou', 'liupanshui', 'changdu', 'ny', 'zs', 'huangshi', 'xianning', 'kaifeng', 'spain',
         'diqing', 'ruzhou', 'hbbz', 'jh', 'sf', 'tongchuan', 'dengfeng', 'wafangdian', 'yuncheng', 'cd', 'aj',
         'zhangye', 'pulandian', 'laizhou', 'jinhu', 'changchun', 'zigong', 'qiannan', 'loudi', 'sdpy', 'ali',
         'gaobeidian', 'dengzhou', 'kaiyang', 'jiaozuo', 'yiyang', 'xinmin', 'dujiangyan', 'dingxing', 'ytcd',
         'yueyang', 'yongtai', 'penglai', 'cangzhou', 'huoqiu', 'shihezi', 'huaihua', 'jieyang', 'fanchang', 'jn',
         'linqing', 'tengzhou', 'nujiang', 'cswc', 'lf', 'pingliang', 'wg', 'zy', 'bazhou', 'tianshui', 'pizhou',
         'dehui', 'malaysia', 'weinan', 'xiantao', 'tj', 'lnzh', 'changshu', 'fuyang', 'sansha', 'hbwj', 'dh', 'yuxi',
         'taixing', 'meizhou', 'xm', 'zhangzhou', 'linan', 'ahsuzhou', 'zoucheng', 'yinchuan', 'chizhou', 'heze',
         'peixian', 'jinchang', 'ganzhou', 'funing', 'jingdezhen', 'wuzhou', 'bh', 'huaian', 'xuchang', 'chaoyang',
         'jz', 'lvliang', 'yk', 'qz', 'la', 'anda', 'dianpu', 'cq', 'ksys', 'chicago', 'gaoyang', 'shuyang', 'gdlm',
         'sh', 'hz', 'gz', 'songyuan', 'nc', 'dongtai', 'changle', 'sg', 'cqnanchuan', 'leiyang', 'nanan',
         'zhangjiajie', 'greece', 'shunde', 'guangyuan', 'baoshan', 'tongren', 'linxia', 'dangtu', 'huludao', 'wz',
         'yongdeng', 'hetian', 'xingtai', 'haiyan', 'sdjy', 'boston', 'donggang', 'jy', 'rz', 'yuhuan', 'wuan',
         'guzhen', 'dali', 'ningde', 'neijiang', 'fangchenggang', 'sdsh', 'xn', 'nanyang', 'tongcheng', 'nn', 'hnyz',
         'jixi', 'chuxiong', 'emeishan', 'laixi', 'betl', 'chaozhou', 'deyang', 'sdcl', 'xz', 'dongfang', 'gongyi',
         'pinghu', 'jl', 'qd', 'sanming', 'xt', 'maoming', 'zhijiang', 'haimen', 'lianjiang', 'xinjian', 'sq',
         'yanbian', 'guyuan', 'hami', 'qianjiang', 'yongning', 'suining', 'yibin', 'jxja', 'wlcb', 'dayi', 'sxly',
         'dangyang', 'haining', 'lantian', 'lc', 'hd', 'puyang', 'qitaihe', 'quanshan', 'dingxi', 'jx', 'weihai', 'dy',
         'chaohu', 'bozhou', 'bj', 'kashi', 'yili', 'jiuquan', 'ningxiang', 'ahcf', 'xuancheng', 'xinji', 'luzhou',
         'heshan', 'shangzhi', 'zjtl', 'alsm', 'baicheng', 'wuchang', 'chunan', 'kaili', 'zhaoqing', 'cqliangping',
         'lasa', 'cqchangshou', 'haian', 'qujing', 'hbjs', 'huian', 'liling', 'yangquan', 'jingjiang', 'jianyang',
         'jiyuan', 'zhenjiang', 'hbql', 'shanwei', 'wuhu', 'zj', 'rikaze', 'feidong', 'daqing', 'pingxiang', 'cqwulong',
         'xianyang', 'aba', 'zhangjiakou', 'agent', 'byne', 'pingdu', 'shizuishan', 'wuhe', 'jinzhou', 'my', 'liuyang',
         'huxian', 'zhoushan', 'tianmen', 'qixia', 'zhaoyuan', 'zhuji', 'jizhou', 'enshi', 'cqtongliang', 'jncq',
         'hezhou', 'yangqu', 'zhongmou', 'fengcheng', 'tz', 'yuyao', 'bulgaria', 'dxal', 'fushun', 'yichun', 'jr',
         'qingyuan', 'baoying', 'baise', 'xingyang', 'haidong', 'yixing', 'pingdingshan', 'hanzhong', 'lhk', 'yanshi',
         'cqzhongxian', 'zh', 'xinyang', 'hengyang', 'au', 'youxian', 'guilin', 'hbys', 'renqiu', 'putian', 'luan',
         'nt', 'mianyang', 'xishuangbanna', 'gaoyou', 'shangluo', 'quangang', 'puer', 'xam', 'yangjiang', 'qionglai',
         'yizheng', 'wuwei', 'jiamusi', 'yutian', 'zhangqiu', 'haixi', 'shannan', 'hnyy', 'cn', 'xinzheng', 'portugal',
         'jiangyan', 'enping', 'bt', 'liuzhou', 'kangping', 'luannan', 'jc', 'longyan', 'dandong', 'zunyi', 'hailin',
         'sxyulin', 'wushan', 'hebi', 'laiyang', 'hailaer', 'changyi', 'rugao', 'yanling', 'cyprus', 'zouping', 'hbzx',
         'xintai', 'scjt', 'hbps', 'xx', 'nanping', 'luoyuan', 'xinle', 'fengdu', 'hblt', 'changde', 'cz', 'wanning',
         'sx', 'yz', 'laishui', 'huangnan', 'xilinhaote', 'zhaodong', 'zhuozhou', 'liangshan', 'jxfuzhou', 'yidu',
         'wenling', 'yanan', 'fs', 'hnxa', 'zunhua', 'dl', 'fuan', 'binzhou', 'liaoyang', 'jinzhong', 'xiangxi', 'sjz',
         'leshan', 'yueqing', 'bayan', 'xinzhou', 'nanchong', 'jssn', 'huanggang', 'hljyichun', 'chongzuo', 'guoluo',
         'ninghai', 'bd', 'fuling', 'yancheng', 'quzhou', 'yiwu', 'nb', 'nongan', 'fjax', 'zhumadian', 'donghai', 'cs',
         'qhd', 'dazhou', 'cixi', 'ezhou', 'puning', 'gannan', 'guigang', 'zhaozhou', 'taian', 'yongqing', 'haicheng',
         'dehong', 'sanmenxia', 'shuozhou', 'zhenhai', 'qidong', 'wuxi', 'siping', 'abazhou', 'sy', 'danzhou',
         'dingzhou', 'jsfx', 'tongxiang', 'ls', 'qianxinan', 'yaan', 'fuxin', 'shishi', 'linhai', 'shangqiu', 'zjg',
         'chongzhou', 'luohe', 'huairen', 'shaoguan', 'cqkaixian', 'xian', 'naqu', 'yushu', 'akesu', 'xiangyang',
         'ankang', 'fz', 'kuerle', 'qj', 'suzhou', 'baiyin', 'cqjiangjin', 'jian', 'dg', 'kzls', 'kaiping', 'longnan',
         'wenshan', 'panjin', 'ks', 'songxian', 'haibei', 'changxing', 'chenzhou', 'linyi', 'jingzhou', 'hn',
         'qingzhou', 'ya', 'guangan', 'laibin', 'qiqihaer', 'yongchun', 'wf', 'zhongxiang', 'binxian', 'lincang',
         'changzhi', 'gaoling', 'yongzhou', 'lankao', 'zhuzhou', 'hs', 'qiandongnan', 'wuhai', 'yichuan', 'shennongjia',
         'shuangyashan', 'suihua', 'jining', 'liaoyuan', 'mas']
