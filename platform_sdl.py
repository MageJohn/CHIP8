import time
import sys
import io
import ctypes

from math import sin, pi

import sdl2
import sdl2.ext
from PIL import Image

import chip8_input

SDL_TO_GENERIC = {sdl2.SDLK_BACKSPACE: "\b",
sdl2.SDLK_TAB: "\t",
sdl2.SDLK_RETURN: "\r",
sdl2.SDLK_ESCAPE: "escape",
sdl2.SDLK_SPACE: "space",
sdl2.SDLK_EXCLAIM: "!",
sdl2.SDLK_QUOTEDBL: "\"",
sdl2.SDLK_HASH: "#",
sdl2.SDLK_DOLLAR: "$",
sdl2.SDLK_PERCENT: "%",
sdl2.SDLK_AMPERSAND: "&",
sdl2.SDLK_QUOTE: "'",
sdl2.SDLK_LEFTPAREN: "(",
sdl2.SDLK_RIGHTPAREN: ")",
sdl2.SDLK_ASTERISK: "*",
sdl2.SDLK_PLUS: "+",
sdl2.SDLK_COMMA: ",",
sdl2.SDLK_MINUS: "-",
sdl2.SDLK_PERIOD: ".",
sdl2.SDLK_SLASH: "/",
sdl2.SDLK_0: "0",
sdl2.SDLK_1: "1",
sdl2.SDLK_2: "2",
sdl2.SDLK_3: "3",
sdl2.SDLK_4: "4",
sdl2.SDLK_5: "5",
sdl2.SDLK_6: "6",
sdl2.SDLK_7: "7",
sdl2.SDLK_8: "8",
sdl2.SDLK_9: "9",
sdl2.SDLK_COLON: ":",
sdl2.SDLK_SEMICOLON: ";",
sdl2.SDLK_LESS: "<",
sdl2.SDLK_EQUALS: "=",
sdl2.SDLK_GREATER: ">",
sdl2.SDLK_QUESTION: "?",
sdl2.SDLK_AT: "@",
sdl2.SDLK_LEFTBRACKET: "[",
sdl2.SDLK_BACKSLASH: "\\",
sdl2.SDLK_RIGHTBRACKET: "]",
sdl2.SDLK_CARET: "^",
sdl2.SDLK_UNDERSCORE: "_",
sdl2.SDLK_BACKQUOTE: "`",
sdl2.SDLK_a: "a",
sdl2.SDLK_b: "b",
sdl2.SDLK_c: "c",
sdl2.SDLK_d: "d",
sdl2.SDLK_e: "e",
sdl2.SDLK_f: "f",
sdl2.SDLK_g: "g",
sdl2.SDLK_h: "h",
sdl2.SDLK_i: "i",
sdl2.SDLK_j: "j",
sdl2.SDLK_k: "k",
sdl2.SDLK_l: "l",
sdl2.SDLK_m: "m",
sdl2.SDLK_n: "n",
sdl2.SDLK_o: "o",
sdl2.SDLK_p: "p",
sdl2.SDLK_q: "q",
sdl2.SDLK_r: "r",
sdl2.SDLK_s: "s",
sdl2.SDLK_t: "t",
sdl2.SDLK_u: "u",
sdl2.SDLK_v: "v",
sdl2.SDLK_w: "w",
sdl2.SDLK_x: "x",
sdl2.SDLK_y: "y",
sdl2.SDLK_z: "z",
sdl2.SDLK_DELETE: "delete",
sdl2.SDLK_CAPSLOCK: "capslock",
sdl2.SDLK_F1: "f1",
sdl2.SDLK_F2: "f2",
sdl2.SDLK_F3: "f3",
sdl2.SDLK_F4: "f4",
sdl2.SDLK_F5: "f5",
sdl2.SDLK_F6: "f6",
sdl2.SDLK_F7: "f7",
sdl2.SDLK_F8: "f8",
sdl2.SDLK_F9: "f9",
sdl2.SDLK_F10: "f10",
sdl2.SDLK_F11: "f11",
sdl2.SDLK_F12: "f12",
sdl2.SDLK_PRINTSCREEN: "printscreen",
sdl2.SDLK_SCROLLLOCK: "scrolllock",
sdl2.SDLK_PAUSE: "pause",
sdl2.SDLK_INSERT: "insert",
sdl2.SDLK_HOME: "home",
sdl2.SDLK_PAGEUP: "pageup",
sdl2.SDLK_END: "end",
sdl2.SDLK_PAGEDOWN: "pagedown",
sdl2.SDLK_RIGHT: "right",
sdl2.SDLK_LEFT: "left",
sdl2.SDLK_DOWN: "down",
sdl2.SDLK_UP: "up",
sdl2.SDLK_NUMLOCKCLEAR: "numlockclear",
sdl2.SDLK_KP_DIVIDE: "kp_divide",
sdl2.SDLK_KP_MULTIPLY: "kp_multiply",
sdl2.SDLK_KP_MINUS: "kp_minus",
sdl2.SDLK_KP_PLUS: "kp_plus",
sdl2.SDLK_KP_ENTER: "kp_enter",
sdl2.SDLK_KP_1: "kp_1",
sdl2.SDLK_KP_2: "kp_2",
sdl2.SDLK_KP_3: "kp_3",
sdl2.SDLK_KP_4: "kp_4",
sdl2.SDLK_KP_5: "kp_5",
sdl2.SDLK_KP_6: "kp_6",
sdl2.SDLK_KP_7: "kp_7",
sdl2.SDLK_KP_8: "kp_8",
sdl2.SDLK_KP_9: "kp_9",
sdl2.SDLK_KP_0: "kp_0",
sdl2.SDLK_KP_PERIOD: "kp_period",
sdl2.SDLK_KP_EQUALS: "kp_equals",
sdl2.SDLK_F13: "f13",
sdl2.SDLK_F14: "f14",
sdl2.SDLK_F15: "f15",
sdl2.SDLK_F16: "f16",
sdl2.SDLK_F17: "f17",
sdl2.SDLK_F18: "f18",
sdl2.SDLK_F19: "f19",
sdl2.SDLK_F20: "f20",
sdl2.SDLK_F21: "f21",
sdl2.SDLK_F22: "f22",
sdl2.SDLK_F23: "f23",
sdl2.SDLK_F24: "f24",
sdl2.SDLK_SELECT: "select",
sdl2.SDLK_STOP: "stop",
sdl2.SDLK_AGAIN: "again",
sdl2.SDLK_UNDO: "undo",
sdl2.SDLK_CUT: "cut",
sdl2.SDLK_COPY: "copy",
sdl2.SDLK_PASTE: "paste",
sdl2.SDLK_FIND: "find",
sdl2.SDLK_KP_COMMA: "kp_comma",
sdl2.SDLK_KP_EQUALSAS400: "kp_equalsas400",
sdl2.SDLK_ALTERASE: "alterase",
sdl2.SDLK_SYSREQ: "sysreq",
sdl2.SDLK_CANCEL: "cancel",
sdl2.SDLK_CLEAR: "clear",
sdl2.SDLK_PRIOR: "prior",
sdl2.SDLK_RETURN2: "return2",
sdl2.SDLK_SEPARATOR: "separator",
sdl2.SDLK_OUT: "out",
sdl2.SDLK_OPER: "oper",
sdl2.SDLK_CLEARAGAIN: "clearagain",
sdl2.SDLK_CRSEL: "crsel",
sdl2.SDLK_EXSEL: "exsel",
sdl2.SDLK_KP_00: "kp_00",
sdl2.SDLK_KP_000: "kp_000",
sdl2.SDLK_THOUSANDSSEPARATOR: "thousandsseparator",
sdl2.SDLK_DECIMALSEPARATOR: "decimalseparator",
sdl2.SDLK_CURRENCYUNIT: "currencyunit",
sdl2.SDLK_CURRENCYSUBUNIT: "currencysubunit",
sdl2.SDLK_KP_LEFTPAREN: "kp_leftparen",
sdl2.SDLK_KP_RIGHTPAREN: "kp_rightparen",
sdl2.SDLK_KP_LEFTBRACE: "kp_leftbrace",
sdl2.SDLK_KP_RIGHTBRACE: "kp_rightbrace",
sdl2.SDLK_KP_TAB: "kp_tab",
sdl2.SDLK_KP_BACKSPACE: "kp_backspace",
sdl2.SDLK_KP_A: "kp_a",
sdl2.SDLK_KP_B: "kp_b",
sdl2.SDLK_KP_C: "kp_c",
sdl2.SDLK_KP_D: "kp_d",
sdl2.SDLK_KP_E: "kp_e",
sdl2.SDLK_KP_F: "kp_f",
sdl2.SDLK_KP_XOR: "kp_xor",
sdl2.SDLK_KP_PERCENT: "kp_percent",
sdl2.SDLK_KP_LESS: "kp_less",
sdl2.SDLK_KP_GREATER: "kp_greater",
sdl2.SDLK_KP_AMPERSAND: "kp_ampersand",
sdl2.SDLK_KP_DBLAMPERSAND: "kp_dblampersand",
sdl2.SDLK_KP_VERTICALBAR: "kp_verticalbar",
sdl2.SDLK_KP_DBLVERTICALBAR: "kp_dblverticalbar",
sdl2.SDLK_KP_COLON: "kp_colon",
sdl2.SDLK_KP_HASH: "kp_hash",
sdl2.SDLK_KP_SPACE: "kp_space",
sdl2.SDLK_KP_AT: "kp_at",
sdl2.SDLK_KP_EXCLAM: "kp_exclam",
sdl2.SDLK_KP_MEMSTORE: "kp_memstore",
sdl2.SDLK_KP_MEMRECALL: "kp_memrecall",
sdl2.SDLK_KP_MEMCLEAR: "kp_memclear",
sdl2.SDLK_KP_MEMADD: "kp_memadd",
sdl2.SDLK_KP_MEMSUBTRACT: "kp_memsubtract",
sdl2.SDLK_KP_MEMMULTIPLY: "kp_memmultiply",
sdl2.SDLK_KP_MEMDIVIDE: "kp_memdivide",
sdl2.SDLK_KP_PLUSMINUS: "kp_plusminus",
sdl2.SDLK_KP_CLEAR: "kp_clear",
sdl2.SDLK_KP_CLEARENTRY: "kp_clearentry",
sdl2.SDLK_KP_BINARY: "kp_binary",
sdl2.SDLK_KP_OCTAL: "kp_octal",
sdl2.SDLK_KP_DECIMAL: "kp_decimal",
sdl2.SDLK_KP_HEXADECIMAL: "kp_hexadecimal"}

