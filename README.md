# GrawlixChatCatScript
using Microsoft Azure Voices and Streamer.bot allows overlap between messages for maximum chaos

# Prerequisites
Python 3.6 or later

An active Azure subscription

Azure Cognitive Services Speech SDK for Python
 -> pip install azure-cognitiveservices-speech
 -> PLEASE READ AND FOLLOW THIS GUIDE: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python

# Guide:

1. Replace the placeholders in the script with your Azure Speech API key and service region:
   speech_key = "SPEECH_KEY_HERE"
   service_region = "SERVICE_REGION_HERE"

2. Run the script
   python tts.py

3. use streamer.bot (https://streamer.bot/) to send a broadcast to the script
   i have a trigger set up everytime someone in chat sends a message,
   with triggers the sub-action UDP broadcast (under core/network)
   the UDP port set to 5005 (this can be any number as long as it matches the one in the script. the default is 5005)
   the payload data is set to '%rawInput%' it is important to write it out like so. 
    
