import azure.cognitiveservices.speech as speechsdk
import asyncio
import random
import socketserver  # we use the socketserver module that comes with python3

speech_key = "SPEECH_KEY_HERE" #<- put your AZURE speech key here . PLEASE READ THIS IF YOU ARE LOST: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python
service_region = "SERVICE_REGION_HERE" #<- put your AZURE service region here, for example, i use 'eastus'
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
synthesizer = speechsdk.SpeechSynthesizer(speech_config, None)
connection = speechsdk.Connection.from_speech_synthesizer(synthesizer)
connection.open(True)
print ("Ready")

class MyUDPHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        

        # for line terminated messages
        msgRecvd = self.rfile.readline().strip()
        print("The Message is {}".format(msgRecvd.decode('utf-8')))
        stylelist = ["shouting", "excited", "normal", "cheerful"]
        namelist = ["Guy", "Tony", "Davis"]
        name = random.choice(namelist)

        try:
            if stylelist:
                style = random.choice(stylelist)
            else:
                style = "default"
        except Exception as e:
            print("Error choosing style:", e)
            style = "default"

        text = msgRecvd.decode('utf-8')
        if len(text) > 140:
                text = text[:140]
                print(f"Message truncated to: {text}")

        contains_url = any(substring in text for substring in ['https://', 'www.', 'http'])
        if contains_url:
                ssml = f"""<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
                    <voice name="en-US-{name}Neural">
                        <s />
                        <mstts:express-as style="{style}">
                            Link
                        </mstts:express-as>
                        <s />
                    </voice>
                </speak>"""
        else:
                ssml = f"""<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
                    <voice name="en-US-{name}Neural">
                        <s />
                        <mstts:express-as style="{style}">
                            {text}
                        </mstts:express-as>
                        <s />
                    </voice>
                </speak>"""

        try:
                if not stylelist:
                    style = "default"
                asyncio.run(self.play_tts(ssml, None, contains_url))
        except Exception as e:
                print("Error during TTS:", e)

    async def play_tts(self, ssml, ssml2, contains_url):
        try:
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            result = await speech_synthesizer.speak_ssml_async(ssml)
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized for text [{}]".format(ssml))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
        except Exception as e:
            print(e)


# this is the main entrypoint
if __name__ == '__main__':
    # we specify the address and port we want to listen on
    listen_addr = ('0.0.0.0', 5005)

    # with allowing to reuse the address we dont get into problems running it consecutively sometimes
    socketserver.UDPServer.allow_reuse_address = True

    # register our class
    serverUDP = socketserver.UDPServer(listen_addr, MyUDPHandler)
    serverUDP.serve_forever()
