import requests
from pyquery import PyQuery as pq
import re
from . import paths
import json

_PTN = re.compile(r'本站数据：')
cachfpath = paths.ipdir / 'cached-checked-ips.json'

cached = None
newips = {}
def load_cache():
    global cached
    if cached is None:
        if cachfpath.exists():
            with open(str(cachfpath), 'r', encoding='utf8') as f:
                cached = json.load(f)
        else:
            cached = {}
    return cached


def update_cached():
    if not newips:
        return 
    cached = load_cache()
    with open(str(cachfpath), 'w', encoding='utf8') as f:
        json.dump(cached, f)

def info(ip):
    ip = str(ip)
    cached = load_cache()
    if ip in cached:
        return cached[ip]
    url = 'http://www.ip138.com/ips138.asp?ip={}&ac'.format(ip)
    r = requests.get(url)
    r.encoding='gb2312'
    html = r.text
    html = html.split('本站数据：', 1)[-1]
    content = html.split('<', 1)[0]
    cached[ip] = content
    newips[ip] = content
    return content

def in_area(ip, pro, city=''):
    if not city:
        city = ''
    inf = info(ip)
    return pro in inf and city in inf


if __name__ == '__main__':
    for i in range(200):
        inf = info('14.18.139.{}'.format(i+1))
        print(i, inf)
