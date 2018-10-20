#!/usr/bin/python3
#-*- coding:utf-8 -*-
import subprocess
import os

def test(files):
    ffmpegroad = os.getcwd()+os.sep+'ffmpeg'+os.sep+'bin;'
    setpath = "set path=%path%;{}".format(ffmpegroad)
    ffmpegset = "ffmpeg -y  -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %sMCF_voice.pcm" % (os.getcwd()+os.sep+files,os.getcwd()+os.sep )
    cmd = "%s &&  %s" % ( setpath,ffmpegset  )
    a = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    a.wait() # 等待子程序( cmd命令 )运行结束,才开始执行新的命令

if __name__=="__main__":
    test('MCF_voice.wav')


