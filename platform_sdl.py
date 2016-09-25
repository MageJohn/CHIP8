import time
import sys
import io

import sdl2
import sdl2.ext
from PIL import Image


import chip8_core

class Interface:
    def __init__(self, state, option_dict, program_name="CHIP-8"):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO|sdl2.SDL_INIT_AUDIO) != 0:
            sys.exit("SDL_Init failed: {}".format(sdl2.SDL_GetError()))

        self.state = state
        self.option_dict = option_dict

        self.video = Video(self, program_name)
        self.input = Input(self)
        self.audio = Audio(self)


class Video:
    def __init__(self, interface, program_name):
        # NOTE: This class wraps SDL2 video.
        self.interface = interface

        window_scale = self.interface.option_dict['window_scale']
        self.palette = self.interface.option_dict['palette']

        win_size = (self.interface.state.SCREEN_WIDTH*window_scale, 
                    self.interface.state.SCREEN_HEIGHT*window_scale)
        self._window = sdl2.ext.Window(program_name, 
                                       size=win_size,
                                       flags=sdl2.SDL_WINDOW_RESIZABLE)
        self._window.show()

        logical_size = (self.interface.state.SCREEN_WIDTH,
                        self.interface.state.SCREEN_HEIGHT)
        self._renderer = sdl2.ext.Renderer(self._window, logical_size=logical_size)
        self._texture_renderer = sdl2.ext.TextureSpriteRenderSystem(self._renderer)
        self._sprite_factory = sdl2.ext.SpriteFactory(renderer=self._renderer)

    def update_screen(self):
        im_screen = Image.new('RGB', 
                              (self.interface.state.SCREEN_WIDTH, 
                               self.interface.state.SCREEN_HEIGHT))
        im_screen.putdata([self.palette[p] for p in self.interface.state.screen])
        bytesio_screen = io.BytesIO()
        im_screen.save(bytesio_screen, format='BMP')
        bytesio_screen.seek(0)

        texture = self._sprite_factory.from_object(bytesio_screen)
        self._texture_renderer.render(texture, x=0, y=0)



class Input:
    def __init__(self, interface):
        self.interface = interface

        self.keys = (sdl2.SDLK_KP_0, # 0
                     sdl2.SDLK_KP_7, # 1
                     sdl2.SDLK_KP_8, # 2
                     sdl2.SDLK_KP_9, # 3
                     sdl2.SDLK_KP_4, # 4
                     sdl2.SDLK_KP_5, # 5
                     sdl2.SDLK_KP_6, # 6
                     sdl2.SDLK_KP_1, # 7
                     sdl2.SDLK_KP_2, # 8
                     sdl2.SDLK_KP_3, # 9
                     sdl2.SDLK_a,    # A
                     sdl2.SDLK_b,    # B
                     sdl2.SDLK_c,    # C
                     sdl2.SDLK_d,    # D
                     sdl2.SDLK_e,    # E
                     sdl2.SDLK_f)    # F

    def process(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                return 'exit'
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key in self.keys:
                    self.interface.state.keypad[self.keys.index(key)] = 1
            elif event.type == sdl2.SDL_KEYUP:
                key = event.key.keysym.sym
                if key in self.keys:
                    self.interface.state.keypad[self.keys.index(key)] = 0
        return


class Audio:
    def __init__(self, interface):
        pass
    def beep(self, length):
        pass