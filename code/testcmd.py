# -*- coding:utf8 -*-

import cmd   
import sfdatalib  

version = '1.0.0'

class MyCmd(cmd.Cmd):  # Cmd是以面向对象设计的
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = 'welcome to stock &f data tool!'  # 定义启动时打印的信息python
        self.prompt = '>'  # 定义提示符
        print "cmd:"
        print "init stock"
        print "init future"
        print "init f"

    def do_version(self, arg):  # 定义'version'命令
        '''
            version : show the version
        '''
        print version

    def help_version(self):  # 定义'version'命令的帮助信息
        print 'show the version'   

    def help_name(self):  # 定义'name'命令的帮助信息
        print 'show the name'   

    def help_quit(self):  # 定义'quit'命令的帮助信息
        print "syntax: quit -- terminatesthe application"                  

    def do_name(self, arg):  # 定义'name'命令
        print 
        print 'do name , arg is:', type(arg)

    def do_init(self, arg):
        if( arg == "stock"):
            print "init stock list"
            sfdatalib.loadsaveStockList()
            return 

        if( arg == "future" or arg == "f"  ):
            print "init future list"
            sfdatalib.saveFuturelist2db()
            return 
        print "error arg:", arg
        pass        


    def do_quit(self, arg):  #定义退出命令'quit'，退出程序
        return True  # 函数返回True，则干净退出程序
 

    do_q = do_quit  # 定义'quit'命令的别名'q'


if __name__ == '__main__':
    myCmd = MyCmd()  # 创建一个MyCmd的实例
    myCmd.cmdloop()  # 启动cmd循环