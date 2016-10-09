# A PySDL port of some C++ code I found linked to in a couple of
# places. The original website is down, but it's available on the
# Wayback Machine here: 
# https://web.archive.org/web/20120313055436/http://www.dgames.org/beep-sound-with-sdl/
# Unfortunately, I couldn't find the name of the author. He didn't
# have it on his website, and I can't download the original source
# file, so I don't know if he put it in there.
# The original transcription of the code to Python and ctypes didn't
# immediately work, but with tweaking it was the first time I managed 
# to get generated sound to work.

import math
from sdl2 import *
from ctypes import *

AMPLITUDE = 128
FREQUENCY = 44100
CHANNELS = 2


class BeepObject():
    def __init__(self, freq, samplesLeft):
        self.freq = freq
        self.samplesLeft = samplesLeft


class Beeper():
    def __init__(self):
        self.v = 0
        self.beeps = []
        ac_func = SDL_AudioCallback(self.audio_callback)
        self.spec = SDL_AudioSpec(freq=FREQUENCY,
                                  aformat=AUDIO_S8,
                                  channels=CHANNELS,
                                  samples=4096,
                                  callback=ac_func)

    def beep(self, freq, duration):
        bo = BeepObject(freq, int(duration * (FREQUENCY / 1000)))

        SDL_LockAudio()
        self.beeps.insert(0, bo)
        SDL_UnlockAudio()

    def wait(self):
        while True:
            SDL_Delay(20)
            SDL_LockAudio()
            size = len(self.beeps)
            SDL_UnlockAudio()
            if not size > 0:
                break


    def audio_callback(self, userdata, stream, length):
        i = 0
        length = int(length / CHANNELS)
        while i < length:
            if not self.beeps:
                for i in range(length):
                        for c in range(CHANNELS):
                            stream[i*CHANNELS+c] = c_ubyte(0)
                return

            bo = self.beeps[-1]

            samplesToDo = min(i + bo.samplesLeft, length);
            bo.samplesLeft -= samplesToDo - i

            while i < samplesToDo:
                sample = int(AMPLITUDE * math.sin(self.v * 2 * math.pi / FREQUENCY))
                for c in range(CHANNELS):
                    stream[i*CHANNELS+c] = c_ubyte(sample)
                i += 1
                self.v += bo.freq


            if bo.samplesLeft == 0:
                self.beeps.pop()


if __name__ == '__main__':
    if SDL_Init(SDL_INIT_AUDIO) != 0:
        raise RuntimeError("Cannot initialize audio system: {}".format(SDL_GetError()))



    duration = 50

    D = 293.665
    E = 329.628
    F = 349.228
    G = 391.995
    A = 440.000
    B = 493.883
    c = 554.365
    d = 587.330

    b = Beeper()

    devid = SDL_OpenAudioDevice(None, 0, b.spec, b.spec, 0)

    b.beep(G, duration)
    b.beep(G, duration)
    b.beep(A, duration)
    b.beep(A, duration)
    b.beep(B, duration)
    b.beep(A, duration)
    b.beep(G, duration)
    b.beep(F, duration)
    b.beep(A, duration)
    b.beep(G, duration)
    b.beep(F, duration)
    b.beep(G, duration)
    b.beep(G, duration)
    b.beep(G, duration)
    b.beep(A, duration)
    b.beep(A, duration)
    b.beep(B, duration)
    b.beep(A, duration)
    b.beep(G, duration)
    b.beep(F, duration)

    SDL_PauseAudioDevice(devid, 0)


    b.wait()

    SDL_CloseAudioDevice(devid)
    SDL_Quit(SDL_INIT_AUDIO)