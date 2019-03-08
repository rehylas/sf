#!/usr/bin/python
# -*- coding: utf-8 -*-   


########################################################################
class DataGenerator(object):
    """
    数据生成器基类
    需要 setting["potsize"]
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(DataGenerator, self).__init__(  )
        self.dataSet =[] 

    def getDataset(self):
        return  self.dataSet       

    def onDataGen( self, oneData ):
        #do some on data
        print 'pot info:', oneData
        pass

