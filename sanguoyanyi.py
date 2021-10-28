"""
使用BeautifulSoup库爬取三国演义的小说内容
"""

import requests
from bs4 import BeautifulSoup

hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
}

url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
# 获取章节目录及其链接
catalogResponse = requests.get(url, hd)
catalogResponse.encoding = catalogResponse.apparent_encoding
catalogSoup = BeautifulSoup(catalogResponse.text, 'lxml')
chapters = catalogSoup.select('.book-mulu > ul > li')   # 根据class属性定位获取子节点
fp = open('sanguoyanyi.txt', 'w')   # 提前准备好代存储的文件

# 遍历获取到的章节列表
for chapter in chapters:
    contentUrl = 'https://www.shicimingju.com' + chapter.a['href']
    title = chapter.a.string    # 获取a标签的直接文本
    fp.write('\n\n' + title + '\n')
    contentResponse = requests.get(contentUrl, headers=hd)
    contentResponse.encoding = 'utf-8'
    contentSoup = BeautifulSoup(contentResponse.text, 'lxml')
    fp.write(contentSoup.select('.chapter_content')[0].text)    # 根据class属性定位节点，获取列表第一个元素的文本
    print(title + "\n------已完成------")

fp.close()