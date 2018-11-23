# -*- coding: utf-8 -*-   
#!/usr/bin/env python       



import time
import os
import datetime
import pymongo
import urllib2
from pymongo import MongoClient
import json

import pandas as pd 
import ConfigParser

from flask import Flask
from flask_cors import CORS


DB_INFO ={ "IP":"127.0.0.1", "PORT":27017 }
MYTRADER_DB_INFO ={ "IP":"192.168.0.8", "PORT":27017 }

dbClient = None
dbClient_Mytrader =  None 

app = Flask(__name__)
#app.run( host='0.0.0.0' )
CORS(app, supports_credentials=True)
app.logger.debug('app start ...')

#app.run(debug=True, use_reloader=False)
#client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] ) 

def readcfg():
    global DB_INFO
    global dbClient_Mytrader 

    app.logger.debug('readcfg')
    cf=ConfigParser.ConfigParser()
    cf.read("./config.ini")
    db_host = None
    db_host_mytrader = None
    try:
        db_host = cf.get("db", "db_host")
        db_host_mytrader = cf.get("db", "db_host_mytrader")
    except:
        print "get db db_host error"    

    if( db_host != None ):
        DB_INFO ={ "IP":db_host, "PORT":27017 }
        MYTRADER_DB_INFO ={ "IP":db_host, "PORT":27017 }
    
    if( db_host_mytrader != None ):
        MYTRADER_DB_INFO ={ "IP":db_host_mytrader, "PORT":27017 }
        dbClient_Mytrader = MongoClient( MYTRADER_DB_INFO["IP"], MYTRADER_DB_INFO["PORT"] )
    else:
        dbClient_Mytrader = MongoClient( MYTRADER_DB_INFO["IP"], MYTRADER_DB_INFO["PORT"] )

    pass

readcfg()


@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath


@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

 

########################################################
# 业务
# /future/zf/<code>
# /future/zf_top5/<date>
# /future/zf_top5
# /future/signal_in_zf_top5
# /future/kline/RU0
########################################################

#获取振幅曲线  
#/future/zf/RU0
@app.route('/future/zf/<code>')
def future_zf_list(code):
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_zf20 = client.market.f_zf20
    data_list =  list( f_zf20.find( {"code": code } ).sort( "date"  , -1 )  )
    data = pd.DataFrame( data_list ) 
    del data['_id']
    #print data_list
    #
    #
    if( len(data_list) >120 ):
        dataLen = 120
    else:
        dataLen =len(data_list)    
    resp ='{"data":['
    for i in range(0, dataLen):
        #jstr = json.dumps( data_list[i] )
        
        item = data_list[i] 
        item.pop('_id')
        print item
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr  
    resp += ']}'
    
    return ''+resp


#获取进入前5清单
@app.route('/future/zf_top5/<date>')
def future_zf_top5_list(date = None):
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_signal_zf20 = client.market.f_signal_zf20
    if( date == None ):
        sqlWhere =  { "type":1 }
    else:    
        sqlWhere =  { "date":date,"type":1 }
    data_list =  list( f_signal_zf20.find( sqlWhere ).sort( "date"  , -1 ).limit(10)  )
 
    if( len(data_list) >5 ):
        dataLen = 5
    else:
        dataLen =len(data_list)    
    resp ='{"data":['
    for i in range(0, dataLen):
        #jstr = json.dumps( data_list[i] )
        item = data_list[i] 
        item.pop('_id')
        print item
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr  
    resp += ']}'
    
    return ''+resp

@app.route('/future/zf_top5')
def future_zf_top5_list_today(  ):
   
    return future_zf_top5_list()

 
#获得进入前5的信号
@app.route('/future/signal_in_zf_top5')
def future_zf_in_top5_today(  ):
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_signal_zf20 = client.market.f_signal_zf20
    date =None
    if( date == None ):
        sqlWhere =  { "type":2 }
    else:    
        sqlWhere =  { "date":date,"type":2 }
    data_list =  list( f_signal_zf20.find( sqlWhere ).sort( "date"  , -1 ).limit(60)  )
 
    dataLen =len(data_list)    

    resp ='{"data":['
    for i in range(0, dataLen):
     
        #jstr = json.dumps( data_list[i] )
        item = data_list[i] 
        item.pop('_id')
        print item
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr    
    resp += ']}'
    
    return ''+resp
    


#获取K线
#/future/kline/RU0
@app.route('/future/kline/<code>')
def future_kline_list(code):
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    # db.getCollection('f_k').find({'code':'RU0'})
    f_k = client.market.f_k
    data_list =  list( f_k.find( {"code": code } ).sort( "date"  , -1 )  )
    data = pd.DataFrame( data_list ) 
    del data['_id']
    #print data_list
    #
    #
    if( len(data_list) >120 ):
        dataLen = 120
    else:
        dataLen =len(data_list)    
    resp ='{"data":['
    for i in range(0, dataLen):
        #jstr = json.dumps( data_list[i] )
        
        item = data_list[i] 
        item.pop('_id')
        print item
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr  
    resp += ']}'
    
    return ''+resp

