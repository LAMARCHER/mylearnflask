# coding:utf-8
from urllib.request import urlopen, Request
import time

from bs4 import BeautifulSoup

from script.jym import write_db


hs = {
    'Cookie': '$first_referrer=https%3A//www.baidu.com/link; $first_referrer_host=undefined; $first_browser_language=zh-CN; $first_visit_time=1516715428508; $first_referrer=https%3A//www.baidu.com/link; $first_referrer_host=undefined; $first_browser_language=zh-CN; $first_visit_time=1516715404314; TSYUUID=0a239bca-855b-490e-bde3-c335d62cdf74; bgtsyuid=k64b8kfc43u0ejmdqfglrsq3f4; __cfduid=d1d855e76bccb2159b369b5bbfb9ddcfa1516670173; $first_referrer_host=undefined; $first_browser_language=zh-CN; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216120963b2348a-0cb28521c8c36a-454c092b-2073600-16120963b24344%22%2C%22%24device_id%22%3A%2216120963b2348a-0cb28521c8c36a-454c092b-2073600-16120963b24344%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; tsyguestid=tsyguest_EFFEDE8203D2; NTKF_T2D_CLIENTID=guest5E65DA54-BEB7-BF7D-6E84-2096419C4C45; $first_referrer=https%3A//www.baidu.com/link; Hm_lvt_417fdf811fee757b9b1f949949acba5c=1516670171,1516715399; $first_visit_time=1516715399176; nTalk_CACHE_DATA={uid:kf_9098_ISME9754_tsyguest_EFFEDE8203D2,tid:1516715400476654}; Hm_lpvt_417fdf811fee757b9b1f949949acba5c=1516715428',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'upgrade-insecure-requests': 1,
}

request = Request(url=r'https://www.taoshouyou.com/game/mingyun_guanweizhiding-4511-0-0/0-0-2-3-0-0-0-0-0-1?quotaid=0&isinsurance=0', headers=hs)
res = urlopen(request).read().decode('utf-8')
bs = BeautifulSoup(res, 'lxml')
goods = bs.findAll(name='div', attrs={'class': 'row b-trade-list-conlist-box'})
ul = bs.find(name='ul', attrs={'class': 'pagination pull-right'})
pagenumber = (ul.findAll('li')[-2].string).split('/')[-1]


def get_data(goods):
    for good in goods:
        good_name = good.find(name='span', attrs={'class': 'jiage'}).string
        good_price = good.find(name='div', attrs={'class': 'price w100'}).get_text()
        good_id = good.find(name='h1', attrs={'class': 'b-tradelist-h1 title left clearfix js-b-tradelist-h1'})['data-id']
        good_url = 'https://www.taoshouyou.com/taoid_' + good_id + '.html'
        write_db(good_name=good_name, good_id=good_id, good_price=float(good_price), good_url=good_url, source='淘手游')


if __name__ == '__main__':
    for i in range(2, int(pagenumber)+1, 1):
        request = Request(url=r'https://www.taoshouyou.com/game/mingyun_guanweizhiding-4511-0-0/0-0-2-3-0-0-0-0-0-{}?quotaid=0&isinsurance=0'.format(i), headers=hs)
        res = urlopen(request).read().decode('utf-8')
        bs = BeautifulSoup(res, 'lxml')
        goods = bs.findAll(name='div', attrs={'class': 'row b-trade-list-conlist-box'})
        get_data(goods)

        print('当前进度{}/{}'.format(i, pagenumber))
        time.sleep(0.5)