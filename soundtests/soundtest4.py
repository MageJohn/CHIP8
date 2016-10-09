# The first sound test I wrote from scratch  which functioned 
# correctly. I had been fiddling with soundtest2.py a lot, and it was
# getting overly complicated. I decided that it would be best start
# over, and keep it simple. After this was working, I went back and
# applied what I learned to soundtest2.py, and got that functioning.

from sdl2 import *
from ctypes import *

AMPLITUDE = 255
SAMPLES_PER_SECOND = 44100
CHANNELS = 1

TONE_HZ = 262
SQUARE_WAVE_PERIOD = int(SAMPLES_PER_SECOND / TONE_HZ)
HALF_SQUARE_WAVE_PERIOD = int(SQUARE_WAVE_PERIOD / 2)

audio_settings = SDL_AudioSpec(freq=SAMPLES_PER_SECOND,
                               aformat=AUDIO_U8,
                               channels=CHANNELS,
                               samples=4096)

SDL_Init(SDL_INIT_AUDIO)
devid = SDL_OpenAudioDevice(None, 0, audio_settings, audio_settings, 0)

running_sample_index = 0
phase = 0

SDL_PauseAudioDevice(devid, 0)
while True:
    sound_buffer = (c_ubyte * audio_settings.samples)()

    for i in range(audio_settings.samples):
        running_sample_index += 1
        if running_sample_index % HALF_SQUARE_WAVE_PERIOD == 0:
            phase = int(not phase)
        sample = AMPLITUDE * phase
        sound_buffer[i] = c_ubyte(sample)

    SDL_QueueAudio(devid, byref(sound_buffer), audio_settings.samples)
    print(SDL_GetQueuedAudioSize(devid))
