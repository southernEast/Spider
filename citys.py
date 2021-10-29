"""
全国主要城市名爬取
使用path做数据解析
"""
from lxml import etree
import requests

hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
}
url = 'https://www.aqistudy.cn/historydata/'
response = requests.get(url=url, headers=hd)
response.encoding = response.apparent_encoding
tree = etree.HTML(response.text)

# 获取热门城市
hotCitys = tree.xpath('//div[@class="hot"]//a/text()') # 定位hot属性的div然后跳转到其下的a标签
print("热门城市: {}".format(hotCitys))

# 获取全部城市
allCitys = tree.xpath('//div[@class="all"]//a/text()') # 定位all属性的div然后跳转到其下的a标签
print("全部城市：{}".format(allCitys))