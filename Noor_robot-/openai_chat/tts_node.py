#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gtts import gTTS
import os

def tts_callback(data):
    # rospy.loginfo("Received: " + data.data)

    # Perform text-to-speech synthesis
    tts = gTTS(text=data.data, lang='en', slow=False)
    tts.save("/tmp/response.mp3")
    os.system("mpg123 /tmp/response.mp3")

def tts_node():
    rospy.init_node('tts_node')
    rospy.loginfo("TTS node started")

    # Create a subscriber for the STT topic
    rospy.Subscriber('/tts_topic', String, tts_callback)

    rospy.spin()

if __name__ == '__main__':
    tts_node()

