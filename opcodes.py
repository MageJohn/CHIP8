'''CHIP-8 has 35 opcodes, which are all two bytes long and stored big-endian. The opcodes are listed below in comments, in hexadecimal and with the following symbols:

    NNN: address
    NN: 8-bit constant
    N: 4-bit constant
    X and Y: 4-bit register identifier
'''

import sys
import random


def x0(state, opcode):
    if opcode == 0x00E0:   # 0x00E0 Clears the screen
        state.init_screen()
    elif opcode == 0x00EE: # 0x00EE Returns from a subroutine
        state.pc = state.stack.pop()
    else:                  # Ox0NNN Calls RCA 1802 machine code at address NNN. Not supported here
        sys.exit("Execution of machine code is not supported.")


def x1NNN(state, opcode):  # 0x1NNN Jump to address NNN.
    state.pc = opcode.NNN


def x2NNN(state, opcode):  # 0x2NNN Calls subroutine at address NNN.
    state.stack.append(state.pc)
    state.pc = opcode.NNN


def x3XNN(state, opcode):  # 0x3XNN Skips the next instruction if VX equals NN.
    if state.register[opcode.X] == opcode.NN:
        state.pc = (state.pc + 2) % 0x1000


def x4XNN(state, opcode):  # 0x4XNN Skips the next instruction if VX doesn't equal NN.
    if state.register[opcode.X] != opcode.NN:
        state.pc = (state.pc + 2) % 0x1000


def x5XY0(state, opcode):  # 0x5XY0 Skips the next instruction if VX equals VY.
    if state.register[opcode.X] == state.register[opcode.Y]:
        state.pc = (state.pc + 2) % 0x1000


def x6XNN(state, opcode):  # 0x6XNN Sets VX to NN.
    state.register[opcode.X] = opcode.NN


def x7XNN(state, opcode):  #  0x7XNN Adds NN to VX.
    state.register[opcode.X] = (state.register[opcode.X] + (opcode.NN)) % 0x100


def x8XY0(state, opcode):  # 0x8XY0 Sets VX to the value of VY.
    state.register[opcode.X] = state.register[opcode.Y]


def x8XY1(state, opcode):  # 0x8XY1 Sets VX to VX | VY.
    state.register[opcode.X] = state.register[opcode.X] | state.register[opcode.Y]


def x8XY2(state, opcode):  # 0x8XY2 Sets VX to VX & VY.
    state.register[opcode.X] = state.register[opcode.X] & state.register[opcode.Y]


def x8XY3(state, opcode):  # 0x8XY3 Sets VX to VX ^ VY.
    state.register[opcode.X] = state.register[opcode.X] ^ state.register[opcode.Y]


def x8XY4(state, opcode):  # 0x8XY4 Sets VX to VX + VY. VF is set to 1 if there was a carry, 0 if not.
    state.register[0xF] = int(state.register[opcode.X] + state.register[opcode.Y] > 0xFF)
    state.register[opcode.X] = (state.register[opcode.X] + state.register[opcode.Y]) % 0x100


def x8XY5(state, opcode):  # 0x8XY5 Sets VX to VX - VY. VF is set to 0 when there's a borrow, 1 when not.
    if state.register[opcode.Y] > state.register[opcode.X]:
        state.register[0xF] = 0
        state.register[opcode.X] = 0
    else:
        state.register[0xF] = 1
        state.register[opcode.X] -= state.register[opcode.Y]


def x8XY6(state, opcode):  # 0x8XY6 Set VX to VY >> 1. Set VF to the least significant bit of VY before the operation.
    state.register[0xF] = state.register[opcode.Y] & 1
    state.register[opcode.X] = state.register[opcode.Y] >> 1


def x8XY7(state, opcode):  # 0x8XY7 Set VX to VY - VX. VF is set to 0 when there's a borrow, and 1 when there isn't.
    if state.register[opcode.X] > state.register[opcode.Y]:
        state.register[0xF] = 0
        state.register[opcode.X] = 0
    else:
        state.register[0xF] = 1
        state.register[opcode.X] = state.register[opcode.Y] - state.register[opcode.X]


def x8XYE(state, opcode):  # 0x8XYE Set VX to VY << 1. Set VF to the most significant bit of VY before the operation.
    state.register[0xF] = state.register[opcode.Y] & 0x80
    state.register[opcode.X] = (state.register[opcode.Y] << 1) & 0xFF


def x8(state, opcode):
    mapping = {0x0: x8XY0,
               0x1: x8XY1,
               0x2: x8XY2,
               0x3: x8XY3,
               0x4: x8XY4,
               0x5: x8XY5,
               0x6: x8XY6,
               0x7: x8XY7,
               0xE: x8XYE}

    mapping[opcode[3]](state, opcode)


