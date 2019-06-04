from ipgen import cache, regions, generate, paths, settings, check
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

    # def test_gen(self):
    #     ips = generate.gen(1000, '河北省')
    #     check.update_cached()
    #     self.assertEqual(len(ips), 1000)
    #     ips = generate.gen(1000)
    #     self.assertEqual(len(ips), 1000)
    #     ips = generate.gen(1000, region='河北省', city='石家庄', n_pre_region=50)
    #     self.assertEqual(1000, len(ips))
    #     check.update_cached()

    def test_split_ips(self):
        '''把ip按照省份切分'''
        files = {}
        dirpath = paths.PROJECT / 'ip'
        for pro in settings.PROS:
            if pro in files:
                f = files[pro]
            else:
                fpath = dirpath / pro
                f = open(str(fpath), 'w', encoding='utf8')
                files[pro] = f
        with open(str(paths.ip_db), 'r', encoding='utf8') as ipfile:
            for line in ipfile:
                info = line.split('\t')
                find = False
                for pro in settings.PROS:
                    if info[5].startswith(pro) and info[2]!=info[4] and info[2]:
                        find = True
                        break
                if find:
                    writer = files[pro]
                    writer.write('{}\t{}\t{}\n'.format(info[5], info[2], info[4]))
        for file in files.values():
            file.close()

    # def test_sample_between(self):
    #     ip = IP(1,2,1,1)
    #     end = IP(1,2,1,200)
    #     ips = ip.sample_between(end, 100)
    #     print(len(ips))
    #     ips = ip.sample_between(end, 1000)
    #     print(len(ips))
        # print(ips)


                



if __name__ == '__main__':
    unittest.main()