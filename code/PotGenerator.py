#!/usr/bin/python
# -*- coding: utf-8 -*-   


#potdata make

from DataGenerator import * 

EMPTY_STRING = ''
EMPTY_FLOAT = 0.0
EMPTY_INT = 0
POT_TYPE_UP = 1
POT_TYPE_DOWN = -1 


#                       open   high  close    low   volume  price_change  p_change     ma5    ma10     ma20    v_ma5   v_ma10   v_ma20  turnover
# date
# 2019-03-04 15:00:00  24.09  24.15  24.15  24.09  2716.00          0.06      0.25  24.118  24.249  24.4245  4203.37  3324.05  3153.88      0.03


########################################################################
class VtMinBarData(object):
    datetime = EMPTY_STRING
    date = EMPTY_STRING                # 日期 20151009
    time = EMPTY_STRING
    endtime = EMPTY_STRING
    open = EMPTY_FLOAT
    close = EMPTY_FLOAT
    low = EMPTY_FLOAT
    high = EMPTY_FLOAT
    volume = EMPTY_FLOAT
    price_change = EMPTY_FLOAT      
    datatype = 'minbar'   

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(VtMinBarData, self).__init__(  )
        self.datetime = EMPTY_STRING
        self.date = EMPTY_STRING                # 日期 20151009
        self.time = EMPTY_STRING
        self.endtime = EMPTY_STRING
        self.open = EMPTY_FLOAT
        self.close = EMPTY_FLOAT
        self.low = EMPTY_FLOAT
        self.high = EMPTY_FLOAT
        self.volume = EMPTY_FLOAT
        self.price_change = EMPTY_FLOAT      
        self.datatype = 'minbar'


########################################################################
class VtPotData(object):
   
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(VtPotData, self).__init__(  )
        self.vtSymbol = EMPTY_STRING
        self.datetime = EMPTY_STRING
        self.date = EMPTY_STRING                # 日期 20151009
        self.time = EMPTY_STRING
        self.endtime = EMPTY_STRING
        self.open = EMPTY_FLOAT
        self.close = EMPTY_FLOAT
        self.minclose = EMPTY_FLOAT
        self.volume = EMPTY_FLOAT
        self.dim = EMPTY_FLOAT
        self.tickcount = EMPTY_INT
        self.datatype = 'pot'



