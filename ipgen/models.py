import requests
from . import cache
import random


class IP:
    def __init__(self, ip1, ip2, ip3, ip4):
        self.ip1 = int(ip1)
        self.ip2 = int(ip2)
        self.ip3 = int(ip3)
        self.ip4 = int(ip4)
        self._info = None

    @property
    def value(self):
        return self.ip4 + self.ip3 * 1000 + self.ip2 * (1000**2) + self.ip1 * (1000**3)

    def __str__(self):
        return '.'.join([str(d) for d in self.data()])

    def __repr__(self):
        return '<IP {} >'.format(self)

    def __eq__(self, value: 'IP'):
        return self.value == value.value

    def __lt__(self, value: 'IP'):
        return self.value.__lt__(value.value)

    def __gt__(self, value: 'IP'):
        return self.value.__gt__(value.value)

    def __ge__(self, value: 'IP'):
        return self.value.__ge__(value.value)

    def __le__(self, value: 'IP'):
        return self.value.__le__(value.value)

    def __add__(self, step: int):
        ip4 = self.ip4 + step
        if ip4 <= 255:
            self.ip4 = ip4
        else:
            pre = self.ip4
            self.ip4 = 255
            self.next()
            self.ip4 += (step - (255-pre) )
        self._info = None


    def next(self):
        if self.ip4 < 255:
            self.ip4 += 1
        elif self.ip3 < 255:
            self.ip3 += 1
            self.ip4 = 0
        elif self.ip2 < 255:
            self.ip2 += 1
            self.ip3 = 0
            self.ip4 = 0
        elif self.ip1 < 255:
            self.ip1 += 1
            self.ip2 = 0
            self.ip3 = 0
            self.ip4 = 0
        self._info = None

    def data(self):
        return [self.ip1, self.ip2, self.ip3, self.ip4]

    def copy(self):
        return IP(*self.data())

    @classmethod
    def from_str(cls, ip: str):
        ip = ip.strip()
        data = ip.split('.')
        data = [int(d) for d in data]
        return cls(*data)

    @classmethod
    def from_value(cls, value: int):
        ip4 = value % 1000
        ip3 = int(value / 1000) % 1000
        ip2 = int(value / (1000**2)) % 1000
        ip1 = int(value / (1000 ** 3)) % 1000
        return cls(ip1, ip2, ip3, ip4)

    @property
    def info(self):
        if self._info is None:
            self._info = self.fetch_info()

    def fetch_info(self)->dict:
        info = cache.get(str(self))
        if info is None:
            url = 'http://ip-api.com/json/{}?lang=zh-CN'.format(
                self)
            print(url)
            r = requests.get(url)
            print(r.text)
            return r.json()
        else:
            return info

    def save(self):
        if self._info is not None:
            cache.insertone(self._info)

    def __del__(self):
        self.save()

    def rand_between(self, ip: 'IP'):
        i1 = random.randint(min(self.ip1, ip.ip1), max(self.ip1, ip.ip1))
        i2 = random.randint(min(self.ip2, ip.ip2), max(self.ip2, ip.ip2))
        i3 = random.randint(min(self.ip3, ip.ip3), max(self.ip3, ip.ip3))
        i4 = random.randint(min(self.ip4, ip.ip4), max(self.ip4, ip.ip4))
        ip = IP(i1, i2, i3, i4)
        return ip
