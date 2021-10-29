"""
清晰度较高的图片爬取
使用xpath做数据解析
本程序只爬取一页做测试，如需爬取多页则在外层加一个对pagesUrl的循环即可
"""

import requests
from lxml import etree
import os

hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
}
pagesUrl = 'https://pic.netbian.com/4kfengjing/'    # 图片目录页
pagesResponse = requests.get(url=pagesUrl, headers=hd, timeout=1)
pagesResponse.encoding = pagesResponse.apparent_encoding
pagesTree = etree.HTML(pagesResponse.text)
pages = pagesTree.xpath('//div[@class="slist"]/ul/li/a/@href')  # 当前图片目录页所带的图片url清晰度较低，故获取图片详情页再爬取

# 创建保存图片的文件夹
if not os.path.exists('./img'):
    os.mkdir('./img')

# 遍历图片详情页
for page in pages:
    imgPageUrl = 'https://pic.netbian.com' + page
    imgPageResponse = requests.get(url=imgPageUrl, headers=hd, timeout=3)
    imgPageResponse.encoding = 'utf-8'
    imgPageTree = etree.HTML(imgPageResponse.text)
    
    imgUrl = 'https://pic.netbian.com' + imgPageTree.xpath('//div[@class="photo-pic"]/a/img/@src')[0] # 获取图片链接
    imgResponse = requests.get(url=imgUrl, headers=hd, timeout=3)
    title = imgUrl.split('/')[-1]
    with open('./img/' + title, 'wb') as fp:
        fp.write(imgResponse.content)
    print(title + ' done!!')