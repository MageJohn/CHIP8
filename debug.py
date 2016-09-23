import chip8_core

def printscreen(screen):
    '''Utility to print out a screen array such as State.screen'''
    for y in range(len(screen[0])):
        for x in range(len(screen)):
            print('0' if screen[x][y] else '.', end='')
        print()


def printstate(state, memslice=None):
    printscreen(state.screen)

    print("\nRegisters:")
    for i in range(len(state.register)):
        print('V{:X}'.format(i), end=' ')
    print()
    for i in state.register:
        print(format(i, '02X'), end=' ')
    print('\n')

    print('Keypad')
    keys_on_off = [format(i, 'X') if state.keypad[i] else ' ' for i in range(16)]
    print('''
+---+---+---+---+
| {0[1]} | {0[2]} | {0[3]} | {0[12]} |
+---+---+---+---+
| {0[4]} | {0[5]} | {0[6]} | {0[13]} |
+---+---+---+---+
| {0[7]} | {0[8]} | {0[9]} | {0[14]} |
+---+---+---+---+
| {0[10]} | {0[0]} | {0[11]} | {0[15]} |
+---+---+---+---+
'''.format(keys_on_off))

    print('I   pc  delay sound')
    print('{:03X} {:03X} {:02X}    {:02X}'.format(state.I, state.pc, state.delay, state.sound))
    
    print('\nLast opcode  Current opcode')
    state.pc -= 2
    print('0x{0:04X}       0x{1:04X}'.format(chip8_core.read_opcode(state), chip8_core.read_opcode(state)))
    state.pc -=2
    
    for i in state.stack:
        print(format(i, '03X'), end=' ')
    print()

def step(state):
    chip8_core.execute_opcode(state, chip8_core.read_opcode(state))
    if state.delay > 0: 
        state.delay -= 1
    if state.sound > 0:
        state.sound -=1
    printstate(state)
