# -*- coding: utf-8 -*-
import re
import time
f = open('C:/Users/dell/Desktop/总和.txt')
a = f.read()

b = a.strip()

cids = re.findall('data-cid="(\d+)"', b)
names = re.findall('data-name="([^"].*)"', b)
print(len(cids))
print(len(names))
mapping = list(zip(names, cids))
print(len(mapping))

Check = set(cids)
print(len(Check))

import webbrowser
import urllib
urllib.parse.quote('adidas/阿迪达斯',safe='1')
urllib.parse.unquote('%E6%98%AF%E5%90%A6%E5%95%86%E5%9C%BA%E5%90%8C%E6%AC%BE')

url_1 = r'http://www.taosj.com/data/industry/hotitems/list/export?api_name=data_industry_hotitems_list_export&cid='
url_2 = r'&date='
url_3 = r'&brand='
url_4 = r'&type=ALL'
o =-10135
for i in mapping:
    o = o+1
    if 0 < o <= 5000:
        brand = i[0].replace('amp;','')
        brand_1 = urllib.parse.quote(brand,safe='1')
        brand_2 = i[1]
        url = url_1+brand_2+url_2+'1533052800000'+url_3+brand_1+url_4
        webbrowser.open(url)
        time.sleep(8)
    if o > 5000:
        break
    



