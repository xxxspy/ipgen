import requests
from . import paths
import re
from pyquery import PyQuery as pq
import json
import random
from .models import IP

Regions = None

def get_regions():
    global Regions
    if Regions is not None:
        return Regions
    if paths.regions_file.exists():
        with open(str(paths.regions_file), 'r', encoding='utf8') as f:
            data = f.read()
        Regions = json.loads(data)
        return Regions
    url = 'http://ips.chacuo.net/'
    html = requests.get(url).text
    links = pq(html).find('ul.list>li>a')
    regions = {}
    for l in links:
        l = pq(l)
        name = l.text().strip()
        href = l.attr('href')
        short = href.split('/')[-1]
        regions[name] = short
    with open(str(paths.regions_file), 'w', encoding='utf8') as f:
        f.write(json.dumps(regions))
    Regions = regions
    return regions

def get_ip_ranges(region_name):
    short = get_regions()[region_name]
    short = short.replace('s_', 'p_')
    url = 'http://ips.chacuo.net/down/t_txt={}'.format(short)
    r = requests.get(url)
    print(url, r)
    lines = r.text.split('\n')
    rtn = []
    for line in lines[1: -1]:
        ip1, ip2, num = line.split()
        ip1, ip2 = IP.from_str(ip1), IP.from_str(ip2)
        rtn.append((ip1, ip2))
    return rtn
