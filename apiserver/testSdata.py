#!/usr/bin/python
# -*- coding: utf-8 -*-   

import tushare as ts
import numpy  as np 
import pandas as pd 
import time
import datetime
import tushare as ts
import copy
import matplotlib.pyplot as plt
from numpy.random import randn

from PotGenerator import * 

#ts.get_k_data('600000','2010-01-01', '2017-01-01') 


#              {day:"2019-03-06 11:20:00",open:"36.370",high:"36.420",low:"36.360",close:"36.390",volume:"751400",ma_price5:36.332,ma_volume5:746372},
#  {day:"2019-03-06 11:25:00",open:"36.390",high:"36.400",low:"36.330",close:"36.350",volume:"563177",ma_price5:36.33,ma_volume5:694455},
#  {day:"2019-03-06 11:30:00",open:"36.360",high:"36.410",low:"36.330",close:"36.390",volume:"709130",ma_price5:36.36,ma_volume5:681461}]


def kdata2potdata( kdata, todayData =  [] ):
    # debug 

    # todayData = [{day:"2019-03-06 11:20:00",open:"36.370",high:"36.420",low:"36.360",close:"36.390",volume:"751400",ma_price5:36.332,ma_volume5:746372},
    #     {day:"2019-03-06 11:25:00",open:"36.390",high:"36.400",low:"36.330",close:"36.350",volume:"563177",ma_price5:36.33,ma_volume5:694455},
    #     {day:"2019-03-06 11:30:00",open:"36.360",high:"36.410",low:"36.330",close:"36.390",volume:"709130",ma_price5:36.36,ma_volume5:681461}]
 
    bar =   VtMinBarData()
    potData = PotGenerator()
 
    for index, row in kdata.iterrows():
        #print  row.to_dict()
        rec = row.to_dict()    
        # print index, row
        try:       
            #do rec  
            bar.datetime = index
            bar.date = EMPTY_STRING                # 日期 20151009
            bar.time = EMPTY_STRING
            bar.endtime = EMPTY_STRING
            bar.open = rec['open']
            bar.close = rec['close']
            bar.low = rec['low']
            bar.high = rec['high']
            bar.volume = rec['volume']
            bar.price_change = rec['price_change']  

            #print bar 
            potData.updateBar( bar )                     
            pass
        except Exception , e:
            print 'except',e
            pass            
        pass     
    pass 

    print 'todayData len :', len( todayData )
    for rec in todayData:
        #print  row.to_dict()
        #print rec 
        try:  
            bar.datetime = rec['day']
            bar.date = EMPTY_STRING                # 日期 20151009
            bar.time = EMPTY_STRING
            bar.endtime = EMPTY_STRING
            bar.open = float(rec['open'])
            bar.close = float(rec['close'])
            bar.low = float(rec['low'])
            bar.high = float(rec['high'])
            bar.volume = rec['volume']
            

            #print bar 
            potData.updateBar( bar )    
        except Exception , e:
            print e.message
            pass            
        

    potlist = potData.getDataset()

    # for rec in potlist:
    #     print rec.__dict__

    #data =[]
    datalist = []
    for rec in potlist:
        print rec.datetime, rec.close  , rec.dim   ,  round( rec.dim / rec.close *100, 2) 
        #data.append( rec.close )
        datalist.append(  [ rec.datetime, rec.close  , rec.minclose,  rec.dim   ,  round( rec.dim / rec.close *100, 2) ]  )

    #drawline( data )
    return datalist 


def drawline( data ,X = None  ):

    
    # fig=plt.figure()
    if( X is None):
        plt.plot( data )  #,color='k',linestyle='dashed',marker='o'
    else:
        plt.plot( np.array( X) , np.array( data[0]  ) )        
        #plt.plot(X,data[1])
    plt.show()
 

#输出
def  getStockPotList( code, potrate = None, peroid =None ):
    kdata = ts.get_hist_data( code, ktype='5'  )
    kdata = kdata.sort_index(ascending=True)
    todaydata = getTodayM5( code  )
    datalist = kdata2potdata( kdata, todayData = todaydata )   
    return  datalist
    pass 
     
def test(): 
    # kdata = ts.get_hist_data('002415', ktype='5', start='2019-02-05', end='2019-03-05' )
    # kdata = kdata.sort_index(ascending=True)
    # #print kdata
    # #print kdata
    # datalist = kdata2potdata( kdata )

    datalist = getStockPotList( '002415' ) 
    pdData = pd.DataFrame( datalist )
    
    s_dt = pdData[0]
    s_close = pdData[1]
    s_minclose = pdData[2]

    dfsub = pdData[[1,2]]

    #print s_close
    drawline( dfsub  ) 

    print s_dt

    pass

