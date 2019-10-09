import urllib
import urllib.parse
import requests
import random
from lxml import etree
from bs4 import BeautifulSoup

class Response():
    def __init__(self, url, data=None):
        self.url = url
        self.data = data
        self.headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4', 'cookie': None},
                        {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36', 'cookie': None},
                        {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36', 'cookie': None}]
    def urllib_req(self):
        if self.data:
            self.data = bytes(urllib.parse.urlencode(self.data), encoding='utf-8')
            req = urllib.request.Request(url=self.url, headers=self.headers[random.randint(0, 2)], data=self.data)
            response = urllib.request.urlopen(req)
        else:
            req = urllib.request.Request(url=self.url, headers=self.headers[random.randint(0, 2)])
            response = urllib.request.urlopen(req)
        return response
    def requests_req(self):
        if self.data:
            response = requests.post(url=self.url, headers=self.headers[random.randint(0, 2)], data=self.data)
        else:
            response = requests.get(url=self.url, headers=self.headers[random.randint(0, 2)])
        response.encoding = 'utf-8'
        return response
    def xpath_analytic(self):
        response = self.requests_req().text
        html = etree.HTML(response)
        return html
    def bs4_analytic(self):
        response = self.requests_req().text
        soup = BeautifulSoup(response, 'lxml')
        return soup
    def file_save_csv(self,name,l):
        tab_head = ','.join(l[0].keys()) + '\n'  # 写入表头
        # 列表l的第一个元素是字典
        # 通过keys()函数取得字典的键名
        # 以 , 作为分隔符（将键名写入csv）
        with open(f'{name}.csv', 'a', encoding='utf-8') as f:
            f.write(tab_head)
            # 以 , 作为分隔符将键名写入csv
            # print(f'tab_head:{tab_head}')       # 输出表头
            s = "i['%s']," * len(l[0])  # 写入内容
            # 通过len()获取列表l的长度，决定写入次数
            # i['%s'] == 字典名['键名'] == dic['name'] 通过键名索引到键值
            s1 = eval('s % tuple(l[0].keys())')  # 将字典键值转换为元组
            # 列表l的第一个元素是字典          {'a': '1', 'b': '2'}
            # 通过keys()函数取得字典的键名     (a, b)

            # s1 = eval('"i['%s']," * len(l[0]) % tuple(l[0].keys())')
            # "i['%s']," * len(l[0])        写入次数
            # % tuple(l[0].keys())          写入内容

            # print(s1)
            for i in l:
                # print(eval(s1), '==', type(eval(s1)))
                f.write(','.join(eval(s1)) + '\n')

