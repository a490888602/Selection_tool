# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 20:01:57 2018

@author: dell
"""
import pandas as pd
import os
import re
import urllib
import pymysql
import numpy as np


f = open('C:/Users/htc/Desktop/总和.txt')
a = f.read()
b = a.strip()
cids = re.findall('data-cid="(\d+)"', b)
names = re.findall('data-name="([^"].*)"', b)
dp = pd.DataFrame({'cid':cids,'pro':names})
#pieces = dict(list(dp.groupby('cid')))
Check = list(set(cids))
industry = ['彩妆/香水/美妆工具','美容护肤/美体/精油','运动服/休闲服装','保健食品/膳食营养补充食品','奶粉/辅食/营养品/零食','运动鞋new']

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
Check = list(set(Check+brand_append_2))
dp1 = pd.DataFrame(brand_append_1,columns=['pro','cid'])
dp1 = dp1[['cid','pro']]
dp = pd.concat([dp,dp1],axis =0).reset_index()
pieces = dict(list(dp.groupby('cid')))

brand_out = pd.read_excel('C:/Users/htc/Desktop/country.xlsx')[0].tolist()
'''
#连接数据库
conn = pymysql.connect(host="rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com", 
                             user="wangquan",
                             passwd="Wq5985790",
                             db='tbdata',
                             port=3306,
                             charset='utf8')
cur = conn.cursor()
conn.commit()
cur.execute('create table group_byss(itemName varchar(100), itemUrl varchar(80), itemBrand varchar(50), storeName varchar(50), storeCredit varchar(20), itemPromotion varchar(30), salesFaverite decimal, salesReview decimal, listPrice decimal(20,2) ,salesPrice decimal(20,2) , salesQty decimal, salesAmount decimal(20,2), catIVID decimal,catI varchar(50),catII varchar(50),catIII varchar(50),catIV varchar(50),dataPeriod varchar(20),主键 INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, group1 decimal, group2 varchar(80))' )
cur.execute('create table groups(itemName varchar(100), itemUrl varchar(80), itemBrand varchar(50), catIV varchar(50), primaryKey decimal, group1 decimal)' )#group是有特殊意义的就像'一样识别不了
#创造
cur.execute("truncate table group_byss")
cur.execute("drop table group_bys")
#清楚'''

#ci = '50010815'
h = 0
j = 0
for ci in Check:
    h += 1
    #if h <= 82:
    #    continue
    brand = pieces[ci]['pro'].tolist()
    brand = list(set(brand))
    for bra in brand:
        if bra not in brand_out:
            continue
        j += 1
        #if j < 4892:
        #    continue
        bra = bra.replace('amp;','')
        #统一品牌名称
        bra_down=bra.replace("'",'’')
        bra = urllib.parse.quote(bra,safe='@')
        if bra[-1] == '.':
            bra = bra.replace('.','。')
        os.chdir('D:/线下行业数据库/%s/%s/' % (ci,bra))
        filelist = os.listdir()
        list_1 = []
        for i in filelist:
            aa = pd.read_excel(i)
            aa['itemBrand'] = bra_down
            aa['group1'] = aa['itemUrl'].str.split('=').str[1]
            aa['group2'] = ''
            list_1.append(aa)
            #数据清洗
            if str(aa['catI'].tolist()[0]) not in industry:
                list_1 = []
                continue
        if list_1 == []:#防空文件夹,同时去掉错误文件
            continue
        
        bigdata_ = pd.concat(list_1)
        bigdata_ = bigdata_.reset_index(drop=True)
        bigdata_.loc[bigdata_[bigdata_['dataPeriod']=='2019年04月'].index.tolist(),'group2'] = bigdata_.loc[bigdata_[bigdata_['dataPeriod']=='2019年04月'].index]['group1']
        
        #去重，难免有些失误
        bigdata_.duplicated()
        df = bigdata_.drop_duplicates()
        df = df.reset_index(drop=True)
        df = df.loc[df['itemName'].dropna(axis=0).index]
        
        df = df.sort_values('group1')
          
        #上传数据
        from sqlalchemy import create_engine
        engine = create_engine("mysql+pymysql://wangquan:Wq5985790@rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com:3306/tbdata?charset=utf8")
        df.to_sql(name = 'group_byss',con = engine,if_exists = 'append',index = False,index_label = False)
            
#df.to_excel("C:/Users/htc/Desktop/shiyan1.xlsx")
#conn.close()     
            #ss
            #sz