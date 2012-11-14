import datetime

from . import helpers


@helpers.throttling(60, 1)
@helpers.commands('lunch')
def urb(bot, conn, event):
    now = datetime.datetime.now()
    if now.hour < 12:
        conn.privmsg(event.target(), "No, it's still to early :(")
    elif now.hour > 13:
        conn.privmsg(event.target(), "No, it's already too late :(")
    else:
        conn.privmsg(event.target(), "Yes, let's go!")
