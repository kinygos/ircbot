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
        empty = ()

        for attr_name in dir(plugin):
            if attr_name.startswith('_'):
                continue
            attr = getattr(plugin, attr_name)
            if not isinstance(attr, collections.Callable):
                continue
            for ev_name in getattr(attr, 'events', empty):
                self.handlers['on_' + ev_name].append(attr)
            for cmd_name in getattr(attr, 'commands', empty):
                self.handlers['cmd_' + cmd_name].append(attr)

    def import_plugins(self):
        plugdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                'plugin')
        success = 0
        fail = 0
        self.handlers.clear()
        # before reloading plugins, make sure we have fresh version of helpers
        sys.modules.pop('plugin.helpers', None)
        for fdname in os.listdir(plugdir):
            if not fdname.endswith('.py'):
                continue
            mod_name = fdname.rsplit('.', 1)[0]
            import_name = 'plugin.' + mod_name
            sys.modules.pop(import_name, None)
            try:
                plugin = importlib.import_module(import_name)
            except Exception as e:
                print("Cannot import '{}' plugin: {}".format(mod_name, e))
                fail += 1
                continue
            self.install_plugin(plugin)
            success += 1
        return (success, fail)

    def dispatch(self, bot, c, ev):
        eventtype = ev.eventtype()
        handlers = self.handlers.get('on_' + eventtype, ())
        for handler in handlers:
            try:
                handler(bot, c, ev)
            except Exception as exc:
                print("Plugin error: {}.{} :: {}".format(
                    handler.__module__, handler.__name__, exc))

        arguments = ev.arguments()
        if not arguments or not arguments[0]:
            return
        if arguments[0][0] not in ('.', ':'):
            return
        cmd = 'cmd_' + arguments[0].split(' ', 1)[0][1:]
        handlers = self.handlers.get(cmd, ())
        for handler in handlers:
            try:
                handler(bot, c, ev)
            except Exception as exc:
                print("Plugin error: {}.{} :: {}".format(
                    handler.__module__, handler.__name__, exc))


class Bot(SingleServerIRCBot):
    version = version.VERSION

    def __init__(self, channels, nickname, server, port=6667):
        super(Bot, self).__init__([(server, port)], nickname, nickname)
        self._channels = channels
        self.pmanager = PluginManager()
        (success, fails) = self.pmanager.import_plugins()
        print("Pluings loaded ({} success, {} fail)".format(success, fails))

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
