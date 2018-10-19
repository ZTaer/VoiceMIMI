#!/usr/bin/python3
#-*- coding:utf-8 -*-

import os
import wave
import numpy as np

f = open("TEST2.wav",'rb')
f.seek(0)
f.read(44)
data = np.fromfile(f, dtype=np.int16)
data.tofile("TEST2.pcm")



