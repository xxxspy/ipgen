from ipgen import cache, regions, generate, paths
import unittest
from ipgen.models import IP


# cache.create()
# cache.get('dfdlkjdlfj')

# r = regions.get_ranges('河北')
# print(r[0][0].fetch_info())


class Test(unittest.TestCase):

    # def test_get_regions(self):
    #     rgs = regions.get_regions()
    #     self.assertEqual(len(rgs), 32)

    # def test_IP(self):
    #     ip = '103.1.171.255'
    #     ip1 = IP.from_str(ip)
    #     self.assertEqual(ip1.value, 103001171255)
    #     ip2 = IP.from_value(ip1.value)
    #     self.assertEqual(ip1, ip2)

    # def test_cache_citys(self):
    #     generate.cache_citys()

    # def test_expand_province(self):
    #     generate.expand_province('河北')

    # def test_select_ip(self):
    #     r=cache.select(regionName='河北')
    #     print(r)

    # def test_expand_city(self):
    #     generate.expand_city('南京')

    # def test_expand_range(self):
    #     for i in range(50):
    #         generate.expand_ip_range('219.216.176.0', '219.216.176.255')
        # generate.expand_ip_range('124.228.0,0', '124.228.255.255')
        # generate.expand_ip_range('113.220.0.0', '113.223.255.255')
        # generate.expand_ip_range('27.42.97.0', '27.42.127.255')
        # generate.expand_ip_range('49.239.192.0', '49.239.255.255')

    # def test_fetch_range(self):
    #     ips = generate.fetch_range(100, 'guangdong', 'zhuhai')
    #     print(ips)
    #     ips = generate.rand_fetch(100, 'guangdong', 'zhuhai')
    #     print(ips)

    # def test_city_ips(self):
    #     citi = '石家庄'
    #     r = generate.random_city_ips(citi, 10)
    #     print(r)

    def test_gen(self):
        ips = generate.gen(100, '河北省')
        self.assertEqual(len(ips), 100)
        ips = generate.gen(1000)
        self.assertEqual(len(ips), 1000)
        ips = generate.gen(1000, region='河北省', city='石家庄', n_pre_region=50)
        self.assertEqual(1000, len(ips))



if __name__ == '__main__':
    unittest.main()