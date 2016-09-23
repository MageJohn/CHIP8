#!/usr/bin/python3
import sys
import time
import random
import sdl2.ext

import opcodes

SCREEN_X = 64
SCREEN_Y = 32

class State():
    def __init__(self, program):
        self.program = program
        self.register = [0x00] * 16 # 16 registers, each 8 bits. Reigisters go from V0 - VF, but VF doubles as a carry flag.
        self.I = 0x0000 # The address register. 16 bits.
        self.pc = 0x200  # Points to the current opcode
        self.delay = 0x00 # When set by 0xFX07, counts down at 60hz
        self.sound = 0x00 # When set by 0xFX18, counts down at 60hz while emitting a tone.
        self.stack = []
        self.keypad = [0] * 16
        self.FONT = (0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
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

        self.init_memory()
        self.init_screen()


    def init_memory(self, locn=0x1000, progstart=0x200):
        '''Initialise the address space with self.program. locn is the number of memory locations. progstart is where the program starts in memory.'''
        memory = [0x00] * locn # Default 4096 (0x1000) memory locations, each 8 bits (1 byte).
        for i, byte in enumerate(self.program):
            memory[progstart+i] = byte

        for i, byte in enumerate(self.FONT): # The font is accessed by opcode 0xFX29
            memory[0+i] = byte

        self.memory = memory


    def init_screen(self):
        self.screen = [[0x00]*SCREEN_Y for x in range(SCREEN_X)]


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


def read_opcode(state):
    '''Return the bytes pointed at by state.pc and state.pc + 1. Advance state.pc'''
    pc = state.pc
    state.pc += 2
    opcode = state.memory[pc:pc+2]
    return Opcode((opcode[0] << 8) + opcode[1])

    
def execute_opcode(state, opcode):
    '''Perform the opcode on state.'''
    opcodes.mapping[opcode[0]](state, opcode)
