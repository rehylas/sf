#coding=utf-8


import os
path='d:/temp'
import datetime
import time 
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

def getDis(path):
    dirs = []
    for dirpath,dirnames,filenames in os.walk(path): 
        dirs = dirnames
        break 
 
    return dirs    

def getFiles(path):
    files = []
    for dirpath,dirnames,filenames in os.walk(path): 
        files = filenames
        break 
    
    return files        

def getMainInfo(  filelistInfo ):
    info =['code','filename',0,'type' ]
    if( len( filelistInfo ) == 0 ):
        return None
    info =  filelistInfo[0]
    for temp in filelistInfo:
        if( temp[2] >= info[2] ):
            info = temp 
    return info
      

def getAllMainSymbols(rootPath,  doFun ):   #doFun = doOneMainSymbol
    today = time.strftime("%Y%m%d", time.localtime()) 
    dirs = getDis( rootPath )
   
    for symbolDir in dirs :
        print symbolDir
        #
        insertSymbol2db( symbolDir )
        files = getFiles( rootPath +'/'+ symbolDir+'/'+today )
        
        InfoList = []
        for oneFile in files:
            #print oneFile
            filePath = rootPath +'/'+symbolDir+'/'+today+'/'+oneFile
            fileSize = os.path.getsize( filePath )
            code = oneFile[0:-13]
            sType = oneFile[0:-15]
            month = oneFile[-15:-13]
            #a09_20181112.cvs  ru01_20181112.cvs
            InfoList.append(  [code,filePath,fileSize,sType, month] )
        pass

        mainSymbols = getMainInfo( InfoList )
        doFun( mainSymbols )
        pass        
    pass

def doOneMainSymbol(  info ):
    if(info == None ):
        return
    code = info[3].upper()+'0'
    print info
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_info = client.market.f_info
    f_info.update(   {"code": code },{"$set":{ "maininfo": info }}   )    


    pass 

def insertSymbol2db( symbol ):
    code = symbol.upper() +'0'
    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    try:
        f_info = client.market.f_info
        f_info.insert(   {"code": code } )   
    except Exception, e:
        print e
        pass
     
    pass

def test():
    # filePath ='d:/temp/dd.py'
    # print getDis( path )
    # print getFiles( path )
    # print os.path.getsize( filePath )

    client = MongoClient( DB_INFO["IP"], DB_INFO["PORT"] )
    f_info = client.market.f_info
    f_info.update(   {"code":"ZN0"},{"$set":{ "maininfo":"['zn01', 'D:/tikfile/zn/20181119/zn01_20181119.csv', 2282029L, 'zn', '01']" }}   )    


def main():
    pass


if __name__ == '__main__':
    # main()
    #test()
    # today = time.strftime("%Y%m%d", time.localtime()) 
    # print today 

    #D:\tikfile
    getAllMainSymbols('D:/tikfile',  doOneMainSymbol )    #doFun = doOneMainSymbol

 
    pass
