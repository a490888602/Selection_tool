# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:06:16 2018

@author: dell
"""
import pandas as pd
import os
# book = xlrd.open_workbook('activity_password1.xlsx')
# sheet = book.sheet_by_name('@activity_password')
os.chdir('C:/Users/htc/Desktop/行业数据整合18-9/')

list_1 = []
filelist = os.listdir()
for i in filelist:
    aa = pd.read_excel(i)
    if aa.size == 0:
        continue
    aa['cid'] = i.split('_')[3]
    scale = len(aa['类目'].str.split('>')[0])
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
    aa['行业日期'] = '2018-9'#唯二每次更新需要改动的地方，别忘了

    list_1.append(aa)
bigdata_ = pd.concat(list_1)
bigdata_.columns = ['itemName','itemUrl','itemBrand','storeName','storeCredit','itemPromotion','salesFaverite','salesReview','listPrice','salesPrice','salesQty','salesAmount','catIVID','catI','catII','catIII','catIV','dataPeriod']#'lastUpdate','primaryKey'

#去重
bigdata_.duplicated()
bigdata = bigdata_.drop_duplicates()
    
#操作数据库建表
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

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://wangquan:Wq5985790@rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com:3306/tbdata?charset=utf8")

bigdata.to_sql(name = 'hotitem',con = engine,if_exists = 'append',index = False,index_label = False)


