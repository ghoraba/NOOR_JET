# Noor_robot-
# ROS Speech-to-Text (STT) and Text-to-Speech (TTS) Nodes

This ROS package contains three nodes that enable speech-to-text (STT) and text-to-speech (TTS) functionality using the Google Speech Recognition service and the OpenAI GPT-3.5-turbo model.

## Dependencies

- ROS (Robot Operating System)
- Python 2.7 or 3.x
- speech_recognition
- gtts (Google Text-to-Speech)
- (your custom API for communicating with OpenAI)

# OpenAI Chat ROS Package

This ROS package provides two nodes for speech-to-text (STT) and text-to-speech (TTS) functionality using the OpenAI API. The STT node listens to audio input from a microphone, performs speech recognition, sends the recognized text to OpenAI for generating a response, and publishes the response to a ROS topic. The TTS node subscribes to the STT topic, receives the responses, and synthesizes them into speech using gTTS.

## Package Structure

The package consists of the following files:

- `stt_node.py`: The STT node script responsible for speech recognition and OpenAI interaction.
- `tts_node.py`: The TTS node script responsible for speech synthesis.
- `CMakeLists.txt`: The CMake build configuration file.
- `package.xml`: The package manifest file.

## Usage
1. Launch the STT node in a terminal:
$ rosrun openai_chat stt_node.py
2. Launch the TTS node in another terminal:
$ rosrun openai_chat tts_node.py
