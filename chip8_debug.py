'''This file is just for my own debugging purposes. It's very hacky, 
and is intended to minimise the typing necassary to use the codebase
from the interactive shell, nothing more.'''


import time

import chip8
import chip8_core
import platform_sdl
import chip8_input

interpreter = chip8_core.Interpreter()


def print_screen(state):
    '''Utility to print out a screen array such as State.screen'''
    for y in range(state.SCREEN_HEIGHT):
        for x in state.screen[y*state.SCREEN_WIDTH:(y+1)*state.SCREEN_WIDTH]:
            print('█' if x else '░', end='')
        print()


def print_state(state):
    '''Format and print the data in a chip8_core.State object.'''
    keys_on_off = ' '.join([format(i, 'X') if state.keypad[i] else ' ' for i in range(16)])
    current_opcode = interpreter.read_opcode(state, advance=False)
    print('''
Registers
V0 V1 V2 V3 V4 V5 V6 V7 V8 V9 VA VB VC VD VE VF
{0[0]:02X} {0[1]:02X} {0[2]:02X} {0[3]:02X} {0[4]:02X} {0[5]:02X} {0[6]:02X} \
{0[7]:02X} {0[8]:02X} {0[9]:02X} {0[10]:02X} {0[11]:02X} {0[12]:02X} \
{0[13]:02X} {0[14]:02X} {0[15]:02X}

Pressed keys: {1}

I   pc  delay sound
{2:03X} {3:03X} {4:02X}    {5:02X}

Current opcode
0x{6:04X}

{7}

Stack
'''.format(state.register, 
           keys_on_off,
           state.I, state.pc, state.delay, state.sound,
           current_opcode,
           chip8_core.doc(current_opcode)))
    for i in state.stack:
        print(format(i, '03X'))


def print_screen_state(state):
    print_screen(state)
    print_state(state)


def step_print_screen_state(state):
    interpreter.step(state)
    print_screen_state(state)


def debug_sdl(state):
    chip8.chip8(None, chip8.KEYMAP, state)
    platform_sdl.sdl2.SDL_Quit()


def init(filename):
    with open(filename, 'rb') as binary_file:
        program = binary_file.read()

    state = chip8_core.State(program)

    return state
