# An attempt to rewrite the handmade penguin sound code in Python.
# This one didn't work, but soundtest2.py is based on it and does work.
# Link: https://davidgow.net/handmadepenguin/ch8.html

import sdl2
import ctypes

def init_audio(samples_per_second, buffer_size):
    audio_settings = sdl2.SDL_AudioSpec(freq=samples_per_second,
                                        aformat=sdl2.AUDIO_S16LSB,
                                        channels=2,
                                        samples=buffer_size)
    sdl2.SDL_OpenAudio(audio_settings, audio_settings)

    if audio_settings.format != sdl2.AUDIO_S16LSB:
        print("Oops! We didn't get AUDIO_S16LSB as our sample format!")
        sdl2.SDL_CloseAudio()


samples_per_second = 48000
tone_hz = 256
tone_volume = 3000
running_sample_index = 0
squarewave_period = samples_per_second / tone_hz
half_squarewave_period = squarewave_period / 2
bytes_per_sample = ctypes.sizeof(ctypes.c_int16) * 2
sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)
init_audio(samples_per_second, int(samples_per_second * bytes_per_sample / 10))
sound_is_playing = False

while True:
    target_queue_bytes = samples_per_second * bytes_per_sample
    bytes_to_write = target_queue_bytes - sdl2.SDL_GetQueuedAudioSize(1)

    if bytes_to_write > 0:
        sound_buffer = (ctypes.c_int16 * bytes_to_write)()
        bytes_buffer = ctypes.cast(sound_buffer, POINTER(ctypes.c_ubyte))
        sample_count = int(bytes_to_write / bytes_per_sample)
        for i in range(sample_count):
            running_sample_index += 1
            high = (running_sample_index / half_squarewave_period) % 2
            sample_value = tone_volume if high else -tone_volume
            sound_buffer[i*bytes_per_sample] = ctypes.c_int16(sample_value)
            sound_buffer[i*bytes_per_sample+1] = ctypes.c_int16(sample_value)

        sdl2.SDL_QueueAudio(1, sound_buffer, bytes_to_write)
        del(sound_buffer)

    if not sound_is_playing:
        sdl2.SDL_PauseAudio(0)
        sound_is_playing = True


