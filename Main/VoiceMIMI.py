#/usr/bin/python3
#-*- coding:utf-8 -*-

from vTplays import *
from filseRw import *
#   #   主体思路总结
#   while循环:
#       选择功能(q接受程序):
#           1.语音翻译( 支持: 中文 -> 英语 )
#               a)请输入录音时间(默认为5秒)
#               提示: 开始录音
#               得出结果
#           2.文字翻译( 支持: 自动识别 -> 5个语种)
#               -> 0 - 文言文
#               -> 1 - 英语
#               -> 2 - 德语
#               -> 3 - 法语
#               -> 4 - 日语
#               -> 5 - 泰语
#               请选择翻译语种:
#                   a) 直接输入
#                        ?是否保存为文档(Y/N)
#                   b) 导入文件
#                        ?是否保存为文档(Y/N)
#           3.播报文字( 支持: 中文 - 英文 )
#               a) 直接输入
#                   提示: 开始播报
#               b) 导入文件
#                   提示: 开始播报
#       如果检测到1( 调用vTplay函数(接受2个参数,times录制时间,lg='en'要求翻译的语言种类( 默认为英语 )))

if __name__=="__main__":
    langEncode = [
        [0,"wyw","文言文"],
        [1,"en","英语"],
        [2,"de","德语"],
        [3,"fra","法语"],
        [4,"jp","日语"],
        [5,"th","泰语"]
    ]
    print("VoiceMIMIv2.0 --- 20190325")
    while True:
        print("1.语音翻译( 支持: 中文 -> 英语 )")
        print("2.文字翻译( 支持: 自动识别 -> 5个语种)")
        print("3.播报文字( 支持: 中文 - 英文,等待更新困死了 )")
        print("q.退出程序")
        choose = input('选择: ')
        if choose == '1':
            times = int(input('请输入录音时间(默认为5秒): '))
            vTplay(times)
        elif choose == '2':
            for lang in langEncode:
                print("-> %d - %s" % (lang[0],lang[2]))
            langNum = int(input("请选择翻译语种: "))
            print("状态: 自动识别 -> %s" % langEncode[langNum][2] )
            inputChosse = input("-> 1 - 直接输入\n-> 2 - 导入文件\n请选择输入方式: ")
            if inputChosse == '1':
                strContent = input("请输入: ")
                print(translation( strContent,langEncode[langNum][1] )+"\n")
            elif inputChosse == '2':
                fileRoad = input("请输入文档路径: ")
                writeStr( fileRoad,langEncode[langNum] )

        elif choose == 'q':
            print("谢谢使用此程序,下个版本会变得更好!\n作者博客: OO7.fun\n源码链接: https://github.com/ZTaer/VoiceMIMI")
            break