import json
def test2(  todayData  ):
    # debug 

    # todayData = '[{day:"2019-03-06 11:20:00",open:"36.370",high:"36.420",low:"36.360",close:"36.390",volume:"751400",ma_price5:36.332,ma_volume5:746372}, \
    #     {day:"2019-03-06 11:25:00",open:"36.390",high:"36.400",low:"36.330",close:"36.350",volume:"563177",ma_price5:36.33,ma_volume5:694455},  \
    #     {day:"2019-03-06 11:30:00",open:"36.360",high:"36.410",low:"36.330",close:"36.390",volume:"709130",ma_price5:36.36,ma_volume5:681461}] '
    
    todayData = todayData.replace('day','"day"')
    todayData = todayData.replace(',volume',',"volume"')
    todayData = todayData.replace('ma_price5','"ma_price5"')
    todayData = todayData.replace('ma_volume5','"ma_volume5"')
    todayData = todayData.replace('open','"open"')
    todayData = todayData.replace('close','"close"')
    todayData = todayData.replace('high','"high"')
    todayData = todayData.replace('low','"low"')

    print todayData
    #todayData = '[{"day":"1234"},2,3]'
    npdata = json.loads( todayData )

    print npdata
    #print len(npdata)
    print 'record[0]:', npdata[0]
    print '----------------'
      


    bar =   VtMinBarData()
    potData = PotGenerator()
 
    for index in range( len(npdata) ):
        #print  row.to_dict()
        rec = npdata[index] 
        print 'rec:', rec #todayData[index] 
        bar.datetime = rec['day']
        bar.date = EMPTY_STRING                # 日期 20151009
        bar.time = EMPTY_STRING
        bar.endtime = EMPTY_STRING
        bar.open = float(rec['open'])
        bar.close = float(rec['close'])
        bar.low = float(rec['low'])
        bar.high = float(rec['high'])
        bar.volume = rec['volume'] 
        bar.price_change = 0.0 

        #print bar 
        potData.updateBar( bar )     

    potlist = potData.getDataset()

    # for rec in potlist:
    #     print rec.__dict__

    #data =[]
    datalist = []
    for rec in potlist:
        print rec.datetime, rec.close  , rec.dim   ,  round( rec.dim / rec.close *100, 2) 
        #data.append( rec.close )
        datalist.append(  [ rec.datetime, rec.close  , rec.minclose,  rec.dim   ,  round( rec.dim / rec.close *100, 2) ]  )

    #drawline( data )
    return datalist 

def getStockmin5FromSina(code):
    if( code[0] == '6' ):
        pass
        codelab = 'sh' + code
    else:
        codelab = 'sz' + code
        pass
    #http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz002415&scale=5&ma=5&datalen=1023
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=' + codelab +'&scale=5&ma=5&datalen=1023'


    import requests #导入requests，然后就可以为所欲为了

    #发送get请求

    r0 = requests.get( url )
    #print r0.text
    return r0.text

    pass

import time 
def getTodayM5( code ):
    localTime = time.localtime( ) #timeStamp
    todayStr = time.strftime('%Y-%m-%d', localTime)  +   ' 00:00:00'
    print 'todayStr:', todayStr

    todayData = getStockmin5FromSina(code)
    todayData = todayData.replace('day','"day"')
    todayData = todayData.replace(',volume',',"volume"')
    todayData = todayData.replace('ma_price5','"ma_price5"')
    todayData = todayData.replace('ma_volume5','"ma_volume5"')
    todayData = todayData.replace('open','"open"')
    todayData = todayData.replace('close','"close"')
    todayData = todayData.replace('high','"high"')
    todayData = todayData.replace('low','"low"')

    # print todayData
    # todayData = '[{"day":"1234"},2,3]'
    npdata = json.loads( todayData )
    todayList = []
    for rec in npdata:     
        #print rec   
        if( rec['day'] >= todayStr ):
            todayList.append( rec )
    return todayList
    pass

if __name__ == "__main__":
    print ('start "testsdata.py"')
    
    #do()
    print test()

    # sinadata = getStockmin5FromSina('002415')
    # test2( sinadata )

    # print getTodayM5( '002415' )

 




