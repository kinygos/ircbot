import threading
import re

import lxml.html


url_rx = re.compile(r'\b(http[s]?://\S+)[,.]?\b')

last_url = None

def page_title(url, title_callback):
    html = lxml.html.parse(url)
    title = html.find(".//title").text
    if not title:
        title = "no title found"
    title_callback("{} => {}".format(url, title))

def last_url_title(bot, conn, event):
    if not last_url:
        return

    def send_title(message):
        conn.privmsg(event.target(), message)

    t = threading.Thread(target=page_title, args=(last_url, send_title))
    t.start()

def remember_url(bot, conn, event):
    arguments = event.arguments()
    if not arguments:
        return
    rx = url_rx.finditer(arguments[0])
    try:
        url = next(rx).group()
        global last_url
        last_url = url
    except StopIteration:
        pass

def on_pubmsg(bot, conn, event):
    remember_url(bot, conn, event)

def on_privmsg(bot, conn, event):
    remember_url(bot, conn, event)

def colon_title(bot, conn, event):
    last_url_title(bot, conn, event)

def dot_title(bot, conn, event):
    last_url_title(bot, conn, event)
