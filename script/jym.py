# coding:utf-8
from urllib.request import urlopen, Request
import re, time

from bs4 import BeautifulSoup
import pymysql

dbconfig = {
          'host': '127.0.0.1',
          'port': 3306,
          'user': 'root',
          'password': '123456',
          'db': 'spider',
          'charset': 'utf8mb4',
          'cursorclass': pymysql.cursors.DictCursor,
          }
connection = pymysql.connect(**dbconfig)


hs={
    'Cookie': 'ssids=1514025775240236; historyScanGame=%5B%224514%22%2Cnull%5D; sfroms=JIAOYIMALL001; Hm_lvt_63bfdb121fda0a8a7846d5aac78f6f37=1514025776,1516426118,1516521996; Hm_lpvt_63bfdb121fda0a8a7846d5aac78f6f37=1516522032',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Upgrade-Insecure-Requests': 1
}
request = Request(url='https://www.jiaoyimao.com/g4514-c1476177217117636/p1-r4.html', headers=hs)
res = urlopen('https://www.jiaoyimao.com/g4514-c1476177217117636/p1-r4.html')
doc = res.read().decode('utf-8')
bs = BeautifulSoup(doc, "lxml")
goods = bs.findAll(name='li', attrs={'name': 'goodsItem'}, limit=2)

good_name = ''
good_url = ''
good_price = ''
good_id = ''
page_text = (bs.find('div', attrs={'class': 'mod-page'})).get_text().replace(' ', '').replace('\n', '')
page_number = int(re.search('>.(\d*)', page_text).groups()[0])


def urls_open(number=page_number):
    urls = ('https://www.jiaoyimao.com/g4514-c1476177217117636/p1-r4-n' + str(i + 2) + '.html' for i in range(page_number))
    i = 2
    for url in urls:
        if i == number + 2:
            break
        request = Request(url=url, headers=hs)
        res = urlopen(request)
        doc = res.read().decode('utf-8')
        bs = BeautifulSoup(doc, 'lxml')
        goods = bs.findAll(name='li', attrs={'name': 'goodsItem'})
        get_datas(goods)
        print('当前页数:{}/{}'.format(i, page_number))
        i += 1
        time.sleep(1)


def get_datas(goods):
    if not goods:
        return 'goods没了'
    for good in goods:
        data_id = good.find(name='span', attrs={'class': 'is-account'})['data-id']
        good_name = good.a.string
        good_id = data_id
        good_url = 'https://www.jiaoyimao.com/goods/' + good_id + '.html'
        good_price = good.find('span', attrs={'class': 'price'}).string
        print('good_id:{good_id}, good_name: {good_name}, good_url: {good_url}, good_price: {good_price}'.format(good_price=good_price, good_name=good_name,
                                                                                                                 good_id=good_id, good_url=good_url))
        write_db(good_name, good_id, good_url, float(good_price))


def write_db(good_name, good_id, good_url, good_price):
    with connection.cursor() as cursor:
        sql = 'insert into fate_mh_goods (good_name, good_url, good_id, good_price ) values (%s, %s, %s, %s)'
        cursor.execute(sql, (good_name, good_url, good_id, good_price))
        connection.commit()


if __name__ == '__main__':
    try:
        urls_open()
    except Exception as e:
        print(e)
    finally:
        connection.close()
        print('db连接关闭.')