def x9XY0(state, opcode):  # 0x9XY0 Skips the next instruction if VX doesn't equal VY
    if state.register[opcode.X] != state.register[opcode.Y]:
        state.pc = (state.pc + 2) % 0x1000


def xANNN(state, opcode):  # 0xANNN Sets register I to the address NNN
    state.I = opcode.NNN


def xBNNN(state, opcode):  # 0xBNNN Jumps to the address NNN plus V0
    state.I = (opcode.NNN + state.register[0]) % 0x1000


def xCXNN(state, opcode):  # 0xCXNN Set VX to a random number with a mask of NN
    state.register[opcode.X] = random.randint(0x00, 0xFF) & opcode.NN



def xDXYN(state, opcode):
    # 0xDXYN Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels 
    # and a height of N pixels. Each row of 8 pixels is read as bit-coded
    # starting from memory location I; I value doesn’t change after the
    # execution of this instruction. VF is set to 1 if any screen pixels 
    # are flipped from set to unset when the sprite is drawn, and to 0 if
    # that doesn’t happen
    sprite = [[int(x) for x in format(state.memory[state.I + y], '08b')] for y in range(opcode[3])]

    state.register[0xF] = 0

    width = state.SCREEN_WIDTH

    for y in range(len(sprite)):
        for x in range(len(sprite[0])):
            screen_y = state.register[opcode.Y] + y
            screen_x = state.register[opcode.X] + x
            try:
                state.register[0xF] = state.register[0xF] or state.screen[screen_y*width + screen_x] & sprite[y][x]
                state.screen[screen_y*width + screen_x] = state.screen[screen_y*width + screen_x] ^ sprite[y][x]
            except IndexError:
                break



def xE(state, opcode):
    if opcode[2:] == 0x9E: # 0xEX9E Skip the following instruction if the key corresponding to the hex value stored in VX is pressed.
        state.pc = (state.pc + 2 * state.keypad[opcode.X]) % 0x1000
    else:                  # 0xEXA1 Skip the following instruction if the key corresponding to the hex value stored in VX is not pressed.
        state.pc = (state.pc + 2 * (not state.keypad[opcode.X])) % 0x1000


def xFX07(state, opcode):  # 0xFX07 Store the current value of the delay timer in register VX
    state.register[opcode.X] = state.delay


def xFX0A(state, opcode):  # 0xFX0A Wait for a keypress and store the result in register VX
    if 1 in state.keypad:
        state.register[opcode.X] = state.keypad.index(1)
    else:
        state.pc -= 2


def xFX15(state, opcode):  # 0xFX15 Set the delay timer to the value of VX
    state.delay = state.register[opcode.X]


def xFX18(state, opcode):  # 0xFX18 Set the sound timer to the value of VX
    state.sound = state.register[opcode.X]


def xFX1E(state, opcode):  # 0xFX1E Add the value stored in VX to register I
    state.register[0xF] = int(state.I + state.register[opcode.X] > 0xFFF)
    state.I = (state.I + state.register[opcode.X]) % 0x1000


def xFX29(state, opcode):  # 0xFX29 Set I to the memory addres of the sprite data corresponding to the hexadecimal digit stored in VX
    state.I = state.register[opcode.X] * 5


def xFX33(state, opcode):  # 0xFX33 Store the binary-coded decimal equivalent of the value stored in VX at addresses I, I+1, and I+2
    dec_x = format(state.register[opcode.X], '03d')
    for i in range(3):
        state.memory[state.I + i] = int(dec_x[i])


def xFX55(state, opcode):  # 0xFX55 Store the values of registers V0 to VX inclusive in memory starting at address I. I is set to I + X + 1 after the operation.
    for register in range(opcode.X+1):
        state.memory[state.I+register] = state.register[opcode.X]
    state.I = state.I + opcode.X + 1


def xFX65(state, opcode): # 0xFX65 Fill registers V0 to VX inclusive with the values stored in memory starting at address I. I is set to I + X + 1 after the operation.
    for register in range(opcode.X+1):
        state.register[register] = state.memory[state.I+register]
    state.I = state.I + opcode.X + 1


def xF(state, opcode):
    mapping = {0x07: xFX07,
               0x0A: xFX0A,
               0x15: xFX15,
               0x18: xFX18,
               0x1E: xFX1E,
               0x29: xFX29,
               0x33: xFX33,
               0x55: xFX55,
               0x65: xFX65}
    mapping[opcode[2:]](state, opcode)

mapping = {0x0: x0,
           0x1: x1NNN,
           0x2: x2NNN,
           0x3: x3XNN,
           0x4: x4XNN,
           0x5: x5XY0,
           0x6: x6XNN,
           0x7: x7XNN,
           0x8: x8,
           0x9: x9XY0,
           0xA: xANNN,
           0xB: xBNNN,
           0xC: xCXNN,
           0xD: xDXYN,
           0xE: xE,
           0xF: xF}