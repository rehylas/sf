# -*- coding:utf8 -*-
# @Date    : 2018-10-01
# @Author  : hylas
"""
本程序是数据 sf 数据整理的客户端工具，也可以做为服务用
实现：初始化数据，下载日k数据，生成zf, signal等扩展数据

"""

import sys
import cmd   
import sfdatalib  
import time 

version = '1.0.0'

# SfClientCmd类  继承命令行交互类 cmd.Cmd ，执行对应业务
class SfClientCmd(cmd.Cmd):  
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = 'welcome to stock & f data tool!'  # 定义启动时打印的信息python
        self.prompt = '>'  # 定义提示符
        print "cmd:"
        print "init stock , init future , init f"
        print "init stockhisk , init fhisk  "
        print "loadsave future/fhisk/stock/stockkhis   "
        print "makezf future  "
        print "signal  futurezf/fzf"
        print "minup bak/2tdx/monitor"

    # 定义version 命令，显示版本号
    def do_version(self, arg):  # 定义'version'命令
        '''
            version : show the version
        '''
        print version

    # 定义 帮助 name
    def help_name(self):  # 定义'name'命令的帮助信息
        print 'show the name'   

    # 定义 帮助 退出
    def help_quit(self):  # 定义'quit'命令的帮助信息
        print "syntax: quit -- terminatesthe application"                  

    # 定义 name 命令
    def do_name(self, arg):  # 定义'name'命令
        print 
        print 'do name , arg is:', type(arg)

     
    # 定义 init 命令, 初始化数据
    # arg:
    #     stock          初始化股票
    #     stockhisk      初始化股票历史k线
    #     future         初始化期货
    def do_init(self, arg):
        if( arg == "stock"):
            print "init stock list"
            sfdatalib.loadsaveStockList()
            print "ok"
            return 
        if( arg == "stockhisk"):
            print "init stock his k data  "
            sfdatalib.loadsaveStockList()
            print "ok"
            return             

        if( arg == "future" or arg == "f"  ):
            print "init future list"
            sfdatalib.saveFuturelist2db()
            print "ok"
            return 

 

        print "error arg:", arg
        print "----------------------------------------"
        print "example:"
        print "init stock , init future , init f"
        print "init stockhisk , init fhisk  "
        print "loadsave future/fhisk/stock/stockkhis   "
        print "makezf future  "
        print "signal  futurezf/fzf"
        print "----------------------------------------"        
        pass   

    # 定义 loadsave 命令, 下载数据入库
    # arg:
    #     stock/s           下载股票
    #     stockhisk         下载股票历史
    #     future/f          下载期货
    #     fhisk             下载期货历史
    def do_loadsave(self, arg):
        if( arg == "future" or arg == "f" ):
            print "loadsave future now k"
            sfdatalib.loadsaveFutureKNow2db_all() 
            print "ok"
            return 

        if( arg == "fhisk"):
            print "loadsave fhisk : loadsave future his k data  "
            sfdatalib.loadsaveFutureKHis2db_all()
            print "ok"
            return              

        if( arg == "stock" or arg == "s" ):
            print "loadsave  stock now k"
            sfdatalib.loadsaveStockK2db_all() 
            print "ok"
            return 

        if( arg == "stockhisk" or arg == "shisk" ):
            print "loadsave  stock his k"
            sfdatalib.loadsaveStockKHis2db_all() 
            print "ok"
            return             

        print "error arg:", arg
        print "----------------------------------------"
        print "example:"
        print "loadsave future , loadsave stock, loadsave stockhisk, loadsave shisk "  
        print "----------------------------------------"             

        pass 

    # 定义 makezf 命令, 生成振幅数据  
    # arg:
    #     fhisk              期货 
    def do_makezf(self, arg):
        if( arg == "future" or arg == "f" ):
            print "loadsave future now k"
            sfdatalib.makeFuturezf20_all() 
            print "ok"
            return 

        print "error arg:", arg
        print "----------------------------------------"
        print "example:"
        print "makezf future  "  
        print "----------------------------------------"             

        pass 

    # 定义 signal 命令, 生成振幅数据  
    # arg:
    #     fzf/futurezf              期货 
    def do_signal(self, arg):
        if( arg == "futurezf" or arg == "fzf" ):
            print "signal futurezf now k"
            sfdatalib.signalFutureZf() 
            print "ok"
            return 

        print "error arg:", arg
        print "----------------------------------------"
        print "example:"
        print "signal futurezf  "  
        print "signal fzf  "  
        print "----------------------------------------"             

        pass 

    # 定义 minup 命令, minup 相关业务均用此命令  
    # arg:
    #     bak/2tdx/monitor        
    #     bak  备份今天的自动选股
    #     2tdx 生成同名的通达信自选股
    #     monitor 把数据导入到数据库， 以便其它子系统可以用       
    def do_minup(self, arg): 
        if( arg == "bak"  ):
            print "minup bak"
            sfdatalib.minupBak() 
            print "ok"
            return 
        if( arg == "2tdx"  ):
            print "minup 2tdx"
            sfdatalib.minup2tdx() 
            print "ok"
            return      
        if( arg == "monitor"  ):
            print "minup monitor"
            sfdatalib.minupMonitor() 
            print "ok"
            return                      

        print "error arg:", arg
        print "----------------------------------------"
        print "example:"
        print "minup bak  "  
        print "minup 2tdx " 
        print "minup monitor " 

        print "----------------------------------------"             

        pass 

   
 
    # 定义 quit/q 命令, 退出  
    # arg:
    #     null                
    def do_quit(self, arg):  #定义退出命令'quit'，退出程序
        return True  # 函数返回True，则干净退出程序
 

    do_q = do_quit  # 定义'quit'命令的别名'q'



# 启动服务程序 
#16:00 开始 ， 执行下载future k ,   makefuturek   , signal k
def runserver():
    while( True ):
        time.sleep( 5 )
        print '.',
        now = time.localtime( time.time() )   
        #print now.tm_hour ,tm_min
        if( now.tm_hour == 16 and now.tm_min == 2 ):
            print "-------------------------------------"
            print "do  future data "
            sfdatalib.loadsaveFutureKNow2db_all()
            sfdatalib.makeFuturezf20_all()
            sfdatalib.signalFutureZf()

            # 股票
            print "-------------------------------------"
            print "do  s data "            
            sfdatalib.loadsaveStockK2db_all()

            print "-------------------------------------"
            time.sleep( 60 )
    pass

#主流程 main 
# 带参数  -d 进入服务模式
# 不带参数 ，进入命令模式
def main(argv):
    if( len( argv ) == 1 ):
        myCmd = SfClientCmd()  # 创建一个MyCmd的实例
        myCmd.cmdloop()  # 启动cmd循环
        exit()

    if( argv[1] == '-d' ):
        print 'run server'
        runserver()
        exit()    
    print argv[1], ' error '
    print 'help'    
    pass


if __name__ == '__main__':
    main( sys.argv )
    pass
 