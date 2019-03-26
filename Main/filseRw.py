#!/usr/bin/python3
#-*- coding:utf-8 -*-

from vTplays import translation
import os

#   写入文件
#   接受文件路径，语种
def wFilseName( road,langCn="" ): # 取出路径文件名称,并且去除后缀名
    nameCut = (os.path.basename(road)).split('.')
    return os.path.dirname(road)+os.sep+nameCut[0]+"_"+langCn+".txt"

def  writeStr( road,lang ): # 翻译内容写到文件中
    with open(road, "rt+", encoding="utf-8") as rFilse, open( wFilseName(road,lang[2]),"wt+",encoding="utf-8" ) as wFilse:
        rFilse.seek(0)
        endStr = translation( rFilse.read().replace('\n','&'),lang[1] ) # 百度翻译遇到‘\n’会停止翻译
        endStr = endStr.replace('&','\n') # 恢复字符串
        wFilse.write(endStr)

