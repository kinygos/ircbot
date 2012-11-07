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
