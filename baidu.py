# coding:utf-8
import requests
from lxml import etree


class Tieba(object):

    def __init__(self, name):
        self.url = "https://tieba.baidu.com/f?ie=utf-8&kw={}".format(name)
        print(self.url)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) '
        }

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        # with open("temp.html","wb") as f:
        #     f.write(response.content)
        return response.content

    def parse_data(self, data):
        # 创建element对象
        data = data.decode().replace("<!--", "").replace("-->", "")
        html = etree.HTML(data)
        el_list = html.xpath('//li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a')
        # print(len(el_list))

        data_list = []
        for el in el_list:
            temp = {}
            temp['title'] = el.xpath("./text()")[0]
            temp['link'] = 'http://tieba.baidu.com' + el.xpath("./@href")[0]
            data_list.append(temp)

        # 获取下一页url
        try:
            next_url = 'https:' + html.xpath('//a[contains(text(),"下一页>")]/@href')[0]
        except:
            next_url = None
        return data_list, next_url

    def save_data(self, data_list):
        for dada in data_list:
            print(dada)

    def run(self):

        # url
        # headers
        next_url = self.url
        while True:
            # 发送请求获取相应
            data = self.get_data(self.url)
            # 从响应中提去数据(获取和翻页用的url)
            data_list, next_url = self.parse_data(data)
            self.save_data(data_list)
            print(next_url)
            # 判断是否终结
            if next_url == None:
                break


if __name__ == '__main__':
    tieba = Tieba("李毅")
    tieba.run()
