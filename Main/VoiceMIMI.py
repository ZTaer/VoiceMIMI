#/usr/bin/python3
#-*- coding:utf-8 -*-

from vTplays import *

#   #   主体思路总结
#   交互界面控制参数:
#   while循环:
#       选择功能(q接受程序):
#           1.语音翻译( 目前只支持英语 )
#           2.文字翻译
#           3.播报文字
#       如果检测到1( 调用vTplay函数(接受2个参数,times录制时间,lg='en'要求翻译的语言种类( 默认为英语 )))

if __name__=="__main__":
    while True:
        print("")
        print("1.语音翻译( 目前只支持英语 )")
        print("2.文字翻译( 目前只支持中文-英文翻译 )")
        print("3.播报文字( 目前只支持中文-英文发音 )")
        choose = input('选择: ')
        if choose == '1':
            times = int(input('请输入录音时间: '))
            s = vTplay(times)
            s.wait()
        elif choose == 'q':
            print("谢谢使用此程序,下个版本会变得更好!")
            break

