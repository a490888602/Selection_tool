# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:42:26 2019

@author: dell
"""

import numpy as np
import pandas as pd
def logo(df):
    df = pd.DataFrame(np.array(df).reshape(1,len(df)),columns = ['cv','volatility','k1','k2','k3','std1','std2','std3','divide1','divide2','t','t1','t2','d','dive','18month','17month','16month','15month','14month','13month','12month','11month','10month','9month','8month','7month','6month','5month','4month','3month','2month','1month']).replace("'",'’')    
    dic = df.T.to_dict()[0]
    if dic['d']<=3:
        a = '新品'
        b = "{:.2%}".format(dic['k3'])#变化率
        c = str(dic['d'])+'个月'#周期长
        d = '新品'#描述
        e = ''#状态
        f = '新品'#周期变化
        g = '变动'#稳定否
    else:
        if dic['cv'] < 0.25:
            if dic['t']>=0.1:
                g = '变动'
                e = '上升'
                a = '稳定的'
                b = "{:.2%}".format(dic['t'])
                c = str(dic['d'])+'个月'
            elif dic['t']<=-0.1:
                g = '变动'
                e = '下降'
                a = '稳定的'
                b = "{:.2%}".format(dic['t'])
                c = str(dic['d'])+'个月'
            else:
                g = '稳定'
                if dic['t']>0:
                    e = '上升'
                    a = '稳定的'
                    b = "{:.2%}".format(dic['t'])
                    c = str(dic['d'])+'个月'
                else:
                    e = '下降'
                    a = '稳定的'
                    b = "{:.2%}".format(dic['t'])
                    c = str(dic['d'])+'个月'
            d = c+a+e+b
            f = a+e
        else:
            if dic['volatility']>=0.8:
                if dic['t']>=0.1:
                    g = '变动'
                    e = '上升'
                    a = '稳定的'
                    b = "{:.2%}".format(dic['t'])
                    c = str(dic['d'])+'个月'
                elif dic['t']<=-0.1:
                    g = '变动'
                    e = '下降'
                    a = '稳定的'
                    b = "{:.2%}".format(dic['t'])
                    c = str(dic['d'])+'个月'
                else:
                    g = '稳定'
                    if dic['t']>0:
                        e = '上升'
                        a = '稳定的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    else:
                        e = '下降'
                        a = '稳定的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                d = c+a+e+b
                f = a+e
            else:
                if abs(dic['t'])<0.1:
                    g = '稳定'
                    if dic['t']>0:
                        e = '上升'
                        if abs(1.5*dic['k3'])>=dic['std3']:
                            a = '稳定的'
                            b = "{:.2%}".format(dic['t'])
                            c = str(dic['d'])+'个月'
                        elif abs(2.5*dic['k3'])>=dic['std3']>abs(1.5*dic['k3']):
                            a = '波动的'
                            b = "{:.2%}".format(dic['t'])
                            c = str(dic['d'])+'个月'
                        else:
                            a = '不稳的'
                            b = "{:.2%}".format(dic['t'])
                            c = str(dic['d'])+'个月'
                    else:
                        e = '下降'
                        if abs(1.5*dic['k3'])>=dic['std3']:
                            a = '稳定的'
                            b = "{:.2%}".format(dic['t'])
                            c = str(dic['d'])+'个月'
                        elif abs(2.5*dic['k3'])>=dic['std3']>abs(1.5*dic['k3']):
                            a = '波动的'
                            b = "{:.2%}".format(dic['t'])
                            c = str(dic['d'])+'个月'
                        else:
                            a = '不稳的'
                            b = "{:.2%}".format(dic['t'])
                            c = str(dic['d'])+'个月'
                    d = c+a+e+b
                    f = a+e
                elif dic['t']>=0.1:
                    g = '变动'
                    e = '上升'
                    if abs(1.5*dic['k3'])>=dic['std3']:
                        a = '稳定的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    elif abs(2.5*dic['k3'])>=dic['std3']>abs(1.5*dic['k3']):
                        a = '波动的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    else:
                        a = '不稳的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    d = c+a+e+b
                    f = a+e
                else:
                    g = '变动'
                    e = '下降'
                    if abs(1.5*dic['k3'])>=dic['std3']:
                        a = '稳定的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    elif abs(2.5*dic['k3'])>=dic['std3']>abs(1.5*dic['k3']):
                        a = '波动的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    else:
                        a = '不稳的'
                        b = "{:.2%}".format(dic['t'])
                        c = str(dic['d'])+'个月'
                    d = c+a+e+b
                    f = a+e
                if dic['dive']==2:
                    if abs(dic['t1'])<0.1:
                        if dic['t1']>0:
                            e1 = '上升'
                            if abs(1.5*dic['k1'])>=dic['std1']:
                                a1 = '稳定的'
                                b1 = "{:.2%}".format(dic['t1'])
                                c1 = str(dic['divide1'])+'个月'
                            elif abs(2.5*dic['k1'])>=dic['std1']>abs(1.5*dic['k1']):
                                a1 = '波动的'
                                b1 = "{:.2%}".format(dic['t1'])
                                c1 = str(dic['divide1'])+'个月'
                            else:
                                a1 = '不稳的'
                                b1 = "{:.2%}".format(dic['t1'])
                                c1 = str(dic['divide1'])+'个月'
                        else:
                            e1 = '下降'
                            if abs(1.5*dic['k1'])>=dic['std1']:
                                a1 = '稳定的'
                                b1 = "{:.2%}".format(dic['t1'])
                                c1 = str(dic['divide1'])+'个月'
                            elif abs(2.5*dic['k1'])>=dic['std1']>abs(1.5*dic['k1']):
                                a1 = '波动的'
                                b1 = "{:.2%}".format(dic['t1'])
                                c1 = str(dic['divide1'])+'个月'
                            else:
                                a1 = '不稳的'
                                b1 = "{:.2%}".format(dic['t1'])
                                c1 = str(dic['divide1'])+'个月'
                        d1 = c1+a1+e1+b1
                        f1 = a1+e1
                    elif dic['t1']>=0.1:
                        e1 = '上升'
                        if abs(1.5*dic['k1'])>=dic['std1']:
                            a1 = '稳定的'
                            b1 = "{:.2%}".format(dic['t1'])
                            c1 = str(dic['divide1'])+'个月'
                        elif abs(2.5*dic['k1'])>=dic['std1']>abs(1.5*dic['k1']):
                            a1 = '波动的'
                            b1 = "{:.2%}".format(dic['t1'])
                            c1 = str(dic['divide1'])+'个月'
                        else:
                            a1 = '不稳的'
                            b1 = "{:.2%}".format(dic['t1'])
                            c1 = str(dic['divide1'])+'个月'
                        d1 = c1+a1+e1+b1
                        f1 = a1+e1
                    else:
                        e1 = '下降'
                        if abs(1.5*dic['k1'])>=dic['std1']:
                            a1 = '稳定的'
                            b1 = "{:.2%}".format(dic['t1'])
                            c1 = str(dic['divide1'])+'个月'
                        elif abs(2.5*dic['k1'])>=dic['std1']>abs(1.5*dic['k1']):
                            a1 = '波动的'
                            b1 = "{:.2%}".format(dic['t1'])
                            c1 = str(dic['divide1'])+'个月'
                        else:
                            a1 = '不稳的'
                            b1 = "{:.2%}".format(dic['t1'])
                            c1 = str(dic['divide1'])+'个月'
                        d1 = c1+a1+e1+b1
                        f1 = a1+e1
                    if abs(dic['t2'])<0.1:
                        if dic['t2']>0:
                            e2 = '上升'
                            if abs(1.5*dic['k2'])>=dic['std2']:
                                a2 = '稳定的'
                                b2 = "{:.2%}".format(dic['t2'])
                                c2 = str(dic['divide2'])+'个月'
                            elif abs(2.5*dic['k2'])>=dic['std2']>abs(1.5*dic['k2']):
                                a2 = '波动的'
                                b2 = "{:.2%}".format(dic['t2'])
                                c2 = str(dic['divide2'])+'个月'
                            else:
                                a2 = '不稳的'
                                b2 = "{:.2%}".format(dic['t2'])
                                c2 = str(dic['divide2'])+'个月'
                        else:
                            e2 = '下降'
                            if abs(1.5*dic['k2'])>=dic['std2']:
                                a2 = '稳定的'
                                b2 = "{:.2%}".format(dic['t2'])
                                c2 = str(dic['divide2'])+'个月'
                            elif abs(2.5*dic['k2'])>=dic['std2']>abs(1.5*dic['k2']):
                                a2 = '波动的'
                                b2 = "{:.2%}".format(dic['t2'])
                                c2 = str(dic['divide2'])+'个月'
                            else:
                                a2 = '不稳的'
                                b2 = "{:.2%}".format(dic['t2'])
                                c2 = str(dic['divide2'])+'个月'
                        d2 = c2+a2+e2+b2
                        f2 = a2+e2
                    elif dic['t2']>=0.1:
                        e2 = '上升'
                        if abs(1.5*dic['k2'])>=dic['std2']:
                            a2 = '稳定的'
                            b2 = "{:.2%}".format(dic['t2'])
                            c2 = str(dic['divide2'])+'个月'
                        elif abs(2.5*dic['k2'])>=dic['std2']>abs(1.5*dic['k2']):
                            a2 = '波动的'
                            b2 = "{:.2%}".format(dic['t2'])
                            c2 = str(dic['divide2'])+'个月'
                        else:
                            a2 = '不稳的'
                            b2 = "{:.2%}".format(dic['t2'])
                            c2 = str(dic['divide2'])+'个月'
                        d2 = c2+a2+e2+b2
                        f2 = a2+e2
                    else:
                        e2 = '下降'
                        if abs(1.5*dic['k2'])>=dic['std2']:
                            a2 = '稳定的'
                            b2 = "{:.2%}".format(dic['t2'])
                            c2 = str(dic['divide2'])+'个月'
                        elif abs(2.5*dic['k2'])>=dic['std2']>abs(1.5*dic['k2']):
                            a2 = '波动的'
                            b2 = "{:.2%}".format(dic['t2'])
                            c2 = str(dic['divide2'])+'个月'
                        else:
                            a2 = '不稳的'
                            b2 = "{:.2%}".format(dic['t2'])
                            c2 = str(dic['divide2'])+'个月'
                        d2 = c2+a2+e2+b2
                        f2 = a2+e2
                    d = d1+d2
                    f = f1+'-'+f2
                    if f1 == f2:
                        f = f1
    return [a,b,c,d,e,f,g]
