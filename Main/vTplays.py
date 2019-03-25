#!/usr/bin/python3
#-*- coding:utf-8 -*-

import pyaudio
import wave
import os
from aip import AipSpeech
import subprocess

import http.client
import hashlib
import json
import urllib
import random

# 百度接口密钥
""" 你的 APPID AK SK """
APP_ID = '14452080'
API_KEY = 'we2bjLhUKwm4edxb58E9jmNB'
SECRET_KEY = 'N7PLBz1abgkDTjMuPSz7dtmfr8HYahy5'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#   语音识别翻译主要步骤:
#           1. 录制音频
#           2. wav转换为pcm格式音频
#           3. 语音识别,音频识别为字符串
#           4. 字符串翻译为英语
#           5. 语音合成,将字符串转为wav音频
#           6. 后台播放音频文件
#
#   #   核心逻辑: vTplay()函数思路
#       调用vTplay函数(接受2个参数,times录制时间,lg='en'要求翻译的语言种类( 默认为英语 ))
#           调用recodeVoice( times , lg='auto' )函数开始录音,返回录音文件MCF_voice.pcm( 转码在函数内部完成! )
#           调用voiceTo_str( 'MCF_voice.pcm' )函数进行语音识别，返回识别后的字符串MCF_voiceStr变量
#           调用translation( MCF_voiceStr,lg='en' )函数进行翻译,返回翻译后的字符串translationStr变量
#           调用strTo_voice( translationStr )函数进行语音合成,返回语音文件Play_voice.wav
#           直接使用play_wav( Play_voice )在后台播放音频

def vTplay(times=5 , lg='en'):
    recodeVoice(times)
    MCF_voiceStr = voiceTo_str('MCF_voice.pcm')
    translationStr = translation(MCF_voiceStr, lg)
    print(MCF_voiceStr, "--", translationStr)
    strTo_voice(translationStr)
    play_wav("Play_voice.wav") # 播放音频

def recodeVoice(times): # 录音函数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = times
    def rec(file_name):
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("开始录音(%s秒)" % times)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("录音结束!!")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    rec('MCF_voice.wav')
    wav_to_pcm('MCF_voice.wav')

def wav_to_pcm(files): # 音频转换格式
    ffmpegroad = os.getcwd()+os.sep+'ffmpeg'+os.sep+'bin;'
    setpath = "set path=%path%;{}".format(ffmpegroad)
    ffmpegset = "ffmpeg -y  -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %sMCF_voice.pcm" % (os.getcwd()+os.sep+files,os.getcwd()+os.sep )
    cmd = "%s &&  %s" % ( setpath,ffmpegset  )
    a = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    a.wait() # 等待子程序( cmd命令 )运行结束,才开始执行新的命令

def voiceTo_str( voiceFiles ): # 语音识别,音频识别成字符串
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 识别本地文件
    test = client.asr(get_file_content(voiceFiles), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    MCF_voiceStr = str(test['result'])
    return MCF_voiceStr

def translation( content , lg='en' ): # 字符串翻译
    appid = '20181017000220898'
    secretKey = 'Gj8WRuv_oa_p5WqNbzBI'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'auto'  # 源语言
    toLang = lg  # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
    return str(dst)

def strTo_voice( translationStr ): # 语音合成,字符串转为音频
    result = client.synthesis(translationStr, 'zh', 1, {
        'spd': 4, 'pit': 6, 'vol': 4, 'per': 4,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):  # 判断是否返回是一个字典类型
        with open('Play_voice.wav', 'wb') as f:
            f.write(result)

def play_wav( files ): # 在后台播放wav音频
    ffmpegroad = os.getcwd() + os.sep + 'ffmpeg' + os.sep + 'bin;'
    setpath = "set path=%path%;{}".format(ffmpegroad)
    ffmpegset = "ffplay -nodisp -autoexit {}".format(os.getcwd() + os.sep + files) # ffplay 无弹窗播放 播放完退出 播放文件
    cmd = "%s &&  %s" % (setpath, ffmpegset) # 设置ffmpeg环境变量与播放文件命连续执行( 因为环境变量只能临时设置 )
    a = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# 出自oo7博客地址:OO7.fun