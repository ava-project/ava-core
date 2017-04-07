from os import environ, path
import signal, sys
import pyaudio
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from Daemon import Daemon
from Event import Event

import wave
#define stream chunk
chunk = 1024
f = wave.open(r"static/launch.wav","rb")
f2 = wave.open("static/success.wav","rb")
# print(f.getframerate())

MODELDIR = "/usr/local/share/pocketsphinx/model"
#DATADIR = "../../../test/data"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join('static/custom.dict'))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

bold = "\033[1m"
reset = "\033[0;0m"

def signal_handler(signal, frame):
    # print 'You pressed Ctrl+C!'
    sys.exit(0)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream2 = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
#read data
data = f.readframes(chunk)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
daemon = Daemon()
daemon.run()
signal.signal(signal.SIGINT, signal_handler)
go = False
while True:
    buf = stream.read(chunk)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                result = decoder.hyp().hypstr
                #print('Result:[%s]' %result)
                if go == True:
                    if result == "list":
                        print("You want me to execute %s" %result + reset)
                        result = "ls"
                        daemon.add_event(Event(result, False, 0))
                        result = ""

                if (result == 'ava') and (go == False):
                    stream.stop_stream()
                    #play stream
                    while data:
                        stream2.write(data)
                        data = f.readframes(chunk)
                    print(bold + 'What can I do for you ?')
                    #stop stream wav before adding the success sound
                    stream2.stop_stream()
                    stream2.close()
                    result = ""
                    stream.start_stream()
                    go = True

                decoder.start_utt()
    else:
        break
decoder.end_utt()
