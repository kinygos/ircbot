from . import helpers


storage = helpers.Storage('memory')

@helpers.commands('set')
def set_text(bot, conn, event):
    try:
        _, word, text = (event.arguments()[0]).split(' ', 3)
    except IndexError:
        return
    with storage as db:
        db[event.target() + word] = text

@helpers.commands('get')
def get_text(bot, conn, event):
    try:
        _, word = (event.arguments()[0]).split(' ', 2)
    except IndexError:
        return
    with storage as db:
        try:
            data = db[event.target() + word]
        except KeyError:
            return
    conn.privmsg(event.target(), data.decode('utf8'))
