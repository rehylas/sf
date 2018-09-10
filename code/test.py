#!/usr/bin/python
# -*- coding: UTF-8 -*

import tushare as ts
import numpy  as np 
import pandas as pd 
import time
import datetime

#ts.get_k_data('600000','2010-01-01', '2017-01-01') 

def test(): 
    kdata = ts.get_k_data('600000' ) 
    print type(kdata)
    kdata['yang'] =0
    kdata['hengpan'] =0
    kdata['isOk'] = 0


    subdata = kdata[0:10]
    print kdata[0:10]

    t = time.time()
    
    for index, row in subdata.iterrows():
        
        #row.isOk = 1    
        subdata.iloc[0,9] =1
        pass
        #print index
        #print row

    t2 = time.time()
    print 'time:',  (int(round(t2 * 1000))) -   (int(round(t * 1000)))
    

    print subdata

#获取k线，保存到文件
def getAdata( code ):
    kdata = ts.get_k_data( code ) 
    kdata['yang'] =0
    kdata['hengpan'] =0
    kdata['isOk'] = 0    
    kdata.to_csv(code+'.csv')
    pass

#读取文件，计算结果，保存到文件
#计算1： 遍历行，选出大阳线，   且volume*close > 10000 万
#计算2： 遍历行，前20个交易日， 计算振幅小于20%， 
#       振幅公式：(max(close,open)-min(close,open)) / min(close,open) <20%
#计算3： 1, 2项为1, （注：1项是前一个交易日 ） isOk 为1
# date    open   close    high     low    volume    code  yang  hengpan  isOk

def dofile( filename ):
    kdata = pd.read_csv(filename, index_col =0 )
    subdata = kdata[-10:] 

    #计算1  #amount = vol/100*close  = xxx 万元
    for index, row in kdata.iterrows():
        if(index <=0 ):
            continue
            pass
        amount =  row.volume/100*row.close 
        preClose = kdata.iloc[ index-1, 2  ]  
        rate = (row.close -preClose) *100 /preClose 
        
        #print 'rate & amount ', row.date, rate, amount 
        if(rate >4 and amount >10000 ):
            #print 'row:', row
            kdata.iloc[ index , 7 ] = 1
            pass

     
    #计算2
    for index, row in kdata.iterrows():

        if(index <20 or index == len(kdata)  -1 ):
            continue
            pass
        subdata = kdata.iloc[index-20:index+1]  
        s_close = subdata['close']
        s_open = subdata['open']

        s_close_max = s_close.max() 
        s_open_max = s_open.max()
        s_close_min = s_close.min()
        s_open_min = s_open.min()

        maxprice =  ( s_close_max  if( s_close_max> s_open_max)  else  s_open_max  )  
        minprice =  ( s_close_min  if( s_close_min< s_open_min ) else  s_open_min  ) 
        rate = (maxprice - minprice) *100 / minprice      
        if(rate<20):
            kdata.iloc[ index , 8 ] = 1

    #计算3
    for index, row in kdata.iterrows():
        if(index <20 or index == len(kdata)  -1 ):
            continue 
            pass
        if( kdata.iloc[ index , 7 ] == 1 and kdata.iloc[ index-1 , 8 ] == 1  ):
           kdata.iloc[ index , 9 ] = 1 

    
    kdata.to_csv( filename+'_2.csv')
    print kdata[-10:]
    pass

#统计盈利亏损，
#亏损：L低于信号当日收盘，或者C低于1/2 信号当日收盘
#盈利：盈利超过 20 %
#不亏，不盈利

def countfileWinFail(filename):
    kdata = pd.read_csv(filename, index_col =0 )
    subdata = kdata[-10:] 

    kdata['winfailFag'] =0    # 1，失败  2，中性； 3，盈利
    kdata['winfailRate'] =0.0


    #计算
    for index, row in kdata.iterrows():
        if(index <=20 or index >= len(kdata)  -20 ):
            continue
            pass
        if(row.isOk == 0 ):
            continue            

        inprice = row.close
        maxfailprice = kdata.iloc[ index-1 , 2 ]

        afterData =  kdata.iloc[index+1:index+21]           
        print 'info code,date,fag, close,preclose:', row.code,row.date,row.isOk,row.close,maxfailprice
        countRet = countWinFail(afterData, inprice=inprice, maxfailprice =maxfailprice  )
        print 'count result:', countRet
        kdata.iloc[ index , 10 ] = countRet[0] 
        kdata.iloc[ index , 11 ] = countRet[1] 
        kdata.to_csv( filename+'_3.csv')


    pass

#统计单笔盈利亏损
#亏损：L低于信号当日收盘，或者C低于1/2 信号当日收盘
#盈利：盈利超过 20 %
#不亏，不盈利
def countWinFail( afterData, inprice=0.0, maxfailprice =0.0   ):
    print 'in function countWinFail:', inprice, maxfailprice 
    ret =[0,    0.0 ] # 1，失败  2，中性； 3，盈利
    lastRow= ''
    for index, row in afterData.iterrows():
        lastRow = row
        if(row.low<=maxfailprice):
            rate = (maxfailprice - inprice)*100 /inprice
            ret=[1, rate ]
            return ret
        pass

        if(row.close<=(maxfailprice+inprice)/2) :
            rate = (maxfailprice - inprice)*100 /inprice /2
            ret=[1, rate ]
            return ret
        pass

        if(row.high > 1.2* inprice ):
            ret =[3,20]
            return ret
    lastPrice =  lastRow.close                   
    ret = [2,  (lastPrice - inprice)*100 /inprice  ]                    
    return ret
    pass
        

#统计单个文件，返回统计结果， 统计结果是:[code, count, ok, fail, other]
def countfile(filename):

    pass    


#业务函数
def do():
    stocklist = ts.get_stock_basics()
    print stocklist 
    for index, row in stocklist.iterrows():
        print index

    #getAdata('600000')
    #dofile('600000.csv')
    #countfileWinFail('600000.csv'+'_2.csv')
    pass    

if __name__ == "__main__":
    print ('start "test.py"')
    do()
    #test()

#(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 

