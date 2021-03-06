import requests
from . import paths, regions
import re
from pyquery import PyQuery as pq
import json
import random
import time
from . import cache
from .models import IP
from .settings import PROS, BLACK_IPS
import hashlib
import linecache
from . import check



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
    while len(ips) < num or len(ips) < 99:
        expand_city(city)
        ips = cache.select(city=city, limit=num)
        ips = cache.record2obj(ips)
    while len(ips) < num:
        ips.append(random.choice(ips))
        
    return ips


def random_pro_ips(pro, num):
    ips = cache.select(regionName=pro, limit=num, rnd=True)
    ips = cache.record2obj(ips)
    while len(ips) < num:
        expand_province(pro)
        ips = cache.select(regionName=pro, limit=num, rnd=True)
        ips = cache.record2obj(ips)
    return ips

def calcmd5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
    return hash


def load_points():
    fpath = paths.pro_point_info
    fileprint_cal = calcmd5(str(paths.ip_db))
    if not fpath.exists():
        points = {}
        fileprint = ''
    else:
        with open(str(fpath), 'r', encoding='utf8') as fle:
            content = fle.read()
            if not content:
                points = {}
                fileprint = ''
            else:
                data = json.loads(content)
                points = data['points']
                fileprint = data['fileprint']
    if not fileprint or fileprint != fileprint_cal:
        f = open(str(paths.ip_db), 'r', encoding='utf8')
        for pro in PROS:
            f.seek(0)
            i = -1
            for line in f:
                line = line.split('\t')
                i += 1
                if line[5].startswith(pro):
                    points[pro] = i
                    break
        f.close()
        f = open(str(fpath), 'w', encoding='utf8')
        json.dump({'fileprint': fileprint_cal, 'points': points}, f)
        f.close()
    for pro in PROS:
        if pro not in PROS:
            raise ValueError('Not fond province {}'.format(pro))
    return points


def quick_gen(num: int):
    '''快速产生ip, 从样本库里直接获取的'''
    f = open(str(paths.dirty_ips), 'r', encoding='utf8')
    rtn = []
    for i in range(num):
        ip = f.readline().strip()
        if ip:
            rtn.append(ip)
    while len(rtn) < num:
        rtn.append(random.choice(rtn))
    f.close()
    return rtn

def load_ips_from_file(n: int, fname: paths.Path, line_num=100):
    from ipaddress import IPv4Address
    lines = []
    with open(str(fname), 'r', encoding='utf8') as f:
        for i, line in enumerate(f):
            if line:
                lines.append(line)
            if i >= line_num:
                break
    

def gen(num: int, region='', city='', n_region=20):
    '''
    region: 省名称
    city: 城市名称
    '''
    if not city:
        city = ''
    ips = []
    count = 0
    filterd = []
    while len(ips) < num:
        count += 1
        if count > 100000:
            print('已经获取ip:', len(ips), '需要ip:', num)
            print(ips)
            raise ValueError('Reach Loop max count!')
        if not region:
            pro = random.choice(PROS)
        else:
            assert region in PROS
            pro = region
        # p = points[pro] + random.randint(1, 5)
        # found = False
        # ID	StartIPNum	StartIPText	EndIPNum	EndIPText	Country	Local
        # loop_cnt = 0
        line =  linecache.getline(str(paths.ipdir / pro), count)
        info = line.split('\t')
        if info[0].startswith(pro) and city in info[0] and info[1]!=info[2] and info[1] not in filterd:
            invalid = False
            for bip in BLACK_IPS:
                if info[1].startswith(bip) or info[2].startswith(bip):
                    invalid = True
                    break
            if invalid:
                continue
            start = IP.from_str(info[1])
            end = IP.from_str(info[2])
            nper = n_region * 4 if region else n_region # 如果指定了省, 我们可以多取一些重复地区 
            ips.extend(start.sample_between(end, nper))
    check.update_cached()
    return ips
    