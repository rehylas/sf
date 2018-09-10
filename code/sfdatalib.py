
# -*- coding: utf-8 -*-   
#!/usr/bin/env python       
    


' a test module '            #表示模块的文档注释

__author__ = 'hylas'  #作者名

import tushare as ts
import pandas as pd 
import time
import datetime
import pymongo
import urllib2
from pymongo import MongoClient


'''
输出接口:
loadsaveStockList()
saveFuturelist2db()    # save futurelist.csv to db
loadsaveFutureKHis2db( futureName )
loadsaveFutureKHis2db_all()
loadsaveFutureKNow2db_all():

loadFutureKhis2file( futureName ) 
loadFutureKhis2file_all()
saveFutureKhis2db( futureName ) 
saveFutureKhis2db_all()

'''


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

def loadsaveStockList():
    loadStocklist2file()
    saveStocklist2db()
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

def saveFutureKhis2db( futureName, now = False ):
    
    client = MongoClient('localhost',27017)
    f_k = client.market.f_k     
    f = open('./'+futureName+'.txt', 'r')
    data = f.read()
    #print data
    recList = list(eval( data ))
    print futureName, recList[len(recList)-1]

    offset = 0
    if( now == True ):
        offset = len(recList) - 7
        if( offset <0):
            offset = 0

    for i in range(offset, len(recList)):
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

def loadsaveFutureKHis2db( futureName ):
    loadFutureKhis2file( futureName ) 
    saveFutureKhis2db( futureName )
    pass

def saveFutureKhis2db_all(  ): 
    doFuture_all( saveFutureKhis2db )
    pass

def loadFutureKhis2file_all():
    loadFutureKhis2file_all()
    saveFutureKhis2db_all()
    pass    

def loadsaveFutureKNow2db_all():
    #load data
    loadFutureKhis2file_all()  
    #save 7 day data 2 db
    client = MongoClient('localhost',27017)
    f_info = client.market.f_info
    data = pd.DataFrame(list(f_info.find()))
    del data['_id']
    #print type(data)
    #print data
    for index,row in data.iterrows():
        #print row['code']
        saveFutureKhis2db( row['code'] ,now = True )
     
    pass  



def test():
    return True

'''
当我们在命令行运行模块文件时，Python解释器把一个特殊变量__name__置为__main__，
而如果在其他地方导入该hello模块时，if判断将失败，
因此，这种if测试可以让一个模块通过命令行运行时执行一些额外的代码，
最常见的就是运行测试。
'''
if __name__=='__main__':
    test()  