########################################################################
class PotGenerator(DataGenerator):
    """
    POT数据生成器类
    需要 setting["potsize"]
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(PotGenerator, self).__init__(  )
        self.oneData = VtPotData() 
        self.dataSet =[] 
        self.lastBar = None     
        self.PotSize = 0   

    #----------------------------------------------------------------------
    def clearTmepData(self):
        self.oneData = VtPotData() 
        self.dataSet =[] 
        self.lastBar = None
        pass


#                       open   high  close    low   volume  price_change  p_change     ma5    ma10     ma20    v_ma5   v_ma10   v_ma20  turnover
# date
# 2019-03-04 15:00:00  24.09  24.15  24.15  24.09  2716.00          0.06      0.25  24.118  24.249  24.4245  4203.37  3324.05  3153.88      0.03

    def updateBar(self, bar):  #updata a k data
        self.PotSize = bar.close * 0.00618*2
        
        # print 'dataSet len :',  len( self.dataSet )

        #bar  is  VtMinBarData
        if( self.oneData.tickcount ==  EMPTY_INT ): 
            self.oneData.datetime = bar.datetime
            self.oneData.time = bar.time
            self.oneData.endtime = bar.time
            self.oneData.open = bar.open
            self.oneData.close = bar.high
            self.oneData.minclose = bar.close
            self.oneData.volume = bar.volume
            self.oneData.type = POT_TYPE_UP
            self.oneData.dim = 0
            self.oneData.tickcount = 1  
            self.datatype = 'pot'
            self.lastBar = bar
            self.oneData.date  = bar.date
            self.dataSet.append( self.oneData )
            #self.generate( )
            return           
            pass    

        if( self.oneData.type == 1 and bar.high> self.oneData.close  ):
            self.oneData.close = bar.high
        if( self.oneData.type == -1 and bar.low< self.oneData.close  ):
            self.oneData.close = bar.low

        if( self.oneData.type == 1  ):
            backDim_temp = ( self.oneData.close - bar.low ) * self.oneData.type

        if( self.oneData.type == -1  ):
            backDim_temp = ( self.oneData.close - bar.high ) * self.oneData.type
 
        # debug
        # print '----------------------------------------------'
        # print 'type, open, close,newpirce,dim, backdim ', self.oneData.type, self.oneData.open, self.oneData.close, bar.close, self.oneData.dim, backDim_temp
        # print '----------------------------------------------'


        if( backDim_temp >=  self.PotSize ):   #形成新的点

           
            if( bar.high > self.oneData.close and self.oneData.type == POT_TYPE_UP ):
                self.oneData.close = bar.high
                self.oneData.minclose = bar.close
                self.oneData.dim = self.oneData.close - self.oneData.open      
                self.oneData.time = bar.time

            if( bar.low < self.oneData.close and self.oneData.type == POT_TYPE_DOWN ):
                self.oneData.close =  bar.low
                self.oneData.minclose = bar.close
                self.oneData.dim = self.oneData.close - self.oneData.open     
                self.oneData.time = bar.time

            lastType = self.oneData.type
            lastclose = self.oneData.close

            #self.oneData =   VtPotData() 
            # newPot = copy.deepcopy( self.oneData )
            # self.dataSet.append( newPot )
 
            self.oneData = VtPotData()
            self.oneData.datetime = bar.datetime
            self.oneData.time = bar.time
            self.oneData.endtime = bar.time
            self.oneData.type = lastType*(-1)
            self.oneData.open = lastclose
            if( self.oneData.type == 1 ):       
                self.oneData.close = bar.high 
            else:
                self.oneData.close = bar.low                 
            self.oneData.volume = bar.volume
            self.oneData.minclose = bar.close
            self.oneData.dim = (self.oneData.close - self.oneData.open)   #*self.oneData.type
            self.oneData.tickcount = 1  
            self.datatype = 'pot'
            self.lastBar = bar
            self.oneData.date  = bar.date
            self.dataSet.append( self.oneData )    
            self.generate( )    
            pass
        else:  #更新当前点

            self.oneData.endtime = bar.time
            if( bar.high >= self.oneData.close and self.oneData.type == POT_TYPE_UP ):
                self.oneData.close = bar.high
                self.oneData.minclose = bar.close
                self.oneData.dim = self.oneData.close - self.oneData.open      
                self.oneData.time = bar.time

            if( bar.low <= self.oneData.close and self.oneData.type == POT_TYPE_DOWN ):
                self.oneData.close =  bar.low
                self.oneData.minclose = bar.close
                self.oneData.dim = self.oneData.close - self.oneData.open     
                self.oneData.time = bar.time

            self.oneData.volume = self.oneData.volume + bar.volume
            self.oneData.tickcount = self.oneData.tickcount + 1  
            self.lastBar = bar               
            pass            

        # 缓存 bar
        self.lastBar = bar
        pass

    #----------------------------------------------------------------------
    def generate(self, lastData = False):
        """手动强制立即完成K线合成"""
        if( lastData == True ):
            self.onDataGen( self.oneData )  
        else:
            if( len(self.dataSet) >=2 ):
                self.onDataGen( self.dataSet[-2] )   #self.oneData
                overPot = self.dataSet[-2]
                #debug
                # print '----------------------------------------------'
                # print 'potsize:', self.PotSize
                # print 'type,close, ,dim  ', overPot.type, overPot.open, overPot.close , overPot.dim 
                # print '----------------------------------------------'
            pass   