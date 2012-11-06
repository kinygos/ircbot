#! /usr/bin/env python

import collections
import importlib
import os
import sys

from irc.bot import SingleServerIRCBot

import version



class PluginManager:
    def __init__(self):
        self.handlers = collections.defaultdict(list)

    def install_plugin(self, plugin):
        for attr_name in dir(plugin):
            if attr_name.startswith('_'):
                continue
            attr = getattr(plugin, attr_name)
            if isinstance(attr, collections.Callable):
                self.handlers[attr_name].append(attr)

    def import_plugins(self):
        plugdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                'plugin')
        for fdname in os.listdir(plugdir):
            if not fdname.endswith('.py'):
                continue
            mod_name = fdname.rsplit('.', 1)[0]
            try:
                plugin = importlib.import_module('plugin.' + mod_name)
            except ImportError as e:
                print("Cannot import {} plugin: {}".format(mod_name, e))
                continue
            self.install_plugin(plugin)

    def dispatch(self, bot, c, e):
        eventtype = e.eventtype()
        handlers = self.handlers.get('on_' + eventtype, ())
        for handler in handlers:
            handler(bot, c, e)

        arguments = e.arguments()
        if not arguments:
            return
        if arguments[0].startswith('.'):
            cmd = 'dot_' + arguments[0].split(' ', 1)[0][1:]
        elif arguments[0].startswith(':'):
            cmd = 'colon_' + arguments[0].split(' ', 1)[0][1:]
        else:
            return
        handlers = self.handlers.get(cmd, ())
        for handler in handlers:
            handler(bot, c, e)


class Bot(SingleServerIRCBot):
    version = version.VERSION

    def __init__(self, channels, nickname, server, port=6667):
        super(Bot, self).__init__([(server, port)], nickname, nickname)
        self._channels = channels
        self.pmanager = PluginManager()
        self.pmanager.import_plugins()

    def _dispatcher(self, c, e):
        super(SingleServerIRCBot, self)._dispatcher(c, e)
        self.pmanager.dispatch(self, c, e)

    def on_welcome(self, c, e):
        for channel in self._channels:
            c.join(channel)


def main():
    if len(sys.argv) < 4:
        sys.exit("Usage: testbot <server[:port]> <nickname> <channel> [<channel>, ... ]")

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            sys.exit("Error: Erroneous port.")
    else:
        port = 6667
    nickname = sys.argv[2]
    channels = [c  if c.startswith('#') else '#' + c for c in sys.argv[3:]]

    bot = Bot(channels, nickname, server, port)
    bot.start()


if __name__ == "__main__":
    main()
