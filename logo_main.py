# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 14:22:28 2018

@author: dell
"""

import sys
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
sys.path.append('C:/Users/htc/Desktop/打标/')
from parm import parm
from logo import logo

#连接数据库
conn = pymysql.connect(host="rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com", 
                             user="wangquan",
                             passwd="Wq5985790",
                             db='tbdata',
                             port=3306,
                             charset='utf8')
cur = conn.cursor()
conn.commit()
#cur.execute('create table signss(catIV varchar(50),itemBrand varchar(50),group2 varchar(50),sign varchar(50),num varchar(50),months varchar(50),describes varchar(100),form varchar(20),changes varchar(20),steady varchar(20),total varchar(20),isbrand varchar(20),sqt_live decimal(20),itemName varchar(100))')
#cur.execute("truncate table signss")
#cur.execute("drop table signss")
engine = create_engine("mysql+pymysql://wangquan:Wq5985790@rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com:3306/tbdata?charset=utf8")

'''
#提取所有品类和品牌
def class_brand():
    sql = 'select distinct catIV,itemBrand from group_by'
    cur.execute(sql)
    results = cur.fetchall()
    df_ci = pd.DataFrame(np.array(results),columns=['catIV','itemBrand']).dropna(axis=0, how='any')
    df_ci = np.array(df_ci).tolist()
    return df_ci
    '''
#提取对应品牌和品类数据
def sql_conn(s,brand):
    sql_brand = 'select sum(salesQty),salesFaverite,group1,group2,dataPeriod,itemName from group_by where catIV="%s" and itemBrand = "%s" GROUP BY group1,dataPeriod' % (s,brand)
    cur.execute(sql_brand)
    results_brand = cur.fetchall()
    result_brand = []
    for i in results_brand:
        result_brand.append((int(i[0]),int(i[1]),i[2],i[3],i[4],i[5]))
    list_brand = np.array(result_brand)
    df_brand = pd.DataFrame(list_brand,columns=['salesQty','salesFaverite','group1','group2','dataPeriod','itemName'])
    return df_brand

def corr(df):
    if __name__=="__main__":
        a=parm(df)
        b = a.turn_out()
        c = logo(b)
        if len(c[1].split('.')[0]) == 1:#方便字符串排序
            c[1] = '00'+c[1]
        if len(c[1].split('.')[0]) == 2 and c[1].split('.')[0][0]!='-':
            c[1] = '0'+c[1]
        if len(c[1].split('.')[0]) == 2 and c[1].split('.')[0][0] =='-':
            c[1] = '-00'+c[1][1:]
        if len(c[1].split('.')[0]) == 3 and c[1].split('.')[0][0] =='-':
            c[1] = '-0'+c[1][1:]
        c.append(c[0]+c[4])
    return c


def show(df_brand):
    #品牌
    sku_para = []
    df = df_brand[['salesQty','salesFaverite','group1','group2','dataPeriod']].copy()
    df['salesQty'] = df['salesQty'].astype(int)
    df['salesFaverite'] = df['salesFaverite'].astype(int)
    df = df.groupby(df_brand['dataPeriod']).sum()
    df.reset_index('dataPeriod',inplace =True)
    sku_name = brand
    list_df = [s,brand,sku_name]+corr(df)+['是']+[df['salesQty'].loc[len(df)-1]]+[brand]#区分品牌
    if ('2019年03月' in df['dataPeriod'].tolist()) & ('2019年04月' in df['dataPeriod'].tolist()):#前一个月存在，一个月增长
        list_df[8]=df['salesQty'].astype(int).iloc[-1]/df['salesQty'].astype(int).iloc[-2]-1
    else:
        list_df[8]=0
    if ('2019年02月' in df['dataPeriod'].tolist()) & ('2019年04月' in df['dataPeriod'].tolist()):#前二个月存在，3个月增长
        list_df.append(df['salesQty'].astype(int).iloc[-1]/df['salesQty'].astype(int)[df['dataPeriod']=='2019年02月'].tolist()[0]-1)
    else:
        list_df.append(0)
    sku_para.append(list_df)
    #sku
    for i in df_brand.groupby('group1'):
        df = i[1]
        sku_name = i[0]
        if len(df)==((df['group2']=='').sum()):
            continue
        df_name = df['itemName'].tolist()[0]
        df = df[['salesQty','group1','dataPeriod']]
        df.columns=['salesQty','group2','dataPeriod']
        df = df.reset_index(drop=True)
        list_df = [s,brand,sku_name]+corr(df)+['否']+[int(df['salesQty'].loc[len(df)-1])]+[df_name]
        if ('2019年03月' in df['dataPeriod'].tolist()) & ('2019年04月' in df['dataPeriod'].tolist()):
            list_df[8]=df['salesQty'].astype(int).iloc[-1]/df['salesQty'].astype(int).iloc[-2]-1
        else:
            list_df[8]=0
        if ('2019年02月' in df['dataPeriod'].tolist()) & ('2019年04月' in df['dataPeriod'].tolist()):#前二个月存在，3个月增长
            list_df.append(df['salesQty'].astype(int).iloc[-1]/df['salesQty'].astype(int)[df['dataPeriod']=='2019年02月'].tolist()[0]-1)
        else:
            list_df.append(0)
        sku_para.append(list_df)
    return sku_para

'''
sql = 'select distinct catIV,itemBrand from group_by where catIV="BB霜"'
cur.execute(sql)
results = cur.fetchall()
df_ci = pd.DataFrame(np.array(results),columns=['catIV','itemBrand']).dropna(axis=0, how='any')
df_ci = np.array(df_ci).tolist()
i = df_ci[0]
'''


def class_brand():
    sql = 'select distinct catIV,itemBrand from group_by'
    cur.execute(sql)
    results = cur.fetchall()
    df_ci = pd.DataFrame(np.array(results),columns=['catIV','itemBrand']).dropna(axis=0, how='any')
    df_ci = np.array(df_ci).tolist()
    return df_ci
    
#提取对应品牌和品类数据

df_ci = class_brand()
for i in df_ci:
    s,brand = i[0],i[1]
    df_brand = sql_conn(s,brand)
    a = show(df_brand)
    data = pd.DataFrame(a,columns = ['catIV','itemBrand','group2','sign','num','months','describes','form','changes','steady','total','isbrand','sqt_live','itemName','increase_3']).replace("'",'’')    
    data.to_sql(name = 'signss',con = engine,if_exists = 'append',index = False,index_label = False)