SDL_KMOD_TO_MOD = {sdl2.KMOD_NONE: "",
                  sdl2.KMOD_LCTRL: "ctrl+",
                  sdl2.KMOD_LSHIFT: "shift+",
                  sdl2.KMOD_LALT: "alt+",
                  sdl2.KMOD_LGUI: "super+",
                  sdl2.KMOD_RCTRL: "ctrl+",
                  sdl2.KMOD_RSHIFT: "shift+",
                  sdl2.KMOD_RALT: "alt+",
                  sdl2.KMOD_RGUI: "super+"}


class Interface:
    def __init__(self, state, option_dict):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO|sdl2.SDL_INIT_AUDIO) != 0:
            sys.exit("SDL_Init failed: {}".format(sdl2.SDL_GetError()))

        self.option_dict = option_dict

        self.video = Video(self, state)
        self.input = Input()
        self.audio = Audio(self)


class Video:
    def __init__(self, interface, state):
        # This class wraps SDL2 video.
        options = interface.option_dict['window']
        self.palette = options['palette']

        window_scale = options['window_scale']
        program_name = options['title']

        win_size = (state.SCREEN_WIDTH*window_scale, 
                    state.SCREEN_HEIGHT*window_scale)

        self._window = sdl2.ext.Window(program_name, 
                                       size=win_size,
                                       flags=sdl2.SDL_WINDOW_RESIZABLE)
        self._window.show()

        logical_size = (state.SCREEN_WIDTH,
                        state.SCREEN_HEIGHT)

        self._renderer = sdl2.ext.Renderer(self._window, logical_size=logical_size)
        self._texture_renderer = sdl2.ext.TextureSpriteRenderSystem(self._renderer)
        self._sprite_factory = sdl2.ext.SpriteFactory(renderer=self._renderer)

    def update_screen(self, state):
        im_screen = Image.new('RGB', 
                              (state.SCREEN_WIDTH, 
                               state.SCREEN_HEIGHT))
        im_screen.putdata([self.palette[p] for p in state.screen])
        bytesio_screen = io.BytesIO()
        im_screen.save(bytesio_screen, format='BMP')
        bytesio_screen.seek(0)

        texture = self._sprite_factory.from_object(bytesio_screen)
        self._texture_renderer.render(texture, x=0, y=0)



