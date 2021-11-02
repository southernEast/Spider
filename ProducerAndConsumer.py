"""
生产者消费者模式爬虫
其中几个线程用于获取链接，另外几个线程用于解析链接
"""
import requests
from lxml import etree
import queue
import threading
import time
import random

# 获取url的HTML内容
def getHtml(url):
    r = requests.get(url, hd)
    return r.text

# 解析HTML数据，此处以解析文章的标题为示例
def getTitle(html):
    tree = etree.HTML(html)
    return tree.xpath('//a[@class="post-item-title"]/text()')

# 执行获取HTML内容，传入url队列和html队列
def doGetHtml(urlQueue: queue.Queue, htmlQueue: queue.Queue):
    while not urlQueue.empty():
        url = urlQueue.get()
        html = getHtml(url)
        htmlQueue.put(html) # 获取到的HTML内容加入队列
        print(threading.current_thread().name, f'craw {url}', f'size: {len(html)}')
        time.sleep(random.randint(1, 2))

# 执行解析HTML数据，传入html队列和输出文件流
def doGetTitle(htmlQueue: queue.Queue, fout):
    while True:
         # get为阻塞操作，若5秒内仍然未获取到html元素则表示解析结束
        try:
            html = htmlQueue.get(timeout=5)
        except:
            print('All HTMLs are done!')
            break

        titles = getTitle(html)
        for title in titles:
            fout.write(title + '\n')
        print(threading.current_thread().name, f'size: {len(html)}')

if __name__ == '__main__':
    hd = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    }
    urls = [f'https://www.cnblogs.com/#p{page}' for page in range(1, 51)]

    # 初始化两个队列
    urlQueue = queue.Queue()
    htmlQueue = queue.Queue()
    for url in urls:
        urlQueue.put(url)
    
    # 创建4个线程用于获取HTML页面数据
    for i in range(4):
        t = threading.Thread(target=doGetHtml, args=(urlQueue, htmlQueue), name=f'craw {i}')
        t.start()
    
    fout = open('./data.txt', 'w')
    # 创建2个线程用于解析HTML数据
    for i in range(2):
        t = threading.Thread(target=doGetTitle, args=(htmlQueue, fout), name=f'parse {i}')
        t.start()
