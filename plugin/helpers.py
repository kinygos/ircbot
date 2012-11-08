import time
import functools


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

throttling_break = object()

def throttling(throttl_time, max_call_count=1):
    def decorator(func):
        func._throttling_time = time.time() - 10000
        func._throttling_count = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            last_call = getattr(func, '_throttling_time', None)
            call_count = getattr(func, '_throttling_count', None)

            tdiff = now - last_call
            if tdiff > throttl_time:
                func._throttling_time = now
                func._throttling_count = 0
            else:
                if call_count >= max_call_count:
                    return throttling_break

            func._throttling_count += 1
            return func(*args, **kwargs)

        return wrapper
    return decorator


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
