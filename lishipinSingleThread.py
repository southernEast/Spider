"""
抓取梨视频上的视频数据并保存于本地
本程序为单线程版本
"""
import requests
from lxml import etree
import random
import re
import os

hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
}
mainUrl = 'https://www.pearvideo.com/category_5' # 目标主网页
mainText = requests.get(url=mainUrl, headers=hd).text
mainTree = etree.HTML(mainText)
videoIdList = mainTree.xpath('//ul[@id="categoryList"]/li/div[@class="vervideo-bd"]/a/@href')   # 获取一页最新视频ID列表

# 创建视频文件夹
if not os.path.exists('videos'):
    os.mkdir('videos')

for videoId in videoIdList:
    videoId = videoId.split('_')[-1]    # 分离视频ID的数字
    data = {
        'contId': videoId,
        'mrd': random.random()
    }
    hd2 = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Referer': 'https://www.pearvideo.com/video_' + videoId # 需要有这个属性才能够正常访问
    }
    videoJspUrl = 'https://www.pearvideo.com/videoStatus.jsp'
    videoJspResponse = requests.get(url=videoJspUrl, headers=hd2, params=data)
    videoUrl = videoJspResponse.json()["videoInfo"]["videos"]["srcUrl"] # 获取到视频链接
    
    # ajax直接获取到的链接无法正常访问，需根据规律对链接进行处理
    videoUrlElementList = videoUrl.split('-')
    videoUrlElementList[0] = re.split(r'\d+$', videoUrlElementList[0])[0]   # 删去末尾的数字并取得列表第一个元素
    videoUrlElementList[0] += 'cont'
    videoUrlElementList.insert(1, videoId)
    newVideoUrl = '-'.join(videoUrlElementList)

    # 获取视频的内容
    video = requests.get(url=newVideoUrl, headers=hd).content

    title = newVideoUrl.split('/')[-1]
    with open('./videos/' + title, 'wb') as fp:
        fp.write(video)
    print(title + ' is done!')