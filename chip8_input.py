from collections import namedtuple

_KEYS = ("\b",
         "\t",
         "\r",
         "escape",
         "space",
         "!",
         "\"",
         "#",
         "$",
         "%",
         "&",
         "'",
         "(",
         ")",
         "*",
         "+",
         ",",
         "-",
         ".",
         "/",
         "0",
         "1",
         "2",
         "3",
         "4",
         "5",
         "6",
         "7",
         "8",
         "9",
         ":",
         ";",
         "<",
         "=",
         ">",
         "?",
         "@",
         "[",
         "\\",
         "]",
         "^",
         "_",
         "`",
         "a",
         "b",
         "c",
         "d",
         "e",
         "f",
         "g",
         "h",
         "i",
         "j",
         "k",
         "l",
         "m",
         "n",
         "o",
         "p",
         "q",
         "r",
         "s",
         "t",
         "u",
         "v",
         "w",
         "x",
         "y",
         "z",
         "delete",
         "capslock",
         "f1",
         "f2",
         "f3",
         "f4",
         "f5",
         "f6",
         "f7",
         "f8",
         "f9",
         "f10",
         "f11",
         "f12",
         "printscreen",
         "scrolllock",
         "pause",
         "insert",
         "home",
         "pageup",
         "end",
         "pagedown",
         "right",
         "left",
         "down",
         "up",
         "numlockclear",
         "kp_divide",
         "kp_multiply",
         "kp_minus",
         "kp_plus",
         "kp_enter",
         "kp_1",
         "kp_2",
         "kp_3",
         "kp_4",
         "kp_5",
         "kp_6",
         "kp_7",
         "kp_8",
         "kp_9",
         "kp_0",
         "kp_period",
         "kp_equals",
         "f13",
         "f14",
         "f15",
         "f16",
         "f17",
         "f18",
         "f19",
         "f20",
         "f21",
         "f22",
         "f23",
         "f24",
         "select",
         "stop",
         "again",
         "undo",
         "cut",
         "copy",
         "paste",
         "find",
         "kp_comma",
         "kp_equalsas400",
         "alterase",
         "sysreq",
         "cancel",
         "clear",
         "prior",
         "return2",
         "separator",
         "out",
         "oper",
         "clearagain",
         "crsel",
         "exsel",
         "kp_00",
         "kp_000",
         "thousandsseparator",
         "decimalseparator",
         "currencyunit",
         "currencysubunit",
         "kp_leftparen",
         "kp_rightparen",
         "kp_leftbrace",
         "kp_rightbrace",
         "kp_tab",
         "kp_backspace",
         "kp_a",
         "kp_b",
         "kp_c",
         "kp_d",
         "kp_e",
         "kp_f",
         "kp_xor",
         "kp_percent",
         "kp_less",
         "kp_greater",
         "kp_ampersand",
         "kp_dblampersand",
         "kp_verticalbar",
         "kp_dblverticalbar",
         "kp_colon",
         "kp_hash",
         "kp_space",
         "kp_at",
         "kp_exclam",
         "kp_memstore",
         "kp_memrecall",
         "kp_memclear",
         "kp_memadd",
         "kp_memsubtract",
         "kp_memmultiply",
         "kp_memdivide",
         "kp_plusminus",
         "kp_clear",
         "kp_clearentry",
         "kp_binary",
         "kp_octal",
         "kp_decimal",
         "kp_hexadecimal")

_MODIFIERS = ("ctrl",
              "shift",
              "alt",
              "super")

_SYNONYMS = {'control':   'ctrl',
             'ctl':       'ctrl',
             'cmd':       'super',
             'command':   'super',
             'apple':     'super',
             'windows':   'super',
             'gui':       'super',
             'esc':       'escape',
             'del':       'delete',
             ' ':         'space',
             'spacebar':  'space',
             'backspace': '\b',
             'tab':       '\t',
             'return':    '\r',
             'enter':     '\r',
             'backslash': '\\'}

KEYDOWN = 1
KEYUP = 0
QUIT = -1


Event = namedtuple('Event', ('type', 'keycode'))


def normalize_keycode(keycode):
    '''Try to normalize key strings. Makes the key string lowercase,
replace common synonyms, and reorders the modifiers with sorted()'''
    keycode = keycode.lower()
    key_parts = keycode.split('+')

    if len(key_parts) > 0:

        if key_parts[-1] in _MODIFIERS:
            raise KeyCodeError("Can't bind modifier directly")

        if (key_parts[-1].startswith('keypad_') or
            key_parts[-1].startswith('numpad_')):

            key_parts[-1] = 'kp_' + key_parts[-1][7:]

        if not key_parts[-1] in _KEYS:

            if key_parts[-1] in _SYNONYMS.keys():

                key_parts[-1] = _SYNONYMS[key_parts[-1]]

            else:

                raise KeyCodeError('Unknown key: {}'.format(key_parts[-1]))

        if len(key_parts) > 1:

            for i, m in enumerate(key_parts[:-1]):

                if not m in _MODIFIERS:

                    if m in _SYNONYMS.keys():

                        key_parts[i] = _SYNONYMS[m]

                    else:

                        raise KeyCodeError('Unknown modifier: {}'.format(m))

            sorted_parts = sorted(key_parts[:-1])
            sorted_parts.append(key_parts[-1])
            key_parts = sorted_parts

    else:

        raise KeyCodeError('Empty key string')

    return '+'.join(key_parts)


class KeyCodeError(Exception):
    '''Raised when attempting to process an invalid keycode'''
    def __init__(self, message):
        self.message = message

class UnhandledActionError(Exception):
    '''Raised when a keymap dictionary returns an unhandled action string'''
    def __init__(self, message, action):
        self.message = message
        self.action = action


