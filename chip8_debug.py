'''This file is just for my own debugging purposes. The idea is to call
`from chip8_debug import *` to set up the interpreter with everything
needed to interact with the codebase.'''

import tempfile
import os

from subprocess import call

import chip8
import chip8_input
import chip8_state
import chip8_interpreter
import platform_sdl


def print_screen(state):
    '''Utility to print out state.screen to the console'''
    for y in range(state.SCREEN_HEIGHT):
        for x in state.screen[y*state.SCREEN_WIDTH:(y+1)*state.SCREEN_WIDTH]:
            print('█' if x else '░', end='')
        print()


def print_sprite(state, I, N):
    '''
Utility to print out N bytes of sprite data, starting at I, from
state.memory'''
    sprite = []
    for y in range(N):
        for x in format(state.memory[I+y], '08b'):
            sprite.append('█' if int(x) else '░')
        sprite.append('\n')
    print(''.join(sprite))


def print_state(state):
    '''Format and print the data in a chip8_state.State object.'''
    keys_on_off = ' '.join([format(i, 'X') if state.keypad[i] else ' ' for i in range(16)])
    current_opcode = chip8_interpreter.read_opcode(state, advance=False)
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
           descriptions[current_opcode]))
    for i in state.stack:
        print(format(i, '03X'))


def print_screen_state(state):
    print_screen(state)
    print_state(state)


def step_print_screen_state(state):
    chip8_interpreter.step(state)
    print_screen_state(state)


def step_out(state, handle_delay=True):
    '''Run until a return command is executed.'''
    while chip8_interpreter.read_opcode(state, advance=False) != 0x00EE:
        chip8_interpreter.step(state)
        if handle_delay:
            state.delay = 0
    chip8_interpreter.step(state)


def debug_sdl(state):
    '''Setup, run, and clean up after chip8.chip8()'''
    chip8.chip8(None, chip8.KEYMAP, state)
    platform_sdl.sdl2.SDL_Quit()

def memslice(state, start, stop):
    '''Print state.memory[start, stop] with the numbers in hex form '''
    print('[', end='')
    for i in state.memory[start:stop-1]:
        print('0x{:02X}'.format(i), end=', ')
    print('0x{:02X}]'.format(state.memory[stop-1]))


def init_state(filename):
    '''Open filename and initialise a State object with it.'''
    with open(filename, 'rb') as binary_file:
        program = binary_file.read()

    state = chip8_state.State(program)

    return state

