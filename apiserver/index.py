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
 
app = Flask(__name__)
app.run( host='0.0.0.0' )
CORS(app, supports_credentials=True)
app.logger.debug('app start ...')

 

def readcfg():
    global DB_INFO
    app.logger.debug('readcfg')
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