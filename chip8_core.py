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



