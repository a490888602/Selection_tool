# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 10:00:41 2018

@author: dell
"""

import pandas as pd
import numpy as np
from math import isnan

#回归系数
class parm:
    def __init__(self, df):
        self.name = df

    def corr(self):
        df = self.name
        dic_mouth = {'2017年09月':1,'2017年10月':2,'2017年11月':3,'2017年12月':4,'2018年01月':5,
         '2018年02月':6,'2018年03月':7,'2018年04月':8,'2018年05月':9,'2018年06月':10,
         '2018年07月':11,'2018年08月':12,'2018年09月':13,'2018年10月':14,'2018年11月':15,'2018年12月':16,'2019年01月':17,
         '2019年02月':18,'2019年03月':19,'2019年04月':20}
        df = df.replace(dic_mouth)
        #填补缺失值
        df['dataPeriod1'] = df['dataPeriod']-1
        df.set_index(['dataPeriod1'], inplace=True)
        in_num=0
        for in_dex in df.index.tolist():
            if len(dic_mouth)-df.index.tolist()[in_num]>18:
                df = df.drop([in_dex])
        if df['dataPeriod'].tolist()==[]:
            return [0,0,0,0,0,0,0,0,0,0,0,0,0]
        n = df['dataPeriod'].tolist()[0]
        df_season = pd.DataFrame(np.arange(n,len(dic_mouth)+1),columns = ['dataPeriod'],index =np.arange(n,len(dic_mouth)+1)-1)
        df = df.combine_first(df_season)
        df.fillna(0,inplace=True)
        salesQty = df['salesQty'].astype(int)
        d = len(salesQty)
        
        if len(salesQty) == 1:
            k1,k2,k3,t,divide1,divide2,std1,std2,std3,t1,t2,dive = (0,0,0,0,0,0,0,0,0,0,0,1)
        elif len(salesQty) == 2:
            k1,k2,t,divide1,divide2,std1,std2,std3,t1,t2,dive = (0,0,0,0,0,0,0,0,0,0,1)
            k3 = (salesQty.tolist()[-1]-salesQty.tolist()[0])/salesQty.tolist()[0]
        elif len(salesQty) == 3:
            k1 = (salesQty.tolist()[1]-salesQty.tolist()[0])/salesQty.tolist()[0]
            try:
                k2 = (salesQty.tolist()[2]-salesQty.tolist()[1])/salesQty.tolist()[1]
                k3 = (k1+k2)/2
            except:
                k2 = 0#0/0
                k3 = (k1+k2)/2
            std3 = (abs(k1-k3)+abs(k2-k3))/2
            t = pow(salesQty.tolist()[-1]/salesQty.tolist()[0],1/2) - 1
            t1 = k1 = 0
            t2 = k2 = 0
            std1,std2,divide1,divide2,dive = (0,0,0,0,1)
        else:
            dmean = (salesQty[:-1].reset_index(drop=True)+salesQty[1:].reset_index(drop=True))/2
            dx = salesQty[1:].reset_index(drop=True)-salesQty[:-1].reset_index(drop=True)
            inx1 = dx/dmean
            inx1 = inx1.fillna(0)#不能为1，算法不同,不然下降为0的那段拐点很大
            inx1 = inx1.replace(np.inf,0)
            inx2 = inx1[1:].reset_index(drop=True)-inx1[:-1].reset_index(drop=True)
            inx2 = inx2.abs()
            cut = inx2.idxmax()
            
            #拐点识别
            sales = salesQty.reset_index(drop=True)
            if abs(sales[cut]-sales[cut+1])>abs(sales[cut+1]-sales[cut+2]):
                divide1 = cut+1
                divide2 = len(salesQty)-cut-1
            else:
                divide1 = cut+2
                divide2 = len(salesQty)-cut-2
            while divide1 <4 or divide2 <4:
                dive = 2
                inx2 = inx2.drop(cut)
                if len(inx2) == 0:
                    dive = 1
                    divide1 = divide2 = 0
                    break
                cut = inx2.idxmax()
                sales = salesQty.reset_index(drop=True)
                if abs(sales[cut]-sales[cut+1])>abs(sales[cut+1]-sales[cut+2]):
                    divide1 = cut+1
                    divide2 = len(salesQty)-cut-1
                else:
                    divide1 = cut+2
                    divide2 = len(salesQty)-cut-2
            else:
                dive = 2
                    
            incra1 = salesQty[1:].reset_index(drop=True)/salesQty[:-1].reset_index(drop=True)
            incra1 = incra1.fillna(1)#0/0为空，不是inf，所以取1区别于真的0/x,神来之笔,da
            incra1 = incra1.replace(np.inf,0)-1#增长率，取0更合适而不是平均，要差值最大  
            
            if dive == 2:
                t = pow(sum(salesQty.tolist()[-3:])/sum(salesQty.tolist()[:3]),1/(len(salesQty)-3)) - 1
                t1 = pow(sum(salesQty.tolist()[divide1-2:divide1])/sum(salesQty.tolist()[:2]),1/(divide1-2)) - 1#2个月
                try:
                    t2 = pow(sum(salesQty.tolist()[-2:])/sum(salesQty.tolist()[divide1:divide1+2]),1/(divide2-2)) - 1
                except:
                    t2 = 0
                y1 = incra1[:divide1-1]
                y2 = incra1[divide1:]
                k1 = y1.mean()
                k2 = y2.mean()
                k3 = incra1.mean()
                std1 = np.array(y1).std()#如果双11的增幅超过任何时候，那只能认为有生命力
                std2 = np.array(y2).std()
                std3 = np.array(incra1).std()
                    
            if dive == 1:
                t = pow(sum(salesQty.tolist()[-3:])/sum(salesQty.tolist()[:3]),1/(len(salesQty)-3)) - 1
                t1 = 0
                t2 = 0
                k1 = 0
                k2 = 0
                k3 = incra1.mean()
                std3 = np.array(incra1).std()
                std1 = 0
                std2 = 0
        return [k1,k2,k3,std1,std2,std3,divide1,divide2,t,t1,t2,d,dive]
    #sku波动性
    def volatility(self):
        df = self.name
        dic_mouth = {'2017年09月':1,'2017年10月':2,'2017年11月':3,'2017年12月':4,'2018年01月':5,
         '2018年02月':6,'2018年03月':7,'2018年04月':8,'2018年05月':9,'2018年06月':10,
         '2018年07月':11,'2018年08月':12,'2018年09月':13,'2018年10月':14,'2018年11月':15,'2018年12月':16,'2019年01月':17,
         '2019年02月':18,'2019年03月':19,'2019年04月':20}
        df = df.replace(dic_mouth)
        
        #填补缺失值
        df['dataPeriod1'] = df['dataPeriod']-1
        df.set_index(['dataPeriod1'], inplace=True)
        in_num=0
        for in_dex in df.index.tolist():
            if len(dic_mouth)-df.index.tolist()[in_num]>18:
                df = df.drop([in_dex])
        if df['dataPeriod'].tolist()==[]:
            return 0
        n = df['dataPeriod'].tolist()[0]
        df_season = pd.DataFrame(np.arange(n,len(dic_mouth)+1),columns = ['dataPeriod'],index =np.arange(n,len(dic_mouth)+1)-1)
        df = df.combine_first(df_season)
        df.fillna(0,inplace=True)
        
        x = df['salesQty'][:-1].reset_index(drop=True).astype(int)
        y = df['salesQty'][1:].reset_index(drop=True).astype(int)
        k2 = y.corr(x)#x,y只有一个就会为空，从而为na
        if isnan(k2) :
            k2 = 0
        return k2
    
    def cv(self):
        df = self.name
        if len(df['salesQty']) == 1:
            CV = 0
        else:
            CV = df['salesQty'].astype(int).std()/df['salesQty'].astype(int).mean()#后一个不加为字符串会乱七八糟，很大
        return CV
    
    def salesQty(self):
        df = self.name
        dic_mouth = {'2017年09月':1,'2017年10月':2,'2017年11月':3,'2017年12月':4,'2018年01月':5,
         '2018年02月':6,'2018年03月':7,'2018年04月':8,'2018年05月':9,'2018年06月':10,
         '2018年07月':11,'2018年08月':12,'2018年09月':13,'2018年10月':14,'2018年11月':15,'2018年12月':16,'2019年01月':17,
         '2019年02月':18,'2019年03月':19,'2019年04月':20}
        df = df.replace(dic_mouth)
        #填补缺失值
        df['dataPeriod1'] = df['dataPeriod']-1
        df.set_index(['dataPeriod1'], inplace=True)
        in_num=0
        for in_dex in df.index.tolist():
            if len(dic_mouth)-df.index.tolist()[in_num]>18:
                df = df.drop([in_dex])
        df_season = pd.DataFrame(np.arange(len(dic_mouth)-17,len(dic_mouth)+1),columns = ['dataPeriod'])
        df_season['dataPeriod1'] = df_season['dataPeriod']-1
        df_season.set_index(['dataPeriod1'], inplace=True)
        df = df.combine_first(df_season)
        df.fillna(0,inplace=True)
        
        df = df['salesQty'].astype(int).tolist()
        return df
    
    def turn_out(self):
        return [self.cv(),self.volatility()]+self.corr()+self.salesQty()
