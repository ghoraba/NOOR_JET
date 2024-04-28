#!/usr/bin/env python

import urllib2
from pydub import AudioSegment
from pydub.playback import play
import os


def check_network():
    try:
        urllib2.urlopen('https://www.google.com', timeout=10)
        
        sound = AudioSegment.from_wav(os.path.join(os.path.dirname(os.path.abspath(__file__)),"success.wav"))
        play(sound)
        print("success")
    except urllib2.URLError as err: 
        sound = AudioSegment.from_wav(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fail.wav"))
        play(sound)
        print("fail")

check_network()
