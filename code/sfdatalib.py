
# -*- coding: utf-8 -*-   
#!/usr/bin/env python       
    
' a stock future data module '            #表示模块的文档注释

__author__ = 'hylas'  #作者名

import tushare as ts
import pandas as pd 
import time
import os
import struct
import shutil
import datetime
import pymongo
import urllib2
from pymongo import MongoClient

import ConfigParser


#DB_INFO ={ "IP":"192.168.0.208", "PORT":27017 }
DB_INFO ={ "IP":"127.0.0.1", "PORT":27017 }
 

def readcfg():
    global DB_INFO
    cf=ConfigParser.ConfigParser()
    cf.read("./config.ini")
    db_host = None
    try:
        db_host = cf.get("db", "db_host")
    except:
        print "get db db_host error"    
    if( db_host != None ):
        DB_INFO ={ "IP":db_host, "PORT":27017 }
    pass

readcfg()

'''
输出接口:
loadsaveStockList()
loadsaveStockKHis2db( code )
loadsaveStockKHis2db_all()
saveFuturelist2db()    # save futurelist.csv to db
loadsaveFutureKHis2db( futureName )
loadsaveFutureKHis2db_all()
loadsaveFutureKNow2db_all() 
minupBak()
minup2tdx()
minupMonitor()

makeFutureZf20( futureName, nDay = 1 )
makeFuturezf20_all( )
signalFutureZf20( futureName, nDay = 1 )


loadFutureKhis2file( futureName ) 
loadFutureKhis2file_all()
saveFutureKhis2db( futureName ) 
saveFutureKhis2db_all()

'''


######################## STOCK minup     相关业务 #########################

#-------------------------------------------------------------------------------------------
#C:\Users\Administrator\Downloads\DZH8.21.00.17283\USERDATA\selfstock\1234\自选MINSUP.slf
#   ==> 自选MINSUP0109.slf 
#
#
#
SELFSTOCK_PATH = 'C:/Users/Administrator/Downloads/DZH8.21.00.17283/USERDATA/selfstock/1234/'
def minupBak():
    now = datetime.datetime.now()  
    desFile = SELFSTOCK_PATH + u'自选MINSUP'+   "{0:02d}".format(now.month) +   "{0:02d}".format(now.day)+'.slf'
    scrFile = SELFSTOCK_PATH + u'自选MINSUP.slf'
    #print now.year, now.month, now.day  , now.hour, now.minute, now.second, now.microsecond   

    if not os.path.isfile(scrFile):
        print scrFile
        print 'is not exist'
        return
        
    if    os.path.isfile( desFile ):
        os.remove( desFile )

    if  not os.path.isfile( desFile ):
      
        shutil.copyfile( scrFile, desFile )      #复制文件

    pass

#-------------------------------------------------------------------------------------------
# .slf 数据格式   
#  16 字节 + n x  20 字节   
#  20 字节 =  12（名称） + 2 （sh / sz） +  6 ( 代码 600177) 
#
SELFSTOCK_PATH_TDX = u'D:/stock/方正证券/T0002/blocknew/'     #*.blk
def minup2tdx():
    now = datetime.datetime.now()  
    
    scrFile = SELFSTOCK_PATH + u'自选MINSUP.slf'
    desFile = SELFSTOCK_PATH_TDX + u'MINSUP.blk'
    #print now.year, now.month, now.day  , now.hour, now.minute, now.second, now.microsecond   

    if not os.path.isfile(scrFile):
        print scrFile
        print 'is not exist'
        return 

    if    os.path.isfile( desFile ):
        os.remove( desFile )

        pass
    
    # file 2 list 
    stocks = dzhfile2list( scrFile )
    # list 2 tdx file 
    list2tdxfile( stocks , desFile )

    pass 


def minupMonitor():
    pass        

#------------------------------------------------------------------------
# 大智慧自选股解析
# .slf 数据格式   
#  16 字节 + n x  20 字节   
#  20 字节 =  12（名称） + 2 （sh / sz） +  6 ( 代码 600177) 
def dzhfile2list(dzffile):
    sList = []
    data_offset = 16
    data_width = 20
    try:
        ofile=open( dzffile ,'rb')
        buf=ofile.read()
        ofile.close()
        
        num=len(buf)
        no=(num-data_offset)/data_width
        b = data_offset                         #begin
        e = data_offset + data_width            #end   
      
        for i in xrange(no):
            #a=unpack('hhfffffii',buf[b:e])
            name,code = struct.unpack("!12s8s",  buf[b:e] )
            print code
            sList.append( code )
            b=b+ data_width
            e=e+ data_width
        #print dl   
        
    except Exception, e:
        print e.message
        return []        
    #print df   
   
    return sList
    pass   


#------------------------------------------------------------------------
# 大智慧自选股解析
# 
def list2tdxfile(stockList,tdxfile):
    lines =[]
    for rec in stockList:
        sc = rec[0:2]
        code = rec[2:8]
        codelab = '' +code + '\n'
        if( sc== 'SH' ):
            codelab = '1' +code + '\n'
        if( sc== 'SZ' ):
            codelab = '0' +code  + '\n' 
        lines.append( codelab )                    

    wfile = open(tdxfile, 'w')
    wfile.writelines( lines )
    
    return 0
    pass 

######################## STOCK minup end         #########################


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
    #ts.get_k_data(code,'2010-01-01', '2019-02-18') 
    code =  code.strip()  
    kdata = ts.get_k_data(code,'2010-01-01', '2019-02-18' ) 
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
        try:
            pass
            doFunction( row['code'] )
        except Exception, e :
            print 'Exception on exec doFunction:', row['code'] 
            print e
            pass        
        
        #break
    pass
    print ""

