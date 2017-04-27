"""
    Here is the Mic class who handles microphone interactions
"""

import pyaudio


class Mic:

    def __init__(self):
        """
        Initiate audio ports with PyAudio instance
        """
        self.audio = pyaudio.PyAudio()

    def __del__(self):
        """
        Destroy the instance of PyAudio
        """
        self.audio.terminate()
