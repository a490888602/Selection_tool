# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:06:16 2018

@author: dell
"""
'''重要的是如何把新加进来的月份能够分类，比如给一个月的数据，根据cid自动划分到指定文件夹，
以后无非就是通过cid索引罢了，创建文件夹都简单，for循环就行了
简单的说，就是cid分类，因为哪怕合一起了，提取数据也是麻烦事，而反正我是品牌分类，只需要品牌集合
cid下品牌的聚合，分几步得，一个月一个月的放，然后品牌迭代更新
或者汇总了以后，根据相同cid和品牌聚合成list，再合成新的excel，名字就是cid+品牌便于索引
如何把新的文件也导入呢，是导入一个还是全部呢，导入一个吧，因为下面代码就是聚合的
那是按文件夹分品牌还是聚合品牌呢，聚合那样对新的不友好吧，不好索引，不如直接分组操作而不是迭代
大概如此，没有验证，只能抽象个大概，归类算法'''
import pandas as pd
import os
import re
import urllib
# book = xlrd.open_workbook('activity_password1.xlsx')
# sheet = book.sheet_by_name('@activity_password')

f = open('C:/Users/htc/Desktop/总和.txt')
a = f.read()
b = a.strip()
cids = re.findall('data-cid="(\d+)"', b)
names = re.findall('data-name="([^"].*)"', b)
dp = pd.DataFrame({'cid':cids,'pro':names})
pieces = dict(list(dp.groupby('cid')))
Check = list(set(cids))

urllib.parse.quote('adidas/阿迪达斯',safe='1')
urllib.parse.unquote('%E6%98%AF%E5%90%A6%E5%95%86%E5%9C%BA%E5%90%8C%E6%AC%BE')

'''
#新增
#新增商品
brand_ = pd.read_excel('C:/Users/htc/Desktop/result.xlsx').values.T.tolist()
url = brand_[1]
cvid = brand_[0]
ull = list(zip(url,cvid))
brand_append_1 = []
brand_append_2 = []
for i in ull:
    itembrand = urllib.parse.unquote(re.findall('name=(\S+)', i[0])[0])
    a = re.findall('data-cid="(\d+)"', i[1])
    b = re.findall('">(\D+)</li>', i[1])#因为没数字
    caid = list(zip(a,b))
    for o in caid:
        if re.findall('(\S+)', o[1])[0] in industry:
            if len(re.findall('(\S+)', o[1])) == 3:
                brand_append_1.append((itembrand,o[0]))
                brand_append_2.append(o[0])
                
dp = pd.DataFrame(brand_append_1,columns=['pro','cid'])
pieces = dict(list(dp.groupby('cid')))
Check = list(set(dp['cid'].tolist()))


#创建文件夹
for ci in Check:
    brand = pieces[ci]['pro'].tolist()
    brand = list(set(brand))#确实有重复
    for bra in brand:
        bra = bra.replace('amp;','')
        bra = urllib.parse.quote(bra,safe='@')
        if bra[-1] == '.':
            bra = bra.replace('.','。')
        #bra = bra.replace('amp;','')
        #bra = bra.replace("'",'’')#l'oreal /欧莱雅
        try:
            os.makedirs('D:/线下行业数据库/%s/%s' % (ci,bra))
        except:
            pass
        '''
        #有个小问题，当品牌里有/的时候就会成找不到指定的路径，那是字符串啊，可居然能识别出来,因为mum－mum /贝比玛玛后面加了空格所以不识别,确实有直接生成的，还有重复的牌子，有中文和没中文的
        #还有一个小问题，确实存在品牌的重复，虽然极少,其实也不一样，只是多了个点，但文件夹不行啊，会自动去掉点
        #真的有重复，而且都是二，不知道是因为搜集的问题还是正则的问题
'''from collections import Counter 
Counter(brand)#检查重复'''
        



'''os.chdir('D:/行业数据整合18-4/')#指定一个月的数据的文件夹
filelist = os.listdir()
aba = []
abb = []

for i in filelist:
    aa = pd.read_excel(i)
    ach = i.split('_')[5]
    if aa.size == 0:
        continue
    ip_brand = str(aa['品牌'][0])
    if ip_brand.isdigit():
        aba.append(ip_brand)
        abb.append(ach)
dd = pd.DataFrame({'shu':aba,'min':abb})'''
        
#归类
os.chdir('C:/Users/htc/Desktop/行业数据整合19-4/')#指定一个月的数据的文件夹
filelist = os.listdir()
'''
N = 0
for x in filelist:
    N += 1
    if x == '淘数据数据报表_热销宝贝排行_类目_125114017_品牌_nu－lax_乐康膏_ALL_2017年09月.xls':
        print(N)
NO = 0'''
for i in filelist:
    ''' 
    NO += 1
    if NO < 9387:
        pass
        '''
    aa = pd.read_excel(i)
    if aa.size == 0:
        continue
    aa['cid'] = i.split('_')[3]
    try:
        scale = len(aa['类目'].str.split('>')[0])#.str是直接操作dataframe，可以直接赋值，但数据由脏的
        cut = aa['类目'].str.split('>')
    except:
        scale = len(aa['类目'].str.split('>')[1])#.str是直接操作dataframe，可以直接赋值，但数据由脏的
        cut = aa['类目'].str.split('>')
    del aa['下一级类目']
    del aa['类目']
    if scale == 4:
        aa['一级类目'] = cut.str[0]
        aa['二级类目'] = cut.str[1]
        aa['三级类目'] = cut.str[2]
        aa['四级类目'] = cut.str[3]
    elif scale == 3:
        aa['一级类目'] = cut.str[0]
        aa['二级类目'] = cut.str[1]
        aa['三级类目'] = cut.str[2]
        aa['四级类目'] = cut.str[2]    
    elif scale == 2:
        aa['一级类目'] = cut.str[0]
        aa['二级类目'] = cut.str[1]
        aa['三级类目'] = cut.str[1]
        aa['四级类目'] = cut.str[1]
    aa['行业日期'] = i.split('_')[-1][0:8]#需要改动的地方，月份甚至星期，别忘了
    ip_cid = i.split('_')[3]
    ip_brand = str(aa['品牌'][0])
    if ip_brand.isdigit():#判断是否为纯数，因为编码会错误
        pass
    else:
        ip_brand = urllib.parse.quote(ip_brand,safe='@')
    if ip_brand[-1] == '.':
            ip_brand = ip_brand.replace('.','。')
    if ip_brand == '4' or ip_brand == '595' or ip_brand == '7' or ip_brand == '6590':
        ip_brand = ip_brand.replace('4','004')
        ip_brand = ip_brand.replace('595','0595')
        ip_brand = ip_brand.replace('7','007')
        ip_brand = ip_brand.replace('6590','06590')
    aa.columns = ['itemName','itemUrl','itemBrand','storeName','storeCredit','itemPromotion','salesFaverite','salesReview','listPrice','salesPrice','salesQty','salesAmount','catIVID','catI','catII','catIII','catIV','dataPeriod']#'lastUpdate','primaryKey'
    try:
        aa.to_excel("D:/线下行业数据库/%s/%s/%s" %(ip_cid,ip_brand,i))
    except:
        print(i)#我在八月曾今手动加过几个文件，应该有问题的&
    #是否文件夹里的品牌与我们提取的一样，但文件名里肯定不同因为不支持特殊字，验证下,有个004和4
#多运行一次应该不会有问题，一是设置了去重，二是应该会覆盖相同的名字因为不是下载
'''
#读取，所有或部分，我们需要获取cid和品牌，在它们底下操作,也可以指定
for ci in Check:
    brand = pieces[ci]['pro'].tolist()
    brand = list(set(brand))
    for bra in brand:
        bra = urllib.parse.quote(bra,safe='@')
        if bra[-1] == '.':
            bra = bra.replace('.','。')
        os.chdir('D:/线下行业数据库/%s/%s/' % (ci,bra))
        filelist = os.listdir()
        list_1 = []
        for i in filelist:
            aa = pd.read_excel(i)
            list_1.append(aa)
            bigdata_ = pd.concat(list_1)
            
            #去重，难免有些失误
            bigdata_.duplicated()
            bigdata = bigdata_.drop_duplicates()
            
            
            from sqlalchemy import create_engine
            engine = create_engine("mysql+pymysql://wangquan:Wq5985790@rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com:3306/tbdata?charset=utf8")
            bigdata.to_sql(name = 'hotitem',con = engine,if_exists = 'append',index = False,index_label = False)
            '''
    
#操作数据库
'''
import pymysql
conn = pymysql.connect(host="rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com", 
                             user="wangquan",
                             passwd="Wq5985790",
                             db='tbdata',
                             port=3306,
                             charset='utf8')
cur = conn.cursor()
cur.execute("truncate table hotitem")
conn.commit()'''
#sql = "insert into testtable ('宝贝名称', '宝贝链接', '品牌', '类目'，'下一级类目','掌柜','信用','营销推广','收藏量','累计评价','标价'，'成交价','销售量','销售金额') values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#cur.execute(sql)
# write
#cur.execute("drop table testwang_1")
#cur.execute('create table testwang_1(宝贝名称 varchar(100), 宝贝链接 varchar(80), 品牌 varchar(50), 掌柜 varchar(50), 信用 varchar(20), 营销推广 varchar(20), 收藏量 decimal, 累计评价 decimal, 标价 decimal(20,2) ,成交价 decimal(20,2) , 销售量 decimal, 销售金额 decimal(20,2), cid decimal,一级类目 varchar(50),二级类目 varchar(50),三级类目 varchar(50),四级类目 varchar(50),行业日期 varchar(20),上传时间 TIMESTAMP,主键 INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT)' )