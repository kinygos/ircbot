import random

from . import helpers


GREETINGS = ('morning', 'hi', 'hello', 'good morning', 'greetings!')


@helpers.throttling(10, 2)
@helpers.events('join')
def greeting(bot, conn, event):
    if random.random() < 0.8:
        return
    if event.source().startswith('{}!'.format(bot._nickname)):
        conn.privmsg(event.target(), 'Greetings mortals!')
    else:
        nickname = event.source().split('!', 1)[0]
        greet = random.choice(GREETINGS)
        conn.privmsg(event.target(), '{}: {}'.format(nickname, greet))

@helpers.throttling(5, 1)
@helpers.events('pubmsg', 'privmsg')
def say_hi(bot, conn, event):
    if not event.arguments():
        return
    message = event.arguments()[0]
    if message in GREETINGS and random.random() > 0.3:
        nickname = event.source().split('!', 1)[0]
        greet = random.choice(GREETINGS)
        conn.privmsg(event.target(), '{}: {}'.format(nickname, greet))
