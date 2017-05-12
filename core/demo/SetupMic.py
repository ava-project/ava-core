#!/usr/bin/env python

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os
import pyaudio
import wave
import audioop
from collections import deque
import time
import math

class MicConfig:
    def __init__(self, path):
        # Microphone stream config.
        self.CHUNK = 1024  # CHUNKS of bytes to read each time from mic
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.THRESHOLD = 4500
        self.num_phrases = -1

        # PocketSphinx folder
        MODELDIR = "/usr/local/share/pocketsphinx/model"
        DATADIR = "/usr/local/share/pocketsphinx/test/data"

        # Create a decoder with certain model
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us/en-us'))
        config.set_string('-lm', os.path.join(MODELDIR, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', os.path.join('../static/', path))
        config.set_string('-logfn', '/dev/null')

        # Creaders decoder object for streaming data.
        self.decoder = Decoder(config)

    def thresold_setup(self):

        THRESHOLD_MULTIPLIER = 1.8
        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1
        # prepare recording stream
        stream = self._audio.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(20)]

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, self.RATE / self.CHUNK * THRESHOLD_TIME):

            data = stream.read(self.CHUNK)
            frames.append(data)

            # save this data point as a score
            lastN.pop(0)
            lastN.append(self.getScore(data))
            average = sum(lastN) / len(lastN)

        stream.stop_stream()
        stream.close()

        # this will be the benchmark to cause a disturbance over!
        self.THRESHOLD = average * THRESHOLD_MULTIPLIER

    def setup_mic(self, num_samples=50):
        """ Gets average audio intensity of mic sound. The average
            is the avg of the .2 of the largest intensities recorded.
        """
        print "Getting intensity values from mic."
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print " Finished "
        print " Average audio intensity is ", r
        stream.close()
        p.terminate()

        if r < 3000:
            self.THRESHOLD = 3500
        else:
            self.THRESHOLD = r

    def run(self):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        self.setup_mic()

if __name__ == "__main__":
    sd = MicConfig()
    sd.run()
