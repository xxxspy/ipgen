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
    #     generate.expand_city('沧州')

    def test_expand_range(self):
        generate.expand_ip_range('1.184.128.0', '1.184.255.255')
        generate.expand_ip_range('14.18.9.0', '14.18.63.255')
        generate.expand_ip_range('14.23.0.0', '14.23.255.255')

    # def test_city_ips(self):
    #     citi = '石家庄'
    #     r = generate.random_city_ips(citi, 10)
    #     print(r)





if __name__ == '__main__':
    unittest.main()