'''Fetch IP from http://ip.taobao.com/service/getIpInfo.php?ip=1.85.189.240'''
import sqlite3
from . import paths

'''
{"code":0,"data":{"ip":"1.85.189.240","country":"中国","area":"","region":"陕西","city":"西安","county":"XX",
"isp":"电信","country_id":"CN","area_id":"","region_id":"610000","city_id":"610100","county_id":"xx","isp_id":"100017"}}
'''


KEYS = [
    "query",
    "status",
    "country",
    "countryCode",
    "region",
    "regionName",
    "city",
    "zip",
    "lat",
    "lon",
    "timezone",
    "isp",
    "org",
]
__cnn = None


def connect():
    global __cnn
    if __cnn is None:
        __cnn = sqlite3.connect(str(paths.database))
    return __cnn


def create():
    '''
    {
        "query": "113.251.255.255",
        "status": "success",
        "country": "中国",
        "countryCode": "CN",
        "region": "CQ",
        "regionName": "重庆",
        "city": "重庆",
        "zip": "",
        "lat": 29.563,
        "lon": 106.552,
        "timezone": "Asia/Shanghai",
        "isp": "Chinanet",
        "org": "Chinanet CQ",
        "as": "AS4134 No.31,Jin-rong Street"
    }
    '''
    conn = sqlite3.connect(str(paths.database))
    cols = []
    c = conn.cursor()
    for k in KEYS:
        cols.append('{} char'.format(k))
    c.execute('''CREATE TABLE ips
        ({})'''.format(','.join(cols)))
    c.execute(
        '''
        CREATE UNIQUE INDEX ipindex
        on ips (query);
        '''
    )
    conn.commit()
    conn.close()


def insert(infos):
    sql = 'insert or ignore into ips values ({})'
    cur = connect().cursor()
    try:
        for info in infos:
            ips = info['ip'].split('.')
            values = []
            for k in KEYS:
                values.append(info[k])
            data = sql.format(','.join(values))
            cur.execute(data)
        cur.close()
        connect().commit()
    except:
        cur.close()
        connect().rollback()


def insertone(info):
    insert([info])


def get(ip: str):
    sql = 'select {} from ips where query = "{}"'.format(
        ', '.join(KEYS),
        ip,
    )
    c = connect().cursor()
    c.execute(sql)
    r = c.fetchone()
    if r is None:
        return None
    info = {}
    for i, k in enumerate(KEYS):
        info[k] = r[0]
    return info


def select(**conditions):
    cons = []
    for key, value in conditions.items():
        cons.append('{}="{}"'.format(key, value))
    sql = 'select {} from ips where {};'.format(
        ','.join(KEYS, ' and '.join(cons)))
    c = connect().cursor()
    c.execute(sql)
    res = c.fetchall()
    c.close()
    return res
