# CHIP8 #
 
## About ##
This is an interpreter for the old Chip-8 programming language, originally designed for the COSMAC VIP and Telmac 1800 microcomputers in the 70s. Read more at [Wikipedia](https://en.wikipedia.org/wiki/CHIP-8). Because it was so close to the metal of these computers, programming a modern interpreter for it has a lot in common with programming an emulator, something I'm interested in learning how to do.

The interpreter uses SDL (only SDL, for now) for input/output, so it should be cross-platform. However it has yet to be tested on anything ohter than Linux.

## Usage ##
To use it make sure you have SDL2, PySDL2, and PIL installed, in addition to Python 3 or above. You'll also need a Chip-8 program. A pack containing all known Chip-8 programs is available at [chip8.com](http://chip8.com/?page=109). Don't worry, the whole thing is only 320kb! Finally, execute from the repo: `python3 chip8.py /path/to/program.ch8`.


## Input ##
The original computers that ran this had only hex keypads, layed out like this:

+---+---+---+---+
| 1 | 2 | 3 | C |
+---+---+---+---+
| 4 | 5 | 6 | D |
+---+---+---+---+
| 7 | 8 | 9 | E |
+---+---+---+---+
| A | 0 | B | F |
+---+---+---+---+

Most games used 2, 4, 6, and 8 for up, left, right and down input. The default keymap for the interpreter flips the physical number keys of a modern keypad vertically, so the directions are correct when you press a key, rather than the numbers being correct. You can also use the arrow keys, if you want. The keys A-F on the keyboard do the duty of the hex pad ones.
You can adjust the key layout to your liking by going to chip8.py and editing the KEYMAP dict, starting on line 22. 

## Conclusion ##
This whole project is still very much a WIP. There may be bugs, there are many features I still need to implement, and the whole codebase needs a good polish. Sound, for example, is not working yet. However, it is still eminently usable, and I hope you can have some fun anyway!
