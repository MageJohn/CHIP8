import time
import sys
import io

import sdl2
import sdl2.ext
from PIL import Image


import chip8_core

WINDOW_SCALE=16
BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
PALETTE = (BLACK, WHITE)
KEYS = (sdl2.SDLK_KP_0,
        sdl2.SDLK_KP_1,
        sdl2.SDLK_KP_2,
        sdl2.SDLK_KP_3,
        sdl2.SDLK_KP_4,
        sdl2.SDLK_KP_5,
        sdl2.SDLK_KP_6,
        sdl2.SDLK_KP_7,
        sdl2.SDLK_KP_8,
        sdl2.SDLK_KP_9,
        sdl2.SDLK_a,
        sdl2.SDLK_b,
        sdl2.SDLK_c,
        sdl2.SDLK_d,
        sdl2.SDLK_e,
        sdl2.SDLK_f)


def screen_to_texture(state, factory):
    im_screen = Image.new('1', (state.SCREEN_WIDTH, state.SCREEN_HEIGHT))
    im_screen.putdata([p * 255 for p in state.screen])
    bytesio_screen = io.BytesIO()
    im_screen.save(bytesio_screen, format='BMP')
    bytesio_screen.seek(0)

    return factory.from_object(bytesio_screen)


def chip8(program):
    state = chip8_core.State(program)

    sdl2.ext.init()
    window = sdl2.ext.Window("CHIP-8", size=(state.SCREEN_WIDTH*WINDOW_SCALE, state.SCREEN_HEIGHT*WINDOW_SCALE), flags=sdl2.SDL_WINDOW_RESIZABLE)
    window.show()

    renderer = sdl2.ext.Renderer(window, logical_size=(state.SCREEN_WIDTH, state.SCREEN_HEIGHT))
    texture_renderer = sdl2.ext.TextureSpriteRenderSystem(renderer)
    sprite_factory = sdl2.ext.SpriteFactory(renderer=renderer)

    countdown = 0
    running = True

    while running:
        t1 = time.perf_counter()

        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key in KEYS:
                    state.keypad[KEYS.index(key)] = 1
                    print('Key Down: {:X}'.format(KEYS.index(key)))
            elif event.type == sdl2.SDL_KEYUP:
                key = event.key.keysym.sym
                if key in KEYS:
                    state.keypad[KEYS.index(key)] = 0
                    print('Key Up: {:X}'.format(KEYS.index(key)))


        chip8_core.execute_opcode(state, chip8_core.read_opcode(state))

        texture = screen_to_texture(state, sprite_factory)
        texture_renderer.render(texture, x=0, y=0)

        t2 = time.perf_counter()

        countdown += (t2 - t1)
        if countdown >= 1/60:
            if state.delay > 0:
                state.delay -= 1
            if state.sound > 0:
                state.sound -= 1
            countdown = 0


if __name__ == '__main__':
    with open(sys.argv[1], "rb") as binary_file:
        program = binary_file.read()
        chip8(program)