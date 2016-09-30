import time

import chip8
import chip8_core
import platform_sdl
import chip8_input

PLATFORM_OPTIONS = {'window_scale': 16,
                    'palette': ((0,0,0), (255,255,255)),
                    'title': 'CHIP8'}

DEBUG_KEYMAP  = {'0'      :   0,
                 'kp_0'   :   0,
                 '1'      :   1,
                 'kp_7'   :   1,
                 '2'      :   2,
                 'kp_8'   :   2,
                 'up'     :   2,
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
                 'a'      : 0xA,
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
                 'ctrl+q' : 'exit',
                 'ctrl+b' : 'break',
                }


def print_screen(state):
    '''Utility to print out a screen array such as State.screen'''
    for y in range(state.SCREEN_HEIGHT):
        for x in state.screen[y*state.SCREEN_WIDTH:(y+1)*state.SCREEN_WIDTH]:
            print('█' if x else '░', end='')
        print()


def print_state(state, interpreter):
    '''Format and print the data in a chip8_core.State object.'''
    keys_on_off = ' '.join([format(i, 'X') if state.keypad[i] else ' ' for i in range(16)])
    print('''
Registers
V0 V1 V2 V3 V4 V5 V6 V7 V8 V9 VA VB VC VD VE VF
{0[0]:02X} {0[1]:02X} {0[2]:02X} {0[3]:02X} {0[4]:02X} {0[5]:02X} {0[6]:02X} \
{0[7]:02X} {0[8]:02X} {0[9]:02X} {0[10]:02X} {0[11]:02X} {0[12]:02X} \
{0[13]:02X} {0[14]:02X} {0[15]:02X}

Pressed keys: {1}

I   pc  delay sound
{2:03X} {3:03X} {4:02X}    {5:02X}

Last opcode  Current opcode
0x{6:04X}       0x{7:04X}

Stack
'''.format(state.register, 
           keys_on_off,
           state.I, state.pc, state.delay, state.sound,
           interpreter.read_opcode(state, offset=(-1), advance=False),
           interpreter.read_opcode(state, advance=False)))
    for i in state.stack:
        print(format(i, '03X'))


def print_screen_state(state, interpreter):
    print_screen(state)
    print_state(state, interpreter)


def step_print_screen_state(state, interpreter):
    interpreter.step(state)
    print_screen_state(state, interpreter)


def debug_sdl(state):
    chip8.chip8(None, chip8.KEYMAP, state)
    platform_sdl.sdl2.SDL_Quit()

