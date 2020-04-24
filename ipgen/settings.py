from functools import lru_cache


PROS = [
    '黑龙江省',
    '北京市',
    '河北省',
    '内蒙古',
    '贵州省',
    '四川省',
    '河南省',
    '江西省',
    '山西省',
    '陕西省',
    '广东省',
    '广西省',
    '辽宁省',
    '上海市',
    '湖北省',
    '云南省',
    '浙江省',
    '江苏省',
    '安徽省',
    '福建省',
    '吉林省',
    '湖北省',
    '山东省',
    '天津市',
    '新疆',
    '湖南省',
    '甘肃省',
    '重庆市',
    '海南省',
    '香港',
    '美国',
]






CITY_CLASS = {
    '一线城市': ['北京', '上海', '广东-广州', '广东-深圳'], # 一线城市
    '新一线城市': [
                '成都',
                '杭州',
                '武汉',
                '重庆',
                '南京',
                '天津',
                '苏州',
                '西安',
                '长沙',
                '沈阳',
                '青岛',
                '郑州',
                '大连',
                '东莞',
                '宁波',
    ],
    '二线城市': [
            '厦门',
            '福州',
            '无锡',
            '合肥',
            '昆明',
            '哈尔滨',
            '济南',
            '佛山',
            '长春',
            '温州',
            '石家庄',
            '南宁',
            '常州',
            '泉州',
            '南昌',
            '贵阳',
            '太原',
            '烟台',
            '嘉兴',
            '南通',
            '金华',
            '珠海',
            '惠州',
            '徐州',
            '海口',
            '乌鲁木齐',
            '绍兴',
            '中山',
            '台州',
            '兰州',
    ],
    '三线城市': [
            '芜湖',
            '阜阳',
            '滁州',
            '蚌埠',
            '马鞍山',
            '安庆',
            '漳州',
            '莆田',
            '宁德',
            '龙岩',
            '三明',
            '南平',
            '汕头',
            '揭阳',
            '江门',
            '湛江',
            '肇庆',
            '清远',
            '潮州',
            '梅州',
            '桂林',
            '柳州',
            '遵义',
            '保定',
            '唐山',
            '廊坊',
            '邯郸',
            '沧州',
            '秦皇岛',
            '宜昌',
            '襄阳',
            '荆州',
            '大庆',
            '三亚',
            '洛阳',
            '南阳',
            '信阳',
            '商丘',
            '新乡',
            '衡阳',
            '株洲',
            '岳阳',
            '湘潭',
            '郴州',
            '吉林',
            '盐城',
            '镇江',
            '泰州',
            '淮安',
            '连云港',
            '宿迁',
            '赣州',
            '上饶',
            '九江',
            '鞍山',
            '呼和浩特',
            '包头',
            '银川',
            '绵阳',
            '潍坊',
            '临沂',
            '济宁',
            '淄博',
            '威海',
            '泰安',
            '咸阳',
            '乌鲁木齐',
            '湖州',
            '舟山',
            '丽水',
    ],
    '四线城市': [],
    '省会城市': [ # 省会城市
        '石家庄',
        '沈阳',
        '哈尔滨',
        '杭州',
        '福州',
        '济南',
        '广州',
        '武汉',
        '成都',
        '昆明',
        '兰州',
        '太原',
        '长春',
        '南京',
        '合肥',
        '南昌',
        '郑州',
        '长沙',
        '海口',
        '贵阳',
        '西安',
        '西宁',

    ], # 省会城市
}

@lru_cache()
def city_class_with_proname():
    from agent.base_info.wjx_city import all_cities
    cc = {}
    wjx_cities = all_cities()
    c4 = []
    for klass in CITY_CLASS:
        citis = CITY_CLASS[klass]
        if klass in ('一线城市', ):
            cc[klass] = citis[:]
            continue
        elif klass == '四线城市':
            cc[klass] = c4
            continue
        cc[klass] = []
        for ct in citis:
            for pro in wjx_cities:
                new_name = '{}-{}'.format(pro, ct)
                if ct in wjx_cities[pro]:
                    cc[klass].append(new_name)

    for pro in wjx_cities:
        for wc in wjx_cities[pro]:
            found = False
            name = '{}-{}'.format(pro, wc)
            for klass in ['一线城市', '二线城市', '三线城市', '新一线城市', '省会城市']:
                if name in cc[klass] or pro in cc[klass]:
                    found = True
                    break
            if not found:
                c4.append(name)
        
    return cc




    

BLACK_IPS = ['39.107.0', ]


if __name__ == '__main__':
    cc = city_class_with_proname()
    for k in cc:
        print(k, len(cc[k]), cc[k])