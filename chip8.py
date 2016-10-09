import time
import sys
import importlib

import chip8_state
import chip8_interpreter
import chip8_input

# NOTE: These constants will be moved to a configuration file at some point

platform_layers = {'sdl': 'platform_sdl'}

PLATFORM_LAYER = 'sdl'

if PLATFORM_LAYER in platform_layers.keys():
    platform_layer = importlib.import_module(platform_layers[PLATFORM_LAYER])
else:
    sys.exit("Unknown platform layer")

PLATFORM_OPTIONS = {'window': {
                               'window_scale': 16,
                               'palette'     : ((0,0,0), (255,255,255)),
                               'title'       : 'CHIP8'
                              },
                    'sound':  {
                               'volume'      : .5, # in percent
                               'tonehz'      : 440, # Note A4
                               'wavetype'    : 'sine' # sine or square
                              }
                   }

KEYMAP  = {'0'      :   0, # Number key
           'kp_0'   :   0, # Keypad number key
           '1'      :   1,
           'kp_7'   :   1,
           '2'      :   2,
           'kp_8'   :   2,
           'up'     :   2, # Non-printing key, named in full
           '3'      :   3,
           'kp_9'   :   3,
           '4'      :   4,
           'kp_4'   :   4,
           'left'   :   4,
           '5'      :   5,
           'kp_5'   :   5,
           '6'      :   6,
           'kp_6'   :   6,
           'right'  :   6,
           '7'      :   7,
           'kp_1'   :   7,
           '8'      :   8,
           'kp_2'   :   8,
           'down'   :   8,
           '9'      :   9,
           'kp_3'   :   9,
           'a'      : 0xA, # Letter key
           'kp_a'   : 0xA,
           'b'      : 0xB,
           'kp_b'   : 0xB,
           'c'      : 0xC,
           'kp_c'   : 0xC,
           'd'      : 0xD,
           'kp_d'   : 0xD,
           'e'      : 0xE,
           'kp_e'   : 0xE,
           'f'      : 0xF,
           'kp_f'   : 0xF,
           'escape' : 'exit',
           'ctrl+q' : 'exit' # Modifier + letter key
           }
           # Other possibilites include multiple modifiers. Modifiers themselves can't be bound directly.


def chip8(program, keymap, state=None):
    if not state:
        state = chip8_state.State(program)

    platform_interface = platform_layer.Interface(state, PLATFORM_OPTIONS)

    countdown = 0
    beeping = False
    running = True

    t1 = time.perf_counter()
    while running:
        events = platform_interface.input.get_events()
        for event in events:
            if event.type == chip8_input.QUIT:
                running = False
            elif event.keycode in keymap.keys():
                action = keymap[event.keycode]
                if action == 'exit':
                    running = False
                elif (type(action) == int and 
                      action in range(len(state.keypad))):
                    state.keypad[action] = event.type
                else:
                    message = "Unhandled action: {}".format(action)
                    raise chip8_input.UnhandledActionError(message, action)
        if not running:
            break

        delay_was = state.delay
        chip8_interpreter.step(state)

        platform_interface.video.update_screen(state)

        #### Timer End ####
        t2 = time.perf_counter()

        countdown += (t2 - t1) # Add timer value to countdown

        t1 = time.perf_counter()
        #### Timer Start ####

        if countdown >= 1/60:
            if delay_was >= state.delay: # This ensures that at least 1/60 of
                                         # a second is elapsed before the
                                         # delay timer starts ticking. Else
                                         # a delay of 1 might not have an
                                         # effect.
                state.delay = max(0, state.delay - 1)
            if state.sound > 0:
                if not beeping:
                    platform_interface.audio.beep(state.sound * 1000/60)
                    beeping = True
                state.sound -= 1
            else:
                beeping = False

            countdown = 0


if __name__ == '__main__':
    with open(sys.argv[1], "rb") as binary_file:
        program = binary_file.read()
    chip8(program, KEYMAP)