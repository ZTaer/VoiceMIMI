#/usr/bin/python3
#-*- coding:utf-8 -*-

from vTplays import *

#   #   主体思路总结
#   while循环:
#       选择功能(q接受程序):
#           1.语音翻译( 目前只支持英语 )
#           2.文字翻译
#           3.播报文字
#       如果检测到1( 调用vTplay函数(接受2个参数,times录制时间,lg='en'要求翻译的语言种类( 默认为英语 )))

if __name__=="__main__":
    while True:
        print("VoiceMIMIv2.0 --- 20190325")
        print("1.语音翻译( 支持: 中文 -> 英语 )")
        print("2.文字翻译( 支持:)")
        print("3.播报文字( 支持:中文-英文 )")
        choose = input('选择: ')
        if choose == '1':
            times = int(input('请输入录音时间: '))
            vTplay(times)
        elif choose == 'q':
            print("谢谢使用此程序,下个版本会变得更好!")
            break

