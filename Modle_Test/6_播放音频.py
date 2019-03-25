#!/usr/bin/python3
#-*- coding:utf-8 -*-
import os
import subprocess

def play_wav( files ): # 在后台播放wav音频
    ffmpegroad = os.getcwd() + os.sep + 'ffmpeg' + os.sep + 'bin;'
    setpath = "set path=%path%;{}".format(ffmpegroad) # 设置ffmpeg环境变量
    ffmpegset = "ffplay -nodisp -autoexit {}".format(os.getcwd() + os.sep + files) # ffplay 无弹窗播放 播放完退出 播放文件
    cmd = "%s &&  %s" % (setpath, ffmpegset) # 设置ffmpeg环境变量与播放文件命连续执行( 因为环境变量只能临时设置 )
    a = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    files = input("文件路径: ")
    play_wav(files)