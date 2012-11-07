from . import helpers


@helpers.commands('reload')
def reload(bot, conn, event):
    (success, fails) = bot.pmanager.import_plugins()
    conn.privmsg(event.target(),
            "Pluings reloaded ({} success, {} fail)".format(success, fails))
