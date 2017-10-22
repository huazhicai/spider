# spider

### 工作实战的爬虫脚本

**爬取京东美妆产品的基本信息和客户问答信息**

  在浏览器中观察网络结构，寻找路由规律，和数据的路由。
  列如： 洗面的搜索路由为：
  # 洗面奶
base_url = 'https://search.jd.com/Search?keyword=洗面奶&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=洗面奶&page={}'.format(num)
通过page 数值翻页， 总共一白页面。但是page全是基数相应的对着1到100 ，page=2*i+1 了。

在索引页中获取详情页的url 和产品价格，因为详情页中价格数据读取不出来。

进入到详情页用requests和BeautifulSoup爬取， 产品名称，和商品详情。 并获取特定商品的id号， 作为参数传递给问答路由

商品问答数据在JS中， 找到数据路由，列如： https://question.jd.com/question/getQuestionAnswerList.action?page=1&productId=3785372
因此只需要传递页面数和商品id号就可以爬取了。 但是问答还是在折叠去，每次只能爬取两个答案，因此还要进一步深入爬取，

继续观察答案数据页面的路由， 例如： https://question.jd.com/question/getAnswerListById.action?callback=jQuery1480101&page=1&questionId=4869695
和上面类似，只需要群体id和页数。

因此总共四个级层： 
> 索引页 url= 'https://search.jd.com/Search?keyword=洗面奶&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=洗面奶&page={}'.format(num) 爬取详情页url,和商品价格。
> 详情页 url= 'https://item.jd.com/3785372.html' 爬取商品名称和商品id， 和商品详情。
> 问答也 url= 'https://question.jd.com/question/getQuestionAnswerList.action?page=1&productId=3785372', 爬取问题和问题id
> 回答页 url= 'https://question.jd.com/question/getAnswerListById.action?callback=jQuery2507508&page=1&questionId=4054813' 爬取所有答案

最后保存到mongodb中。