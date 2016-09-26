# CHIP8 #
 
## About ##
This is an interpreter for the old Chip-8 programming language, originally designed for the COSMAC VIP and Telmac 1800 microcomputers in the 70s. Read more at [Wikipedia](https://en.wikipedia.org/wiki/CHIP-8). Because it was so close to the metal of these computers, programming a modern interpreter for it has a lot in common with programming an emulator, something I'm interested in learning how to do.

The interpreter uses SDL (only SDL, for now) for input/output, so it should be cross-platform. However it has yet to be tested on anything ohter than Linux.

## Usage ##
To use it make sure you have SDL2, PySDL2, and PIL installed, in addition to Python 3 or above, and execute from the repo: `python3 chip8.py /path/to/program.ch8`
That's it! The original computers that ran this had hex keypads, so use the numpad and the A - F keys for input. If that layout doesn't work for you, for example if you don't have a numpad, then the key layout can be changed manually in platform_sdl.py starting at line 64. Reference the [SDL Keycode Lookup Table](https://wiki.libsdl.org/SDLKeycodeLookup) to get the correct keycodes. I plan to implement a settings file at some point, as well as alternative layouts, so hopefully in future you won't need to use this method.

A pack containing all known Chip-8 programs is available at [chip8.com](http://chip8.com/?page=109). Don't worry, the whole thing is only 320kb!

## Conclusion ##
This whole project is still very much a WIP. There may be bugs, there are many features I still need to implement, and the whole codebase needs a good polish. Sound, for example, is not working yet. However, it is still eminently usable, and I hope you can have some fun anyway!
