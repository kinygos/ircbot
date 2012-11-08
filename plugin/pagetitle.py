import threading
import re

import lxml.html

from . import helpers


url_rx = re.compile(r'\b(http[s]?://\S+)[,.]?\b')

latest_urls = {}

def page_title(url, title_callback):
    html = lxml.html.parse(url)
    title = html.find(".//title").text.strip()
    if not title:
        title = "No title found"
    title_callback(title)

@helpers.commands('title')
def last_url_title(bot, conn, event):
    if not latest_urls.get(event.target(), None):
        return

    def send_title(message):
        conn.privmsg(event.target(), message)

    t = threading.Thread(target=page_title,
            args=(latest_urls[event.target()], send_title))
    t.start()

@helpers.events('pubmsg', 'privmsg')
@helpers.throttling(10, 2)
def remember_url(bot, conn, event):
    arguments = event.arguments()
    if not arguments:
        return
    rx = url_rx.finditer(arguments[0])
    try:
        latest_urls[event.target()] = next(rx).group()
    except StopIteration:
        pass


