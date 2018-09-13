
# -*- coding: utf-8 -*-   
#!/usr/bin/env python       
    


' a stock future data module '            #表示模块的文档注释

__author__ = 'hylas'  #作者名

import tushare as ts
import pandas as pd 
import time
import datetime
import pymongo
import urllib2
from pymongo import MongoClient

DB_INFO ={ "IP":"192.168.0.208", "PORT":27017 }


'''
输出接口:
loadsaveStockList()
loadsaveStockKHis2db( code )
loadsaveStockKHis2db_all()
saveFuturelist2db()    # save futurelist.csv to db
loadsaveFutureKHis2db( futureName )
loadsaveFutureKHis2db_all()
loadsaveFutureKNow2db_all() 

makeFutureZf20( futureName, nDay = 1 )
signalFutureZf20( futureName, nDay = 1 )


loadFutureKhis2file( futureName ) 
loadFutureKhis2file_all()
saveFutureKhis2db( futureName ) 
saveFutureKhis2db_all()

'''

######################## STOCK #########################
def loadStocklist2file():
    stocklist = ts.get_stock_basics()
    stocklist.to_csv("stocklist.csv")
    #data = pd.read_csv( "stocklist.csv" )
    return stocklist
    pass

def saveStocklist2db():
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    stock_info = client.market.stock_info
    data = loadStocklist2file()
    #print data[0:2]
 
    for index, row in data.iterrows():
        #print  row.to_dict()
        rec = row.to_dict()
        rec["code"]=index    
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

def loadsaveStockKHis2db( code ):
    #ts.get_k_data(code,'2010-01-01', '2017-01-01') 
    code =  code.strip()  
    kdata = ts.get_k_data(code,'2010-01-01', '2018-09-01' ) 
    kdata = kdata[:-1]  #去掉当天
    print type(kdata), '  len:', len(kdata)
    print kdata[-2:]
 
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    stock_k_his = client.market.stock_k_his    
    for index, row in kdata.iterrows():
        #print  row.to_dict()
        rec = row.to_dict()    
        try:                  
            rs = stock_k_his.insert_one( rec )
        except Exception , e:
            pass            
        pass 
    
    print '*'

    pass

#与his的区别是，只保存最近30天，提高效率， 
#如果是  16:00 以前，不保存当天
#
def loadsaveStockK2db( code ):
    #ts.get_k_data(code,'2010-01-01', '2017-01-01') 
    code =  code.strip()  
    kdata = ts.get_k_data(code ) 
    
    kdata = kdata[-31:] #最近30天
    localtime = time.localtime(time.time())
    if(localtime.tm_hour <16 ):
        kdata = kdata[:-1]  #去掉当天

    print type(kdata), '  len:', len(kdata)
    #print kdata[-2:]

    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    stock_k = client.market.stock_k   
    for index, row in kdata.iterrows():
        #print  row.to_dict()
        rec = row.to_dict()    
        try:                  
            rs = stock_k.insert_one( rec )
        except Exception , e:
            pass            
        pass 
    
    print '*'

    pass

def loadsaveStockKHis2db_all() :
    doStock_all( loadsaveStockKHis2db )
    pass

def loadsaveStockK2db_all() :
    doStock_all( loadsaveStockK2db )
    pass

def doStock_all( doFunction ):
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    stock_info = client.market.stock_info
    data = pd.DataFrame(list(stock_info.find()))
    del data['_id']
    #print type(data)
    #print data
    for index,row in data.iterrows():
        print ".",
        doFunction( row['code'] )
        #break
    pass
    print ""

######################## FUTURE #########################
def saveFuturelist2db():
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
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
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_info = client.market.f_info
    data = pd.DataFrame(list(f_info.find()))
    del data['_id']
    #print type(data)
    #print data
    for index,row in data.iterrows():
        #print row['code']
        print ".",
        doFunction( row['code'] )
        #break
    pass
    print ""

def loadFutureKhis2file_all():
    doFuture_all( loadFutureKhis2file )
    return 
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
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
    
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
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
    f.close()
 
    pass

def loadsaveFutureKHis2db( futureName ):
    loadFutureKhis2file( futureName ) 
    saveFutureKhis2db( futureName )
    pass

def saveFutureKhis2db_all(  ): 
    doFuture_all( saveFutureKhis2db )
    pass

def loadFutureKhis2file_all():
    doFuture_all( loadFutureKhis2file )

    pass    

def loadsaveFutureKHis2db_all():
    doFuture_all( loadsaveFutureKHis2db )
 
    pass    

def loadsaveFutureKNow2db_all():
    #load data
    print 'loadFutureKhis2file all '
    loadFutureKhis2file_all()  
      
    #save 7 day data 2 db
    print 'save 7 day data 2 db '
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_info = client.market.f_info
    data = pd.DataFrame(list(f_info.find()))
    del data['_id']
    #print type(data)
    #print data
    
    for index,row in data.iterrows():
        #print row['code']
        saveFutureKhis2db( row['code'] ,now = True )
     
    pass  

# f_zf20     { code, date,  zf, zf5, zf20  }
def makeFutureZf20( futureName, nDay = 20 ):
    # make zf20 data  2 db
    print 'make zf20 data  2 db '
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_k = client.market.f_k
    f_zf20 = client.market.f_zf20
 
    data = pd.DataFrame( list( f_k.find( {"code": futureName } ).sort( "date"  , 1 ) ) )
    del data['_id']
    #print type(data)
    #print data

    data[['high', 'low']] = data[['high', 'low']].astype(float)

    data['zf'] = (data['high'] - data['low']) *100 / data['low']
  
 
    data['zf5'] = 0.0
    data['zf20'] = 0.0

    nlen = len(data)    
    for offset in range( nlen-nDay, nlen  ):
        print offset, nlen
        zfinfo = calcFutureZf(offset, data)
        row_one = data.iloc[offset]
        rec_info = {"code":row_one.code, "date":row_one.date, "zf":row_one.zf,"zf5":zfinfo[0], "zf20": zfinfo[0]  }
        try:
            rs = f_zf20.insert_one( rec_info )        
        except Exception , e:
            pass     
      

    pass

def makeFutureZf20_all():
    doFuture_all( makeFutureZf20 )
    pass
 


def calcFutureZf( index, datadf ):
    nlen = len( datadf )  
    data5 = datadf[index+1-5:index+1]
    s_zf = data5['zf']
    zf5 = s_zf.mean()

    data20 = datadf[index+1-20:index+1]
    s_zf = data20['zf']
    zf20 = s_zf.mean()


    return [  round(zf5,2), round(zf20,2)  ]
    pass

#db.f_zf20.find({ date:"2018-09-13" }).sort( {"zf20":-1} )
def signalFutureMa( futureName, nDay = 1 ):
    pass


def test():
    #loadsaveStockList()
    #loadsaveFutureKNow2db_all()
    #loadFutureKhis2file_all()
    #loadsaveFutureKHis2db_all()
    #loadsaveStockKHis2db('600000')
    #loadsaveStockKHis2db_all()
    #loadsaveStockK2db_all()

    #saveStocklist2db()
    #makeFutureZf20( "RU0")
    makeFutureZf20_all()

    return True

'''
loadsaveStockList()
saveFuturelist2db()    # save futurelist.csv to db
loadsaveFutureKHis2db( futureName )
loadsaveFutureKHis2db_all()
loadsaveFutureKNow2db_all()
'''
if __name__=='__main__':
    test()  