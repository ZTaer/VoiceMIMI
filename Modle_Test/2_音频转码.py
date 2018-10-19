#!/usr/bin/python3
#-*- coding:utf-8 -*-

import os

if __name__=="__main__":
    ffmpegRoad = 'set path=%path%;'+os.getcwd()+os.sep+'ffmpeg\\bin'+';'
    # os.system('第一条命令 && 第二条命令')多条命令执行方式
    os.system("%s &&  ffmpeg -y  -i %sMCF_voice.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %sMCF_voice.pcm " % (ffmpegRoad,os.getcwd()+'\\',os.getcwd()+'\\'))