# The second sound test, written entirely by  myself, that I got to
# actually work. It has lots of options in the constants, *almost* all
# of which function corretly!

from ctypes import *
from sdl2 import *

## Sample format ##
BITSIZE = 8 # 8, 16, or 32.
DATATYPE = 0 << 8 # Integer (0) or float (1). Float is 32 bit only.
ENDIAN = 0 << 12 # Little endian (0) or Big endian (1).
SIGNED = 1 << 15 # Unsigned (0) or Signed (1).
SAMPLE_FORMAT = BITSIZE | DATATYPE | ENDIAN | SIGNED

## Other Audio Settings
SAMPLES_PER_SECOND = 44100
CHANNELS = 1 # 1, 2, 4, or 6

## Tone Settings ##
TONE_HZ = 256
TONE_VOLUME = .25 # Volume in percent
SQUARE_WAVE_PERIOD = int(SAMPLES_PER_SECOND / TONE_HZ) # Number of samples in 1 hz
HALF_SQUARE_WAVE_PERIOD = int(SQUARE_WAVE_PERIOD / 2) # Number of samples for up or down


FORMAT_TO_CINT = {0x8008: c_int8,
                  0x8010: c_int16,
                  0x8020: c_int32,
                  0x0008: c_uint8,
                  0x0010: c_uint16,
                  0x0020: c_uint32,
                  0x0120: c_float}


SDL_Init(SDL_INIT_AUDIO)

audio_settings = SDL_AudioSpec(freq=SAMPLES_PER_SECOND,
                               aformat=SAMPLE_FORMAT,
                               channels=CHANNELS,
                               samples=4096)

devid = SDL_OpenAudioDevice(None, 0, audio_settings, audio_settings, SDL_AUDIO_ALLOW_ANY_CHANGE)

sample_format = FORMAT_TO_CINT[audio_settings.format&0x81FF]
bytes_per_sample = sizeof(sample_format)

issigned = (audio_settings.format & (1<<15)) >> 15
amplitude = int(TONE_VOLUME * 2**(sizeof(sample_format)*(8-issigned)) - 1)

running_sample_index = 0
phase = 0

SDL_PauseAudioDevice(devid, 0)
while True:
    bytes_buffer = (c_ubyte * audio_settings.size)()
    sound_buffer = cast(bytes_buffer, POINTER(sample_format))
    i = 0
    for i in range(int(audio_settings.size / 
                       bytes_per_sample / 
                       audio_settings.channels)):
        running_sample_index += 1
        if running_sample_index % HALF_SQUARE_WAVE_PERIOD == 0:
            phase += 1
        if issigned:
            sample_value = amplitude if phase % 2 else -amplitude
        else:
            sample_value = (phase % 2) * amplitude
        for c in range(audio_settings.channels):
            sound_buffer[i*audio_settings.channels+c] = sample_format(sample_value)
    SDL_QueueAudio(devid, bytes_buffer, audio_settings.size)
