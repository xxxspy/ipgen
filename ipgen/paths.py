from pathlib import Path

HERE = Path(__file__).parent
PROJECT = HERE.parent
database = HERE / 'database.db'
regions_file = HERE / 'regions.json'
ip_db_file = HERE / 'qqwry_lastest.dat'
ip_db = PROJECT / 'ip' / 'IPTABLE.txt'
pro_point_info = PROJECT / 'ip' / 'pro_point.json'