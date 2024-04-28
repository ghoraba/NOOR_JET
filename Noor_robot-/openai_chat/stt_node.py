#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#########################################################################################
#                                    _                                                  #
#      __ _ ___ _ __   ___  ___  ___| |__                                               #
#     / _` / __| '_ \ / _ \/ _ \/ __| '_ \                                              #
#    | (_| \__ \ |_) |  __/  __/ (__| | | |                                             #
#     \__, |___/ .__/ \___|\___|\___|_| |_|                                             #
#     |___/    |_|                                                                      #
#                                                                                       #
# ros package for speech recognition using Google Speech API                            #
# run using 'rosrun gspeech gspeech.py <your api key>'                                  #
# it creates and runs a node named gspeech                                              #
# the node gspeech publishes two topics- /speech and /confidence                        #
# the topic /speech contains the reconized speech string                                #
# the topic /confidence contains the confidence level in percentage of the recognization#
# the node gspeech registers services start and stop                                    #
# For dependencies use: pip install --upgrade google-cloud; sudo apt-get install sox    #
# For authentication do:    #
#                                                                                       #
# written by achuwilson                                                                 #
# revision by pexison,                                                                  #
# revision by slesinger - removing redundant code, updating to latest Google API         #
#                                                                                       #
# 30-06-2012 , 3.00pm                                                                   #
# achu@achuwilson.in                                                                    #
# 01-04-2015 , 11:00am                                                                  #
# pexison@gmail.com                                                                     #
# 17-08-2017                                                                            #
# slesinger@gmail.com                                                                   #
#########################################################################################

import json, shlex, socket, subprocess, sys, threading
import roslib; roslib.load_manifest('gspeech')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8
import shlex,subprocess,os,io
from std_srvs.srv import *
from google.cloud import speech
import speech_recognition as sr
import pyttsx

#import google.cloud.texttospeech as tts
import os
import requests
from playsound import playsound
credential_path = "/home/jetson/Desktop/Jun22/noor2-344811-28bdfdce8e66.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
url='https://b682-196-132-132-185.ngrok.io/'

#credentials = service_account.Credentials.from_service_account_file("/home/ahmed/noor2-344811-28bdfdce8e66.json")

#GOOGLE_APPLICATION_CREDENTIALS="/home/ahmed/noor2-344811-28bdfdce8e66.json"

class GSpeech(object):
  """Speech Recogniser using Google Speech API"""

  def __init__(self):
    """Constructor"""
    # configure system commands
    self.sox_cmd = "sox -r 16000 -c 1 -t alsa default /home/jetson/nourrobot_ws/src/Noor_robot-/openai_chat/recording.flac silence 1 0.1 1% 1 1.5 2%"
    self.sox_args = shlex.split(self.sox_cmd)
    self.client = speech.SpeechClient()
    # start ROS node
    rospy.init_node('gspeech')
    # configure ROS settings
    rospy.on_shutdown(self.shutdown)
    self.pub_speech = rospy.Publisher('~speech', String, queue_size=10)
    self.pub_confidence = rospy.Publisher('~confidence', Int8, queue_size=10)
    self.srv_start = rospy.Service('~start', Empty, self.start)
    self.srv_stop = rospy.Service('~stop', Empty, self.stop)

    self.stt_pub = rospy.Publisher('stt_topic', String, queue_size=10)
    # run speech recognition
    self.started = True
    self.recog_thread = threading.Thread(target=self.do_recognition, args=())
    self.recog_thread.start()
    playsound('/home/jetson/nourrobot_ws/src/Noor_robot-/openai_chat/wait_mess.mp3')

  def start(self, req):
    """Start speech recognition"""
    if not self.started:
      self.started = True
      if not self.recog_thread.is_alive():
        self.recog_thread = threading.Thread(
          target=self.do_recognition, args=()
        )
        self.recog_thread.start()
      rospy.loginfo("gspeech recognizer started")
    else:
      rospy.loginfo("gspeech is already running")
    return EmptyResponse()

  def stop(self, req):
    """Stop speech recognition"""
    if self.started:
        self.started = False
        if self.recog_thread.is_alive():
            self.recog_thread.join()
        rospy.loginfo("gspeech recognizer stopped")
    else:
        rospy.loginfo("gspeech is already stopped")
    return EmptyResponse()

  def shutdown(self):
    """Stop all system process before killing node"""
    self.started = False
    if self.recog_thread.is_alive():
      self.recog_thread.join()
    self.srv_start.shutdown()
    self.srv_stop.shutdown()
    os.remove("/home/jetson/nourrobot_ws/src/Noor_robot-/openai_chat/recording.flac")

  def is_speaker_busy(self):
    engine = pyttsx.init()
    try:
        # engine.say("")
        engine.runAndWait()
        return False
    except pyttsx.EngineError:
        return True
    
  def do_recognition(self):
    """Do speech recognition"""
    while self.started:
      if(not self.is_speaker_busy()):
        sox_p = subprocess.call(self.sox_args)
        with sr.AudioFile("//home/jetson/nourrobot_ws/src/Noor_robot-/openai_chat/recording.flac") as audio_file:
            #content = audio_file.read()
            try:
                
                    r = sr.Recognizer()
                    audio = r.record(audio_file)
                    text = r.recognize_google(audio, language='en')
                    # audio = speech.RecognitionAudio(content=content)
                    print(text)
                    self.stt_pub.publish(text)
            except Exception as err:
                print(err)

                playsound('/home/jetson/nourrobot_ws/src/Noor_robot-/openai_chat/get_it.mp3')

    #   config = speech.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    #     sample_rate_hertz=16000,
    #     language_code='ar-EG')

    #   response = self.client.recognize(config=config, audio=audio)
    #   url='https://cff9-156-207-198-129.ngrok.io/model/parse'
    #   print_sentences(response,url)
    #   playsound('en-US.wav')



# end of GSpeech class



def print_sentences(response,url):
    f = open("response.txt", "a")
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print(transcript)
        print(confidence)
        payload={"text":transcript}
        headers = {'Content-Type': "application/json",}
        x=requests.post(url,data=json.dumps(payload), headers=headers)
        response=json.loads(x.content)
        print(response['intent']['name']) 
        f.write(str(response['text']) + '\n')
        f.write(str(response['intent']) + '\n')
        #text_to_wav('en-US',response['intent']['name'])
    f.close()
'''
def text_to_wav(voice_name,text):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = "{language_code}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print('Generated speech saved to "{filename}"')
'''


def is_connected():
  """Check if connected to Internet"""
  try:
    # check if DNS can resolve hostname
    remote_host = socket.gethostbyname("www.google.com")
    # check if host is reachable
    s = socket.create_connection(address=(remote_host, 80), timeout=5)
    return True
  except:
    pass
  return False


def usage():
  """Print Usage"""
  print("Usage:")
  print("rosrun gspeech gspeech.py <API_KEY>")


def main():
  if not is_connected():
    sys.exit("No Internet connection available")
  speech = GSpeech()
  rospy.spin()


if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    pass
  except KeyboardInterrupt:
    sys.exit(0)
