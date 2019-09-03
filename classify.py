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
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.cluster.hierarchy as sch
import numpy as np

f = open('C:/Users/htc/Desktop/总和.txt')
a = f.read()
b = a.strip()
cids = re.findall('data-cid="(\d+)"', b)
names = re.findall('data-name="([^"].*)"', b)
dp = pd.DataFrame({'cid':cids,'pro':names})
pieces = dict(list(dp.groupby('cid')))
Check = list(set(cids))
industry = ['彩妆/香水/美妆工具','美容护肤/美体/精油','运动服/休闲服装','保健食品/膳食营养补充食品','奶粉/辅食/营养品/零食','运动鞋new']
'''
#需要添加海外国家
country = pd.read_excel('C:/Users/htc/Desktop/品牌数据.xlsx')[['品牌（英文）','所属国家']]
country = country.drop_duplicates()
country_index = dict(zip(country['品牌（英文）'],country['所属国家']))'''

'''urllib.parse.quote('adidas/阿迪达斯',safe='1')
urllib.parse.unquote('%E6%98%AF%E5%90%A6%E5%95%86%E5%9C%BA%E5%90%8C%E6%AC%BE')'''

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

#加载分词
jieba.load_userdict('C:/Users/htc/Desktop/jieba/新建文件夹/words_dict.txt')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#停词
stop = pd.read_table('C:/Users/htc/Desktop/jieba/words_stop.txt',encoding='gbk',header=None,
            names=['txt'])
stopwords = stop['txt'].values.tolist()
stopwords.extend(list(range(0,5000)))#把一个列表带入另一个
stopword = []#搜集停词
#ci = '50010815'
for ci in Check:
    brand = pieces[ci]['pro'].tolist()
    brand = list(set(brand))
    for bra in brand:
        bra = bra.replace('amp;','')
        bra = urllib.parse.quote(bra,safe='@')
        if bra[-1] == '.':
            bra = bra.replace('.','。')
        os.chdir('D:/线下行业数据库/%s/%s/' % (ci,bra))
        filelist = os.listdir()
        list_1 = []
        for i in filelist:
            aa = pd.read_excel(i)
            list_1.append(aa)
            #数据清洗
            if str(aa['catI'].tolist()[0]) not in industry:
                list_1 = []
                continue
        if list_1 == []:#防空文件夹,同时去掉错误文件
            continue
        
        bigdata_ = pd.concat(list_1)

        
        #去重，难免有些失误
        bigdata_.duplicated()
        df = bigdata_.drop_duplicates()
        df = df.reset_index(drop=True)
        df = df.loc[df['itemName'].dropna(axis=0).index]
        text = df['itemName'].str.lower()
        
        '''
        #需要添加海外国家
        abroad = str(df['itemBrand'].tolist()[0]).split('/')[0]
        if abroad in list(country_index):
            df.loc[:,'country'] = country_index[abroad]
        else:
            df.loc[:,'country'] = '中国' '''
            
        #分词
        sent_words = []
        for sent0 in text:
            sent0 = sent0.replace('0','')#可以替换多个
            sent0 = sent0.replace('1','')#不赋值就不会改变
            sent0 = sent0.replace('2','')
            sent0 = sent0.replace('3','')
            sent0 = sent0.replace('4','')
            sent0 = sent0.replace('5','')
            sent0 = sent0.replace('6','')
            sent0 = sent0.replace('7','')
            sent0 = sent0.replace('8','')
            sent0 = sent0.replace('9','')
            sent0 = sent_words.append(list(jieba.cut(sent0)))
        document = [" ".join(sent0) for sent0 in sent_words]
            
        #开始运算
        try:
            tfidf_model = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.03, max_df=0.8,stop_words=stopwords).fit(document)
        except:
            tfidf_model = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.03,stop_words=stopwords).fit(document)
        #去除掉迪拜岗这种，还有抱团800个在24个之下的抱团出现，跟地点格式有关系
        tfidf_model_ = tfidf_model.vocabulary_
        sparse_result = tfidf_model.transform(document)# 得到tf-idf矩阵，稀疏矩阵表示法
        juzhen = sparse_result.todense()# 转化为更直观的一般矩阵
        baobei = pd.DataFrame(juzhen,index=text)
            
        '''
        #加关键权重
        we = pd.read_table('C:/Users/htc/Desktop/jieba/words_weight.txt',encoding='gbk',header=None,
                           names=['txt'])
        weight = we['txt'].values.tolist()
        col = []
        for o in  weight:
            if o in tfidf_model_.keys():
                col.append(tfidf_model_[o])
        baobei[col] = baobei[col]*2
        #增加权重后留出来的，我们要留多少容纳与精确程度'''
            
        if len(baobei) == 1:
            df.loc[:,'group1'] = 1
            df.loc[:,'group2'] = ''
            continue
        # 层次聚类
        #生成点与点之间的距离矩阵,这里用的余弦相似距离:
        disMat = sch.distance.pdist(baobei,'cosine') 
        dismat = np.nan_to_num(disMat)
        #进行层次聚类:
        Z=sch.linkage(dismat,method='average')
            
        #根据linkage matrix Z得到聚类结果:
        #tb = input('参数：')
        labels_pred = sch.fcluster(Z, t=0.7, criterion='distance')#调参
            
        df.loc[:,'group1'] = labels_pred
            
            
        #分类关键词抽取
        group = list(range(1,df['group1'].max()+1))
        df.loc[:,'group2']=''
        df = df.sort_values('group1').reset_index(drop=True)#按道理不会配对不上啊
        
        for gro in group:
            text_ = df[df['group1'] == gro]['itemName'].str.lower()
            #分词
            sent_words_ = []
            for sent1 in text_:
                sent1 = sent1.replace('0','')#可以替换多个
                sent1 = sent1.replace('1','')
                sent1 = sent1.replace('2','')
                sent1 = sent1.replace('3','')
                sent1 = sent1.replace('4','')
                sent1 = sent1.replace('5','')
                sent1 = sent1.replace('6','')
                sent1 = sent1.replace('7','')
                sent1 = sent1.replace('8','')
                sent1 = sent1.replace('9','')
                sent_words_.append(list(jieba.cut(sent1)))
            document_ = [" ".join(sent1) for sent1 in sent_words_]
            try:
                tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.5,stop_words=stopwords).fit(document_)#这个0.5是否能支撑，假设检验？
            except:
                try:
                    tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.4,stop_words=stopwords).fit(document_)
                except:
                    try:
                        tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.3,stop_words=stopwords).fit(document_)
                    except:
                        try:
                            tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.2,stop_words=stopwords).fit(document_)
                        except:
                            try:
                                tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.1,stop_words=stopwords).fit(document_)
                            except:
                                try:
                                    tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.05,stop_words=stopwords).fit(document_)
                                except:
                                    tfidf_model_l = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", min_df=0.01,stop_words=stopwords).fit(document_)
            tfidf_model_l_ = tfidf_model_l.vocabulary_
            groupstr=''.join(list(tfidf_model_l_))
            df.loc[text_.index,'group2'] = groupstr
            stopword.append(groupstr)
        df = df.sort_values('group1')
          
        #上传数据
        from sqlalchemy import create_engine
        engine = create_engine("mysql+pymysql://wangquan:Wq5985790@rm-bp12z8rh0j5503p6p2o.mysql.rds.aliyuncs.com:3306/tbdata?charset=utf8")
        df.to_sql(name = 'group_byss',con = engine,if_exists = 'append',index = False,index_label = False)
            
#pd.Series(stopword).to_excel("C:/Users/htc/Desktop/停词.xlsx")
#conn.close()     
            #ss
            #sz