class Input:
    def get_events(self):
        sdl2_events = sdl2.ext.get_events()
        generic_events = []
        for event in sdl2_events:
            if event.type == sdl2.SDL_QUIT:
                generic_events.append(chip8_input.Event(chip8_input.QUIT, ''))
                return generic_events
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key in SDL_TO_GENERIC.keys():
                    keycode = chip8_input.normalize_keycode(self._modstate() +
                                                SDL_TO_GENERIC[key])
                    generic_events.append(chip8_input.Event(chip8_input.KEYDOWN, keycode))
            elif event.type == sdl2.SDL_KEYUP:
                key = event.key.keysym.sym
                if key in SDL_TO_GENERIC.keys():
                    keycode = chip8_input.normalize_keycode(self._modstate() +
                                                SDL_TO_GENERIC[key])
                    generic_events.append(chip8_input.Event(chip8_input.KEYUP, keycode))
                                          
        return tuple(generic_events)

    def _modstate(self):
        modstate = sdl2.SDL_GetModState()
        string = []
        for k in SDL_KMOD_TO_MOD.keys():
            string.append(SDL_KMOD_TO_MOD[modstate & k])
        return ''.join(string)


class Audio:
    def __init__(self, interface):
        self._samples_left = 0
        samples_per_second = 44100

        options = interface.option_dict['sound']
        self._amplitude = int(options['volume'] * 127)
        self._tonehz = options['tonehz']

        if options['wavetype'] == 'square':
            self._phase = 0
            self._running_sample_index = 0
            square_wave_period = samples_per_second / self._tonehz
            self._half_square_wave_period = int(square_wave_period / 2)

            self._generate_sample = self._generate_square
        elif options['wavetype'] == 'sine':
            self._v = 0
            self._generate_sample = self._generate_sine

        audio_callback = sdl2.SDL_AudioCallback(self._callback)
        self._spec = sdl2.SDL_AudioSpec(freq=samples_per_second,
                                        aformat=sdl2.AUDIO_S8,
                                        channels=1,
                                        samples=256,
                                        callback=audio_callback)

        self._devid = sdl2.SDL_OpenAudioDevice(None, 0, self._spec, self._spec, 0)
        sdl2.SDL_PauseAudioDevice(self._devid, 0)


    def _generate_sine(self):
        sample = int(self._amplitude * 
                     sin(self._v * 2 * pi / self._spec.freq))
        self._v += self._tonehz
        return sample


    def _generate_square(self):
        self._running_sample_index += 1
        if self._running_sample_index % self._half_square_wave_period == 0:
            self._phase += 1
        sample = self._amplitude  if self._phase % 2 else -self._amplitude
        return sample


    def _callback(self, notused, stream, length):
        for i in range(length):
            if self._samples_left > 0:
                sample = self._generate_sample()
                stream[i] = ctypes.c_ubyte(sample)
                self._samples_left -= 1
            else:
                stream[i] = ctypes.c_ubyte(0)


    def beep(self, length):
        '''Beep for length milliseconds'''
        sdl2.SDL_LockAudioDevice(self._devid)
        self._samples_left += int(self._spec.freq / 1000 * length)
        sdl2.SDL_UnlockAudioDevice(self._devid)
