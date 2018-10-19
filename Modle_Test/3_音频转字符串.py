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
test = client.asr(get_file_content('test.pcm'), 'pcm', 16000, {
    'dev_pid': 1536,
})

print(test['result'])