#获取分时线
#/future/minline/RU0
@app.route('/future/minline/<code>/<curDate>')
def future_minline_list(code, curDate=None):
    print code, curDate
    resp =""
    '''
        db.getCollection('ru1901').find(   {$or :  [   {'time' : {$gte : '20:55:00'},  'date': '20181106' } , 
        { 'time' : {$lte : '15:16:00'}, 'date':  '20181107' } ] } )
    '''
    collectionName = getMainSymbol( code )

    db = dbClient_Mytrader.MyTrader_1Min_Db
    collection = db[collectionName]
    
    strToday, strYestoday = getDate( sDate = curDate )
    sqlWhere =     {'$or' :  [   {'time' : {'$gte' : '20:55:00'},  'date':  strYestoday } ,   { 'time' : {'$lte' : '15:16:00'}, 'date':  strToday } ] }  


    # if curDate == None :
    #     strDate = ''
    #     sqlWhere = {}
    # else:    
    #     sqlWhere =  { 'time' : {'$gte' : '09:06:00'}, 'date':strDate  } 
    print 'sqlWhere:',sqlWhere
    data_list =  list( collection.find( sqlWhere ).sort(   [("date",1),("time",1) ]   )  )
    dataLen =len(data_list)        
    resp ='{"data":['
    for i in range(0, dataLen):
        #jstr = json.dumps( data_list[i] )
        
        item = data_list[i] 
 

        item.pop('_id')
        item.pop('datetime')
        #print item
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr  
    resp += ']}'

    return ''+resp
    pass
  

#获取Signal 数据
#/future/signal/RU0
@app.route('/future/signal/<code>/<curDate>')
def future_signal_list(code, curDate=None):
    print code, curDate
    signalCode = 'goodpot'
    resp =""
    '''
        db.getCollection('ru1901').find(   {$or :  [   {'time' : {$gte : '20:55:00'},  'date': '20181106' } , 
        { 'time' : {$lte : '15:16:00'}, 'date':  '20181107' } ] } )
    '''
    collectionName = getMainSymbol( code )

    db = dbClient_Mytrader.MyTrader_SignalTrading_Db
    collection = db[collectionName]
    
    strToday, strYestoday = getDate( sDate = curDate )
    sqlWhere =     {'$or' :  [   {'time' : {'$gte' : '20:55:00'},  'date':  strYestoday, 'code':signalCode } ,   { 'time' : {'$lte' : '15:16:00'}, 'date':  strToday, 'code':signalCode  } ] }  


    # if curDate == None :
    #     strDate = ''
    #     sqlWhere = {}
    # else:    
    #     sqlWhere =  { 'time' : {'$gte' : '09:06:00'}, 'date':strDate  } 
    print 'sqlWhere:',sqlWhere
    data_list =  list( collection.find( sqlWhere ).sort(   [("date",1),("time",1) ]   )  )
    dataLen =len(data_list)        
    resp ='{"data":['
    for i in range(0, dataLen):
        #jstr = json.dumps( data_list[i] )
        
        item = data_list[i] 
        item.pop('_id')
        item.pop('datetime')
        #print item
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr  
    resp += ']}'

    return ''+resp
    pass


#获取Exdata 数据
#/future/exdata/pot/RU0
@app.route('/future/exdata/<datatype>/<code>/<curDate>')
def future_exdata_list(code, datatype, curDate=None):
    print code, curDate
    signalCode = 'goodpot'
    resp = getExdataFromDB(code,datatype, curDate)
    return ''+resp
    pass

#-------------------------------------------------------------------------
# 内部函数
# 从数据库里获取扩展数据
def getExdataFromDB( code, datatype, sDate ):
    print code, datatype, sDate 
   
    resp =""
    collectionName = getMainSymbol( code )

    db = dbClient_Mytrader.MyTrader_Exdata_Db
    collection = db[collectionName]
    
    strToday, strYestoday = getDate( sDate = sDate )
    sqlWhere =     {'$or' :  [   {'time' : {'$gte' : '20:55:00'},  'date':  strYestoday, 'datatype':datatype } ,   { 'time' : {'$lte' : '15:16:00'}, 'date':  strToday, 'datatype':datatype } ] }  


    # if curDate == None :
    #     strDate = ''
    #     sqlWhere = {}
    # else:    
    #     sqlWhere =  { 'time' : {'$gte' : '09:06:00'}, 'date':strDate  } 
    print 'sqlWhere:',sqlWhere
    data_list =  list( collection.find( sqlWhere ).sort(   [("date",1),("time",1) ]   )  )
    dataLen =len(data_list)        
    resp ='{"data":['
    for i in range(0, dataLen):
        #jstr = json.dumps( data_list[i] )
        
        item = data_list[i] 
        #print item
        item.pop('_id')
        item.pop('datetime')
        if( datatype =='pot' or datatype == 'jump'):
            item.pop('endtime')
        #print item
      
        jstr = json.dumps(  item )
        if( i != 0 ):
            resp += ','+  jstr 
        else:
            resp += jstr  
    resp += ']}'

    return ''+resp
    pass




# 获取主力合约代码
def getMainSymbol( code ):
    cf=ConfigParser.ConfigParser()
    cf.read("./config.ini")
    Symbol = 'ru1901'
    try:
        Symbol = cf.get("maincode", code )   
           
    except:
        print "get cfg maincode error ", code    

    return Symbol 

def getDate( sDate = None ):
    strToday,strYestoday ='',''
    if( sDate == None ):
        # 格式化成2016-03-20 11:45:39形式
        now = datetime.datetime.now()
         
        strToday = now.strftime("%Y%m%d")     #"%Y-%m-%d %H:%M:%S"
        yesTerday = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        strYestoday = yesTerday.strftime("%Y%m%d")      
    else:
      
        now = datetime.datetime.strptime(sDate, '%Y-%m-%d')
        strToday = now.strftime("%Y%m%d")     #"%Y-%m-%d %H:%M:%S"
        yesTerday = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        strYestoday = yesTerday.strftime("%Y%m%d")              
        pass

    print     strToday,strYestoday
    return strToday,strYestoday


