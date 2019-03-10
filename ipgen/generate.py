import requests
from . import paths, regions
import re
from pyquery import PyQuery as pq
import json
import random
import time



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





def random_city_ip(region_name):
    ip_rngs = regions.get_ip_ranges(region_name)


def gen(num: int, region=None, city=None):
    '''
    region: 省名称
    city: 城市名称
    '''
    if region is None :
        region, short = random_region()
    if city is None:
        pass

    