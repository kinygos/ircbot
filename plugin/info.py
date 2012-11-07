from . import helpers


@helpers.commands('help', 'version')
def help(bot, conn, event):
    conn.privmsg(event.target(), "{} => https://github.com/husio/ircbot".format(bot.version))

@helpers.commands('plugins')
def plugins(bot, conn, event):
    nickname = event.source().split('!', 1)[0]
    for plugin, commands in bot.pmanager.handlers.items():
        conn.privmsg(nickname, "{:>18} =>  {}".format(
            plugin, " ".join(str(c) for c in commands)))
