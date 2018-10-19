#/usr/bin/python3
#-*- coding:utf-8 -*-

from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '14452080'
API_KEY = 'we2bjLhUKwm4edxb58E9jmNB'
SECRET_KEY = 'N7PLBz1abgkDTjMuPSz7dtmfr8HYahy5'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#   #   本地文件语音识别

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
test = client.asr(get_file_content('TEST2.wav'), 'wav', 16000, {
    'dev_pid': 1536,
})
print(test)

#   #   文字转语音

result  = client.synthesis("我只想说在坐的各位都是垃圾", 'en', 1, {
   'spd': 3,'pit':6, 'vol': 4, 'per':4,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)

