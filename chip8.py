import time
import sys
import importlib

import chip8_core

platform_layers = {'sdl': 'platform_sdl'}

platform_layer = 'sdl'

if platform_layer in platform_layers.keys():
    platform_layer = importlib.import_module(platform_layers[platform_layer])
else:
    sys.exit("Unknown platform layer")

OPTIONS = {'window_scale': 16,
           'palette': ((0,0,0), (255,255,255)),
          }


def chip8(program):
    state = chip8_core.State(program)
    interpreter = chip8_core.Interpreter(state)
    platform_interface = platform_layer.Interface(state, OPTIONS)

    countdown = 0
    beeping = False

    while True:
        t1 = time.perf_counter()

        if platform_interface.input.process() == 'exit':
            break

        delay_was = state.delay
        interpreter.step()

        platform_interface.video.update_screen()

        t2 = time.perf_counter()

        countdown += (t2 - t1)
        if countdown >= 1/60:
            if delay_was >= state.delay: # This ensures that at least 1/60 of
                                         # a second is elapsed before the
                                         # delay timer starts ticking.
                state.delay -= 1
            if state.sound > 0:
                if not beeping:
                    platform_interface.audio.beep(state.sound * 1/60)
                    beeping = True
                state.sound -= 1
            else:
                beeping = False

            countdown = 0


if __name__ == '__main__':
    with open(sys.argv[1], "rb") as binary_file:
        program = binary_file.read()
        chip8(program)