class Descriptions:
    def __init__(self):
        self._notes = {}
        self.docstrings = {"0x0NNN":    "Execute machine language subroutine at address {0.NNN:03X}.",
                           "0x00E0":    "Clear the screen.",
                           "0x00EE":    "Return from a subroutine.",
                           "0x1NNN":    "Jump to address {0.NNN:03X}.",
                           "0x2NNN":    "Execute subroutine starting at address {0.NNN:03X}.",
                           "0x3XNN":    "Skip the following instruction if the value of register V{0.X:01X} equals {0.NN:02X}.",
                           "0x4XNN":    "Skip the following instruction if the value of register V{0.X:01X} is not equal to {0.NN:02X}.",
                           "0x5XY0":    "Skip the following instruction if the value of register V{0.X:01X} is equal to the value of register V{0.Y:01X}.",
                           "0x6XNN":    "Store number {0.NN:02X} in register V{0.X:01X}.",
                           "0x7XNN":    "Add the value {0.NN:02X} to register V{0.X:01X}.",
                           "0x8XY0":    "Store the value of register V{0.Y:01X} in register V{0.X:01X}.",
                           "0x8XY1":    "Set V{0.X:01X} to V{0.X:01X} OR V{0.Y:01X}.",
                           "0x8XY2":    "Set V{0.X:01X} to V{0.X:01X} AND V{0.Y:01X}.",
                           "0x8XY3":    "Set V{0.X:01X} to V{0.X:01X} XOR V{0.Y:01X}.",
                           "0x8XY4":    "Add the value of register V{0.Y:01X} to register V{0.X:01X}. \nSet VF to 01 if a carry occurs. \nSet VF to 00 if a carry does not occur.",
                           "0x8XY5":    "Subtract the value of register V{0.Y:01X} from register V{0.X:01X}. \nSet VF to 00 if a borrow occurs. \nSet VF to 01 if a borrow does not occur.",
                           "0x8XY6":    "Shifts V{0.X:01X} right by one. VF is set to the value of the least significant bit of V{0.X:01X} before the shift.",
                           "0x8XY7":    "Set register V{0.X:01X} to the value of V{0.Y:01X} minus V{0.X:01X}. \nSet VF to 00 if a borrow occurs. \nSet VF to 01 if a borrow does not occur.",
                           "0x8XYE":    "Shifts V{0.X:01X} left by one. VF is set to the value of the most significant bit of V{0.X:01X} before the shift.",
                           "0x9XY0":    "Skip the following instruction if the value of register V{0.X:01X} is not equal to the value of register V{0.Y:01X}.",
                           "0xANNN":    "Store memory address {0.NNN:03X} in register I.",
                           "0xBNNN":    "Jump to address {0.NNN:03X} + V0.",
                           "0xCXNN":    "Set V{0.X:01X} to a random number with a mask of {0.NN:02X}.",
                           "0xDXYN":    "Draw a sprite at position V{0.X:01X}, V{0.Y:01X} with {0[3]:X} bytes of sprite data starting at the address stored in I. \nSet VF to 01 if any set pixels are changed to unset, and 00 otherwise.",
                           "0xEX9E":    "Skip the following instruction if the key corresponding to the hex value currently stored in register V{0.X:01X} is pressed.",
                           "0xEXA1":    "Skip the following instruction if the key corresponding to the hex value currently stored in register V{0.X:01X} is not pressed.",
                           "0xFX07":    "Store the current value of the delay timer in register V{0.X:01X}.",
                           "0xFX0A":    "Wait for a keypress and store the result in register V{0.X:01X}.",
                           "0xFX15":    "Set the delay timer to the value of register V{0.X:01X}.",
                           "0xFX18":    "Set the sound timer to the value of register V{0.X:01X}.",
                           "0xFX1E":    "Add the value stored in register V{0.X:01X} to register I.",
                           "0xFX29":    "Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in register V{0.X:01X}.",
                           "0xFX33":    "Store the binary-coded decimal equivalent of the value stored in register V{0.X:01X} at addresses I, I+1, and I+2.",
                           "0xFX55":    "Store the values of registers V0 to V{0.X:01X} inclusive in memory starting at address I. \nI is set to I + {0.X:01X} + 1 after operation.",
                           "0xFX65":    "Fill registers V0 to V{0.X:01X} inclusive with the values stored in memory starting at address I. \nI is set to I + {0.X:01X} + 1 after operation."}

    def __getitem__(self, opcode):
        '''Return a string documenting the specific opcode passed. If there is
a note set for opcode, that is included.'''

        opcode = self._normalize_opcode(opcode)

        if opcode[0] == 0:
            try:
                string = self.docstrings[opcode.__repr__()]
            except KeyError:
                string = self.docstrings["0x0NNN"]
        elif opcode[0] == 8:
            l_opcode = list(opcode.__repr__())
            l_opcode[3:5] = ['X', 'Y']
            string = self.docstrings[''.join(l_opcode)]
        elif opcode[0] == 0xE or opcode[0] == 0xF:
            l_opcode = list(opcode.__repr__())
            l_opcode[3] = 'X'
            string = self.docstrings[''.join(l_opcode)]
        else:
            string = self.docstrings['0' + chip8_interpreter.MAPPING[opcode[0]].__name__]

        try:
            string = string + '\n\nNote: ' + self._notes[opcode]
        except KeyError:
            pass

        return string.format(opcode)

    def annotate(self, opcode):
        '''Create or edit the note on a particular opcode in $EDITOR. If note
set, nano is used.'''
        opcode = self._normalize_opcode(opcode)
        try:
            note = self._notes[opcode]
        except KeyError:
            note = ''

        EDITOR = os.environ.get('EDITOR','nano') #that easy!
        if EDITOR == 'nano':
            line = len(note.split('\n'))
            column = len(note.split('\n')[-1]) + 1
            cli_options = [EDITOR, '-L', '-R', '+{},{}'.format(line, column)]
        else:
            cli_options = [EDITOR]
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
          tf.write(bytes(note, 'utf-8'))
          tf.flush()
          cli_options.append(tf.name)
          call(cli_options)
          tf.seek(0)
          self._notes[opcode] = tf.read().decode('utf-8')
        

    def _normalize_opcode(self, opcode):
        '''Convert opcodes in string and integer
forms into an Opcode object'''
        if type(opcode) == int:
            opcode = chip8_interpreter.Opcode(opcode)
        elif type(opcode) == str:
            opcode = chip8_interpreter.Opcode(int(opcode, 16))
        return opcode

# If debugging a particular file, save typing by setting it here.
FILENAME = '/home/yuri/Downloads/Chip-8 Pack/Chip-8 Games/Landing.ch8'

state = init_state(FILENAME)
descriptions = Descriptions()
note = descriptions.annotate