# def loadFutureKhis2file_all():
#     doFuture_all( loadFutureKhis2file )

#     pass    

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
    if(data == None) :
        f.close()
        return 

    #print data
    recList = list(eval( data ))
    if(len( recList) <=0 ):
        print 'futureName 0 data'
        return 
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
    try:
        pass
        saveFutureKhis2db( futureName )
    except Exception, e :
        print 'Exception on exec saveFutureKhis2db:', futureName
        print e
        pass
    
    pass

def saveFutureKhis2db_all(  ): 
    doFuture_all( saveFutureKhis2db )
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

        try:
            pass
            saveFutureKhis2db( row['code'] ,now = True  )
        except Exception, e :
            print 'Exception on exec saveFutureKhis2db:', row['code']
            print e
            pass        
      
     
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
        rec_info = {"code":row_one.code, "date":row_one.date, "zf":row_one.zf,"zf5":zfinfo[0], "zf20": zfinfo[1]  }
        try:
            rs = f_zf20.insert_one( rec_info )        
        except Exception , e:
            pass     
      

    pass

def makeFuturezf20_all( ):
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


#  倒20 个时间， 横向比较所有品种 统计最大5个  type = 1
#  倒20 个时间， 取当日所有品种  和  昨日所有品种比较，  新进前5做为 signal   type = 2
def signalFutureZf(  nDay = 20 ):
    now = time.localtime( time.time() - 86400*0 )   
    todayStr = time.strftime('%Y-%m-%d',  now )

    oneDay = time.localtime( time.time() - 86400*nDay )   
    onedayStr = time.strftime('%Y-%m-%d',  oneDay )

    #top  5
    for index in range(0,nDay):
        oneDay = time.localtime( time.time() - 86400*index )   
        onedayStr = time.strftime('%Y-%m-%d',  oneDay )        
        maxFutureZf2db( onedayStr )

    #in top 5
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_zf20 = client.market.f_zf20
    data = pd.DataFrame( list( f_zf20.find( {"code":"RU0"}  ).sort( "date"  , -1 ) ) )
    print data
    for index in range(0,nDay):
        if( index+1  >= len(data) ):
            break
        row_one = data.iloc[index]
        row_one_bef = data.iloc[index+1]
        print row_one.date, row_one_bef.date
        inMaxFuturezftop5( row_one.date, row_one_bef.date)
        pass
    pass


#db.f_zf20.find({date:"2018-09-14" }).sort({"zf20":-1} )
__MAX_ZF_COUNT = 5
def maxFutureZf2db( dateStr ):
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_k = client.market.f_k
    f_zf20 = client.market.f_zf20
    f_signal_zf20  = client.market.f_signal_zf20
    print dateStr
     

    data = pd.DataFrame( list( f_zf20.find( {"date":dateStr}  ).sort( "zf20"  , -1 ) ) )
    #print data
    if( len(data)  < __MAX_ZF_COUNT ):
        return

    for index in range( 0,__MAX_ZF_COUNT ):
        #print index, len(data)
        row_one = data.iloc[index]
        #print row_one.date , row_one.code, row_one.zf20

        rec_info = {"code":row_one.code, "date":row_one.date, "zf20":row_one.zf20,"type":1, "param1":index+1   }
        try:
            rs = f_signal_zf20.insert_one( rec_info )        
        except Exception , e:
            pass 

        pass
            
    pass

def inMaxFuturezftop5( oneDay, befDay):      
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_zf20 = client.market.f_zf20
    f_signal_zf20  = client.market.f_signal_zf20    

    data_day = pd.DataFrame( list( f_signal_zf20.find( {"date":oneDay,"type":1}  ) ) )
    data_bef = pd.DataFrame( list( f_signal_zf20.find( {"date":befDay,"type":1}  ) ) )

    if( len(data_day) != __MAX_ZF_COUNT or len(data_bef) != __MAX_ZF_COUNT  ):
        # print data_day
        # print data_bef
        print 'len != ', __MAX_ZF_COUNT, " ", len(data_day), len(data_bef)
        return 

    oneDayList =[]
    befDayList=[]
 
    for index in range(0, __MAX_ZF_COUNT) :
        oneDayList.append(  data_day.iloc[index].code  )
        befDayList.append(  data_bef.iloc[index].code  )

        pass   
    # print oneDayList
    # print befDayList    
    dimList = [item for item in oneDayList if item not in befDayList ]
    #print dimList
    print 'new ', len(dimList), " in top 5"
    for index in range(0, len(dimList) ):
        rec_info = {"code":dimList[index], "date":oneDay, "zf20":0.0,"type":2, "param1":0   }
        try:
            rs = f_signal_zf20.insert_one( rec_info )        
        except Exception , e:
            pass 
    pass

def signalFutureZf_all(  ):
    pass


'''
id, tag, version, count = struct.unpack("!H4s2I", s)

https://www.cnblogs.com/gala/archive/2011/09/22/2184801.html
id, tag, version, count = struct.unpack("!H4s2I", s)
struct Header
{

    unsigned short id;

    char[4] tag;

    unsigned int version;

    unsigned int count;

}
'''

import datetime
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
    #makeFuturezf20_all()
    #signalFutureZf()
    

     

    #inMaxFuturezftop5("2018-09-11", "2018-09-10" )

    # A= [1,2,3]
    # B= [2,3,4]

    # dim_list = [item for item in B if item not in A]
    # print dim_list

 

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