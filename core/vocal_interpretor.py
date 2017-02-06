from os import environ, path
import pyaudio
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from Daemon import Daemon
from Event import Event

MODELDIR = "/usr/local/share/pocketsphinx/model"
#DATADIR = "../../../test/data"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join('static/custom.dict'))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
daemon = Daemon()
daemon.run()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                result = decoder.hyp().hypstr
                print('Result:[%s]' %result)
                daemon.add_event(Event(result, False, 0))
                if result == 'yes':
                      print('Do whatever you want')

                decoder.start_utt()
    else:
        break
decoder.end_utt()
