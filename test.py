from ipgen import cache, regions, generate, paths
import unittest
from ipgen.models import IP


# cache.create()
# cache.get('dfdlkjdlfj')

# r = regions.get_ranges('河北')
# print(r[0][0].fetch_info())


class Test(unittest.TestCase):

    def test_get_regions(self):
        rgs = regions.get_regions()
        self.assertEqual(len(rgs), 32)

    def test_IP(self):
        ip = '103.1.171.255'
        ip1 = IP.from_str(ip)
        self.assertEqual(ip1.value, 103001171255)
        ip2 = IP.from_value(ip1.value)
        self.assertEqual(ip1, ip2)

    def test_cache_citys(self):
        generate.cache_citys()





if __name__ == '__main__':
    unittest.main()