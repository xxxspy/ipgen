import requests
from . import paths, regions
import re
from pyquery import PyQuery as pq
import json
import random
import time
from . import cache
from .models import IP



def random_region():
    rs = regions.get_regions()
    name = random.choice(rs.keys())
    return name, rs[name]

def cache_citys():
    '''从网上查找省的ip段, 然后从ip段中随机游走, 以便获取该网段的一些样本数据'''
    for sheng, short in regions.get_regions().items():
        print(sheng, short)
        rngs = regions.get_ip_ranges(sheng)
        print(rngs)
        for start, end in rngs:
            ip = start.rand_between(end)
            print('ip: ', ip)
            info = ip.info
            print(info)
            ip.save()
            time.sleep(0.1)


def expand_province(proname):
    '''增加某个省的ip缓存'''
    rngs = regions.get_ip_ranges(proname)
    for start, end in rngs:
        for i in range(10):
            ip = start.rand_between(end)
            print('ip: ', ip)
            info = ip.info
            print(info)
            ip.save()
            time.sleep(0.1)

def expand_city(cityname):
    ips = cache.select(city=cityname)
    if len(ips) == 0:
        raise ValueError('No cached ip in city {}'.format(cityname))
    if ips:
        for info in ips:
            ip = IP.from_str(info[0])
            for subip in ip.expand():
                subip.save(fetch=True)

def expand_ip_range(start: str, end: str, num=10):
    ip1, ip2 = IP.from_str(start), IP.from_str(end)
    for i in range(num):
        ip = ip1.rand_between(ip2)
        ip.save(True)
        print(ip.info)
            
            
def random_city_ips(city, num):
    ips = cache.select(city=city, limit=num, rnd=True)
    ips = cache.record2obj(ips)
    while len(ips) < num:
        expand_city(city)
        ips = cache.select(city=city, limit=num)
        ips = cache.record2obj(ips)
    return ips


def random_pro_ips(pro, num):
    ips = cache.select(regionName=pro, limit=num, rnd=True)
    ips = cache.record2obj(ips)
    while len(ips) < num:
        expand_province(pro)
        ips = cache.select(regionName=pro, limit=num, rnd=True)
        ips = cache.record2obj(ips)
    return ips


def rand_ips(num):
    ips = cache.select(limit=num, rnd=True)
    ips = cache.record2obj(ips)
    return ips


def gen(num: int, region=None, city=None):
    '''
    region: 省名称
    city: 城市名称
    '''
    if region is None and city is None:
        return rand_ips(num)
    if city is None:
        return random_pro_ips(region, num)
    else:
        return random_city_ips(city, num)

def fetch_range(n, pro, city=''):
    if city:
        url = 'http://ip.yqie.com/cn/{pro}/{city}/'.format(pro=pro, city=city)
    else:
        url = 'http://ip.yqie.com/cn/{pro}/'.format(pro=pro)
    html = requests.get(url).text
    q = pq(html)
    trs = q.find('#GridViewOrder > tr')
    ips = []
    for tr in trs[1:]:
        tds = pq(tr).find('td')
        ips.append((pq(tds[1]).text(), pq(tds[2]).text()))
    return random.sample(ips, n)


def rand_fetch(n, pro, city=''):
    '''从网页抓取IP'''
    m = int(n/10)
    if m > 20:
        m = 20
    elif m < 5:
        m = 5
    ip_segs = fetch_range(m, pro, city)
    ips = []
    while len(ips) < n:
        for s, e in ip_segs:
            ip = IP.from_str(s).rand_between(IP.from_str(e))
            ips.append(ip)
            if len(ips) >= n:
                return ips
    return ips

