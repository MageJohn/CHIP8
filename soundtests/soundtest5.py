# After getting soundtest2.py and soundtest4.py working, I decided to
# test my knowledge by writing a soundtest using the audio callback 
# method from scratch. It worked almost without a hitch!

from sdl2 import *
from ctypes import *
from math import sin, pi

SAMPLES_PER_SECOND = 44100
FREQUENCY = 440
SQUARE_WAVE_PERIOD = int(SAMPLES_PER_SECOND/FREQUENCY)
HALF_SQUARE_WAVE_PERIOD = int(SQUARE_WAVE_PERIOD/2)

SDL_Init(SDL_INIT_AUDIO)

class Sound:
    def __init__(self):
        self.phase = 0
        self.running_sample_index = 0
        self.v = 0

    def callback(self, notused, stream, length):
        for i in range(length):
            #self.running_sample_index += 1
            #if self.running_sample_index % HALF_SQUARE_WAVE_PERIOD == 0:
                #self.phase += 1
            #sample = 127 if self.phase % 2 else -127

            sample = int(127 * sin(self.v*2*pi/SAMPLES_PER_SECOND))
            self.v += FREQUENCY
            stream[i] = c_ubyte(sample)

s = Sound()
sdl_callback = SDL_AudioCallback(s.callback)
spec = SDL_AudioSpec(freq=SAMPLES_PER_SECOND,
                     aformat=AUDIO_S8,
                     channels=1,
                     samples=0,
                     callback=sdl_callback)

devid = SDL_OpenAudioDevice(None, 0, spec, spec, 0)

SDL_PauseAudioDevice(devid, 0)
input('Press Enter to exit')
