import requests
from pyquery import PyQuery as pq
import re

_PTN = re.compile(r'本站数据：')

def info(ip):
    url = 'http://www.ip138.com/ips138.asp?ip={}&ac'.format(ip)
    r = requests.get(url)
    r.encoding='gb2312'
    html = r.text
    html = html.split('本站数据：', 1)[-1]
    content = html.split('<', 1)[0]
    return content


if __name__ == '__main__':
    i = info('14.18.139.74')
    print(i)
