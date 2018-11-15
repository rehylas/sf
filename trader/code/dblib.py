

#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import time
import sys
import logging


conn =None
db = None
tb_trader = None
DB_IP = '127.0.0.1'

def init():
    global conn
    global db
    global tb_trader
    conn = MongoClient(DB_IP, 27017)
    db = conn.market
    print db
    tb_trader = db.trader

    pass


def test():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.market
    print db
    tb_trader = db.trader


    for i in tb_trader.find():
        print(i)

    print tb_trader
    ret = tb_trader.insert( {  "sys":"ru_tk","orderid":"9801", "ctpid":123456, "status":0, "insertDt":"2018-05-14", "name":"ru1901","type":"buy","price":2050,"amount":1  })
    print 'ret:',ret

 
 
def insertTrader( trader ):
    tb_trader.insert( trader )
    pass 

def getTrader_one():
    dataList =[]
    for rec in tb_trader.find({"status":0}).limit(1):
        dataList.append( rec )
    #print dataList
    return dataList
    pass

def updateTrader(orderid, status, ctpid = None):
    setData = {"status":status}
    if( ctpid != None ):
        setData = {"status":status, "ctpid":ctpid}
    tb_trader.update({"orderid":orderid},{ "$set":{"status":status} } )
 
    pass

def main():
    init()
    updateTrader("9802",9)
    print getTrader_one()
    trader = {  "sys":"ru_tk","orderid":"9801", "ctpid":123456, "status":0, "insertDt":"2018-05-14", "name":"ru1901","type":"buy","price":2050,"amount":1  }
    insertTrader( trader )
    pass

    
if __name__ == '__main__':
    logging.info("This is a info log:", sys.argv)
    main()
    #test()
    time.sleep(5)


