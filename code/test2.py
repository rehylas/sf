#!/usr/bin/python
# -*- coding: UTF-8 -*

import tushare as ts
import numpy  as np 
import pandas as pd 
import time
import datetime
import pymongo
import urllib2
from pymongo import MongoClient

def loadStocklist2file():
    stocklist = ts.get_stock_basics()
    stocklist.to_csv("stocklist.csv")
    return stocklist
    pass

def saveStocklist2db():
    client = MongoClient('localhost',27017)
    stock_info = client.market.stock_info
    data = pd.read_csv( "stocklist.csv" )
    #print data[0:2]
    
    for index, row in data.iterrows():
        #print  row.to_dict()
        rec = row.to_dict()
    
        try:
                 
            rs = stock_info.insert_one( rec )
        except Exception , e:
            pass            
        pass        
        
         
    pass    

def saveFuturelist2db():
    client = MongoClient('localhost',27017)
    f_info = client.market.f_info
    data = pd.read_csv( "futurelist.csv" )
    #print data[0:2]
    
    for index, row in data.iterrows():
        #print  row.to_dict()
        rec = row.to_dict()
        #print rec
        rec = {"code":row['code'],"name":row['name'].decode("gbk").encode("UTF-8") }
        #print rec
        try:
                 
            rs = f_info.insert_one( rec )
        except Exception , e:
            pass            
        pass        
        
    pass    

def loadFutureKhis2file( futureName ):    
    #http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M0
    url = "http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol="+futureName
    f = urllib2.urlopen(url) 
    with open(futureName + ".txt", "wb") as datafile:
        datafile.write(f.read())
    pass
    pass



def loadFutureNewPrice(futureName):
    #http://hq.sinajs.cn/list=V0
    return ''

def doFuture_all( doFunction ):
    client = MongoClient('localhost',27017)
    f_info = client.market.f_info
    data = pd.DataFrame(list(f_info.find()))
    del data['_id']
    #print type(data)
    #print data
    for index,row in data.iterrows():
        #print row['code']
        doFunction( row['code'] )
    pass

def loadFutureKhis2file_all():
    doFuture_all( loadFutureKhis2file )
    return 
    client = MongoClient('localhost',27017)
    f_info = client.market.f_info
    data = pd.DataFrame(list(f_info.find()))
    del data['_id']
    #print type(data)
    #print data
    for index,row in data.iterrows():
        #print row['code']
        loadFutureKhis2file( row['code'] )
    
    pass

def saveFutureKhis2db( futureName ):
    
    client = MongoClient('localhost',27017)
    f_k = client.market.f_k     
    f = open('./'+futureName+'.txt', 'r')
    data = f.read()
    #print data
    recList = list(eval( data ))
    print futureName, recList[len(recList)-1]
    for i in range(0, len(recList)):
        row = recList[i]
        rec ={"code":futureName,  "date": row[0],
        "open": row[1],"high": row[2],"low": row[3],"close": row[4],
        "vol": row[5] }
        try:
            rs = f_k.insert_one( rec )        
        except Exception , e:
            pass            
        pass
    f.clos8e()
 
    pass

def saveFutureKhis2db_all(  ): 
    doFuture_all( saveFutureKhis2db )
    pass

def saveFutureKNow2db_all():
    #未完待续
    pass    

#业务函数
def do():
    #stocklist = loadStocklist2file()  
    #saveStocklist2db()
    saveFuturelist2db()
 
    pass    


 

def test():
    # saveFutureKhis2db_all()
    # return 
    # saveFutureKhis2db("RU0")
    # return 
    saveFutureKhis2db("OI0")
    return
    # loadFutureKhis2file_all()
    # return 
    loadFutureKhis2file("OI0")
    return 
    url = "http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M0"
    f = urllib2.urlopen(url) 
    with open("m0.txt", "wb") as mofile:
        mofile.write(f.read())
    pass

if __name__ == "__main__":
    print ('start "test2.py"')
    #do()
    test()
