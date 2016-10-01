#!/usr/bin/python3
import sys
import random
import sdl2.ext

import interpreter_opcodes

FONT = (0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
        0x20, 0x60, 0x20, 0x20, 0x70, # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
        0x90, 0x90, 0xF0, 0x10, 0x10, # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
        0xF0, 0x80, 0xF0, 0x80, 0x80) # F

class State:
    def __init__(self, program): # Creates a state object with all values empty
        self.SCREEN_WIDTH = 64
        self.SCREEN_HEIGHT = 32

        self.register = [0x00] * 16 # 16 registers, each 8 bits. Reigisters go from V0 - VF, but VF doubles as a carry flag.
        self.I = 0x0000 # The address register. 16 bits.
        self.pc = 0x200  # Points to the current opcode
        self.delay = 0x00 # When set by 0xFX07, counts down at 60hz
        self.sound = 0x00 # When set by 0xFX18, counts down at 60hz while emitting a tone.
        self.stack = []
        self.keypad = [0] * 16

        self.init_memory(program)
        self.init_screen()

    def load_data(self, data, data_start):
        '''Load data into memory, starting at datastart'''
        for i, byte in enumerate(data):
            self.memory[data_start+i] = byte

    def init_memory(self, program):
        self.memory = [0x00] * 0x1000 # Default 4096 (0x1000) memory locations, each 8 bits (1 byte).
        self.load_data(program, 0x200)
        self.load_data(FONT, 0)

    def init_state(self, program):
        self.init_memory(program)
        self.state.pc = 0x200

    def init_screen(self):
        self.screen = [0x00]*self.SCREEN_HEIGHT*self.SCREEN_WIDTH


class Interpreter:
    def read_opcode(self, state, offset=0, advance=True):
        '''Return the bytes pointed at by state.pc and state.pc + 1. Advance state.pc'''
        pc = state.pc + (offset * 2)
        if advance:
            state.pc += 2
        opcode = state.memory[pc:pc+2]
        return Opcode((opcode[0] << 8) + opcode[1])
        
    def execute_opcode(self, opcode, state):
        '''Perform the opcode on state.'''
        interpreter_opcodes.mapping[opcode[0]](state, opcode)

    def step(self, state):
        self.execute_opcode(self.read_opcode(state), state)


class Opcode(int):
    def __new__(cls, value):
        new_instance = int.__new__(cls, value)
        new_instance.X = (value & 0x0F00) >> 8
        new_instance.Y = (value & 0x00F0) >> 4
        new_instance.NN = value & 0x00FF
        new_instance.NNN = value & 0x0FFF
        new_instance.__hex__ = format(value, '04X')
        return new_instance

    def __repr__(self):
        return '0x' + self.__hex__

    def __getitem__(self, value):
        return int(self.__hex__[value], base=16)


def doc(opcode):
    '''Return a string documenting the specific opcode passed'''
    docstrings = {"0x0NNN":    "Execute machine language subroutine at address {0.NNN:03X}.",
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
                  "0xDXYN":    "Draw a sprite at position V{0.X:01X}, V{0.Y:01X} with N bytes of sprite data starting at the address stored in I. \nSet VF to 01 if any set pixels are changed to unset, and 00 otherwise.",
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
    if type(opcode) == int:
        opcode = Opcode(opcode)
    elif type(opcode) == str:
        opcode = Opcode(int(opcode, 16))

    if opcode[0] == 0:
        try:
            return docstrings[opcode.__repr__()].format(opcode)
        except KeyError:
            return docstrings["0x0NNN"].format(opcode)
    elif opcode[0] == 8:
        l_opcode = list(opcode.__repr__())
        l_opcode[3:5] = ['X', 'Y']
        return docstrings[''.join(l_opcode)].format(opcode)
    elif opcode[0] == 0xE or opcode[0] == 0xF:
        l_opcode = list(opcode.__repr__())
        l_opcode[3] = 'X'
        return docstrings[''.join(l_opcode)].format(opcode)
    else:
        return docstrings['0' + interpreter_opcodes.mapping[opcode[0]].__name__].format(opcode)



