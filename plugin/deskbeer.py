import datetime

from . import helpers

def format_time_left(now, deskbeer_time):
    tdiff = now - deskbeer_time
    diff_sec = int(round(abs(tdiff.days * 86400 + tdiff.seconds)))
    diff_min = int(round(diff_sec / 60))

    if diff_sec <= 1:
        if diff_sec == 0:
            return "less than a minute"
        return "1 minute"
    if diff_min < 45:
        return "{} minutes".format(diff_min)
    if diff_min < 90:
        return "about 1 hour"
    return "about {} hours".format(round(diff_min / 60.0))

def deskbeer_message():
    "every friday, 5pm"
    now = datetime.datetime.now()
    if now.isoweekday() == 1:
        return "Calm down drunkard, it is only Monday afterall!"
    if now.isoweekday() == 2:
        return "Tuesday isn't deskbeer day, " \
               "but definitely feel less bad going to the pub after work."
    if now.isoweekday() == 3:
        return "We're getting there, only 2 days to go!"
    if now.isoweekday() == 4:
        return "If you're a geek it's games night, " \
               "if you're not, have fun with the hangover tomorrow. " \
               "Deskbeer not required."
    if now.isoweekday() == 5:
        deskbeer_time = datetime.datetime(now.year, now.month, now.day, 17)
        if now > deskbeer_time:
            return "Deskbeer should be on it's way or in your belly!"
        time_left = format_time_left(now, deskbeer_time)
        return "Deskbeer needs to be aquired in {}".format(time_left)
    return "Why are you here on the weekend?"

@helpers.commands('deskbeer')
@helpers.throttling(5, 2)
def deskbeer(bot, conn, event):
    conn.privmsg(event.target(), deskbeer_message())
