import collections


def colon_help(bot, conn, event):
    nickname = event.source().split('!', 1)[0]
    conn.privmsg(nickname, "{} => https://github.com/husio/ircbot".format(bot.version))
    conn.privmsg(nickname, "type :plugins for complete plugins list")

def colon_plugins(bot, conn, event):
    nickname = event.source().split('!', 1)[0]
    plugs = collections.defaultdict(set)
    for name, handlers in bot.pmanager.handlers.items():
        for handler in handlers:
            plugin = handler.__module__
            if handler.__name__.startswith('dot_'):
                cmd = '.{}'.format(handler.__name__[4:])
            elif handler.__name__.startswith('colon_'):
                cmd = ':{}'.format(handler.__name__[6:])
            elif handler.__name__.startswith('on_'):
                cmd = 'event-{}'.format(handler.__name__[3:])
            else:
                continue
            plugs[plugin].add(cmd)

    for plugin, commands in plugs.items():
        conn.privmsg(nickname, "{:>18} =>  {}".format(plugin, "   ".join(commands)))
