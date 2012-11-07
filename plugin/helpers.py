def commands(*commands):
    def wrapper(func):
        func.commands = commands
        return func
    return wrapper

def events(*events):
    def wrapper(func):
        func.events = events
        return func
    return wrapper

COLORS = {
        'aqua': 11,
        'black': 1,
        'blue': 12,
        'bluecyan': 10,
        'brown': 5,
        'cyan': 11,
        'fuchsia': 13,
        'gray': 14,
        'green': 3,
        'grey': 14,
        'lightgray': 15,
        'lightgreen': 9,
        'lightgrey': 15,
        'lightpurple': 13,
        'lime': 9,
        'maroon': 5,
        'navy': 2,
        'olive': 7,
        'pink': 13,
        'purple': 6,
        'red': 4,
        'royal': 12,
        'silver': 15,
        'teal': 10,
        'violet': 6,
        'white': 0,
        'yellow': 8,
 }

def color(c, message=''):
    if c in COLORS:
        c = COLORS[c]
    return "{}{}{}".format(chr(3), c, message)
