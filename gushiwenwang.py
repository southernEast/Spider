"""
模拟登录古诗文网
使用超级鹰做验证码的识别
本程序默认使用手动输入验证码
"""
import requests
from hashlib import md5
from lxml import etree

# 超级鹰的识别相关接口
class Chaojiying_Client(object):
    def __init__(self, username, password, soft_id): # 初始化超级鹰的账户、密码和软件id
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片的字节内容
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
}
# chaojiying = Chaojiying_Client('超级鹰的账号（需自行更改）', '超级鹰的密码（需自行更改）', '924224')    # 初始化一个超级鹰对象用于后续自动识别验证码
mainUrl = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx' # 登录页面的url
session = requests.session() # 初始化一个session，在后续访问中基于同一个session，防止识别出的验证码信息与post上去的内容不符

mainResponse = session.get(url=mainUrl, headers=hd)
mainResponse.encoding = mainResponse.apparent_encoding
tree = etree.HTML(mainResponse.text)

# 抓取页面上以下两个变量的内容以满足后续登录时post需要
viewState = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
viewStateGenerator = tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]

# 处理验证码的内容
picUrl = 'https://so.gushiwen.cn' + tree.xpath('//img[@id="imgCode"]/@src')[0] # 定位验证码图片的url
pic = session.get(url=picUrl, headers=hd).content
with open('a.jpg', 'wb') as fp: # 将验证码在本地保存一份，以作验证
    fp.write(pic)
# 方法一：使用超级鹰做验证码自动识别
# picDict = chaojiying.PostPic(pic, '1902')
# 方法二：根据前面保存下来的a.jpg手动输入验证码内容
picDict = {}
picDict['pic_str'] = input('请输入验证码内容：')

# 进行登录操作
loginUrl = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
data = {
    '__VIEWSTATE': viewState,
    '__VIEWSTATEGENERATOR': viewStateGenerator,
    'from': 'http://so.gushiwen.cn/user/collect.aspx',
    'email': '古诗文网的邮箱地址（需自行更改）',
    'pwd': '古诗文网的密码（需自行更改）',
    'code': picDict['pic_str'],
    'denglu': '登录'
}
loginResponse = session.post(url=loginUrl, headers=hd, data=data)
loginResponse.encoding = loginResponse.apparent_encoding
print(loginResponse.status_code)
with open('page.html', 'w') as fp:  # 将登录后获取到的页面保存在本地查看校验结果
    fp.write(loginResponse.text)