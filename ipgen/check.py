import requests
from pyquery import PyQuery as pq
import re

_PTN = re.compile(r'本站数据：')

cached = {}
def info(ip):
    ip = str(ip)
    if ip in cached:
        return cached[ip]
    url = 'http://www.ip138.com/ips138.asp?ip={}&ac'.format(ip)
    r = requests.get(url)
    r.encoding='gb2312'
    html = r.text
    html = html.split('本站数据：', 1)[-1]
    content = html.split('<', 1)[0]
    cahed[ip] = content
    return content


if __name__ == '__main__':
    for i in range(200):
        inf = info('14.18.139.{}'.format(i+1))
        print(i, inf)
