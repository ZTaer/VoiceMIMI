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

""" 你的 APPID AK SK """
APP_ID = '14452080'
API_KEY = 'we2bjLhUKwm4edxb58E9jmNB'
SECRET_KEY = 'N7PLBz1abgkDTjMuPSz7dtmfr8HYahy5'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#   #   #   功能: 录制中文语音，读出要求翻译后的语音( 存放在vTplays文件中 )
#   #   问题: 语音识别
#                   语音录制
#                       创建,recodeVoice()函数( 接受1个参数,times,控制录制时间 ),录制音频生成在当前目录"MCF_voice.wav"文件
#                   文件格式转换
#                       音频文件转为pcm格式通过ffmpeg,并且生成当前路径下文件为"MCF_voice.pcm"
#                   上传识别成字符串
#                       识别MCF_voice.pcm( 注意必须是pcm格式文件才识别 )
#                       创建语音识别voiceTo_str()函数(接受1个参数,voiceFiles,所需识别的文件名称路径)
#                       返回识别出的字符串MCF_voiceStr
#   #   问题: 字符串翻译
#                   创建translation( 接受2个参数，字符串MCF_voiceStr，要求翻译的语言 )
#                   翻译成要求语音字符串
#                   返回翻译后的字符串translationStr
#   #   问题: 语音合成
#                   创建strTo_voice(接受1个参数,将要翻译的字符串translationStr)
#                   语音合成
#                   返回语音文件Play_voice.wav
#   #   问题: 语音播放
#                   在后台播放语音合成的文件
def wav_to_pcm(files):
    ffmpegroad = os.getcwd()+os.sep+'ffmpeg'+os.sep+'bin;'
    setpath = "set path=%path%;{}".format(ffmpegroad)
    ffmpegset = "ffmpeg -y  -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %sMCF_voice.pcm" % (os.getcwd()+os.sep+files,os.getcwd()+os.sep )
    cmd = "%s &&  %s" % ( setpath,ffmpegset  )
    a = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    a.wait() # 等待子程序( cmd命令 )运行结束,才开始执行新的命令


def recodeVoice(times):
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



def voiceTo_str( voiceFiles ):
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 识别本地文件
    test = client.asr(get_file_content(voiceFiles), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    MCF_voiceStr = str(test['result'])
    return MCF_voiceStr

def translation( content , lg='en' ):
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

def strTo_voice( translationStr ):

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

#   #   核心逻辑: vTplay()函数思路
#       调用vTplay函数(接受2个参数,times录制时间,lg='en'要求翻译的语言种类( 默认为英语 ))
#           调用recodeVoice( times , lg='auto' )函数开始录音,返回录音文件MCF_voice.pcm( 转码在函数内部完成! )
#           调用voiceTo_str( 'MCF_voice.pcm' )函数进行语音识别，返回识别后的字符串MCF_voiceStr变量
#           调用translation( MCF_voiceStr,lg='en' )函数进行翻译,返回翻译后的字符串translationStr变量
#           调用strTo_voice( translationStr )函数进行语音合成,返回语音文件Play_voice.wav
#           直接使用os.system('Play_voice.wav')进行语音播放

def vTplay(times=5 , lg='en'):
    recodeVoice(times)
    MCF_voiceStr = voiceTo_str('MCF_voice.pcm')
    translationStr = translation(MCF_voiceStr, lg)
    print(MCF_voiceStr, "--", translationStr)
    strTo_voice(translationStr)
    play_wav("Play_voice.wav") # 播放音频
