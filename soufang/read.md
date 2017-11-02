### 爬取房天下的楼盘的评论

**正序思路**
 
首先选择一个城市，上海，进入新房首页面，F12打开network , Doc, 刷新， 翻页
观察路由变化规则，url='http://newhouse.sh.fang.com/house/s/b91/?ctm=1.sh.xf_search.page.1'
发现真正有用的是 url='http://newhouse.sh.fang.com/house/s/b9{}/'.format(page)
这就方便翻页爬取了。

翻到什么时候呢， 尾页可以提取总页数，在首页时可以提取这个数据

要获取索引页的楼盘名字和评论的url, 使用requests 和 pyquery


点击一个评论的详情页，观察路由，打开监听器
url='http://junhuishangpinjzy021.fang.com/dianping/?ctm=1.sh.xf_search.lplist.5'
发现靠谱的url='http://junhuishangpinjzy021.fang.com/dianping/', 中间的差异部分需要从索引页
提取楼盘id .。


但这只是进入评论页的路由，数据不在这里，数据是通过ajax异步方式加载的，在XHR中找到了评论的数据了
url='http://junhuishangpinjzy021.fang.com/house/ajaxrequest/dianpingList_201501.php?city=%E4%B8%8A%E6%B5%B7&newcode=1210125306&jiajing=0&page=3&tid=&pagesize=20&starnum=6&shtag=-1'
city:上海
newcode:1210125306   (从评论详情页获取)
jiajing:0
page:3     当前页面
pagesize:20  (每页的评论数)
starnum:6
shtag:-1
需要传递的参数


