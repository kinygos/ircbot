from . import helpers


@helpers.commands('help')
def help(bot, conn, event):
    nickname = event.source().split('!', 1)[0]
    conn.privmsg(nickname, "{} => https://github.com/husio/ircbot".format(bot.version))
    conn.privmsg(nickname, "type :plugins for complete plugins list")

@helpers.commands('plugins')
def plugins(bot, conn, event):
    nickname = event.source().split('!', 1)[0]
    for plugin, commands in bot.pmanager.handlers.items():
        conn.privmsg(nickname, "{:>18} =>  {}".format(
            plugin, " ".join(str(c) for c in commands)))
