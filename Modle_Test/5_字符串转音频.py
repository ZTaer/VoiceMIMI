#!/usr/bin/python3
#-*- coding:utf-8 -*-
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '14452080'
API_KEY = 'we2bjLhUKwm4edxb58E9jmNB'
SECRET_KEY = 'N7PLBz1abgkDTjMuPSz7dtmfr8HYahy5'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


#   #   文字转语音
def str_to_voice():
    result  = client.synthesis("everyone is really good", 'zh', 1, {
       'spd': 5,'pit':6, 'vol': 4, 'per':4,
    })
    print(result)
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict): #  判断是否返回是一个字典类型
        with open('auido.wav', 'wb') as f:
            f.write(result)

if __name__ == "__main__":
    str_to_voice()
