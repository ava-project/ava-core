from os import environ, path
import signal, sys
import pyaudio
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from Daemon import Daemon
from Event import Event
from SetupMic import MicConfig

import wave

#define stream chunk
#chunk = 1024
f = wave.open("../static/launch.wav","rb")
f2 = wave.open("../static/success.wav","rb")
# print(f.getframerate())

#MODELDIR = "/usr/local/share/pocketsphinx/model"
#DATADIR = "../../../test/data"

# config = Decoder.default_config()
# config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
# config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
# config.set_string('-dict', path.join('static/custom.dict'))
# config.set_string('-logfn', '/dev/null')
# decoder = Decoder(config)

bold = "\033[1m"
reset = "\033[0;0m"

def signal_handler(signal, frame):
    # print 'You pressed Ctrl+C!'
    sys.exit(0)

try:
    sys.argv[1]
except:
    micConfig = MicConfig("custom.dict")
else:
    micConfig = MicConfig(sys.argv[1])

#micConfig.setup_mic()
p = pyaudio.PyAudio()
stream = p.open(format = micConfig.FORMAT,
                channels = micConfig.CHANNELS,
                rate = micConfig.RATE,
                input = True,
                frames_per_buffer = 2048)
stream2 = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
#read data
data = f.readframes(micConfig.CHUNK)
stream.start_stream()

in_speech_bf = False
micConfig.decoder.start_utt()
daemon = Daemon()
daemon.run()
signal.signal(signal.SIGINT, signal_handler)
go = False
while True:
    buf = stream.read(micConfig.CHUNK)
    if buf:
        micConfig.decoder.process_raw(buf, False, False)
        if micConfig.decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = micConfig.decoder.get_in_speech()
            if not in_speech_bf:
                micConfig.decoder.end_utt()
                result = micConfig.decoder.hyp().hypstr
                print('Result:[%s]' %result)
                if go == True:
                    if result == "exit":
                        break
                    if result == "play music":
                        print("You want me to execute %s" %result + reset)
                        result = "vlc ../static/music.mp3"
                        daemon.add_event(Event(result, False, 0))
                        result = ""
                    if result.startswith("change directory") :
                        print("You want me to execute %s" %result + reset)
                        result = "cd" + result[16:]
                        daemon.add_event(Event(result, False, 0))
                        result = ""
                    if result == "google":
                        print("You want me to execute %s" %result + reset)
                        result = "chromium-browser"
                        daemon.add_event(Event(result, False, 0))
                        result = ""
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
                        data = f.readframes(micConfig.CHUNK)
                    print(bold + 'What can I do for you ?')
                    #stop stream wav before adding the success sound
                    stream2.stop_stream()
                    stream2.close()
                    result = ""
                    stream.start_stream()
                    go = True

                micConfig.decoder.start_utt()
    else:
        break
daemon.stop();
#micConfig.decoder.end_utt()
