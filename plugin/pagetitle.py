import threading
import re

import lxml.html


url_rx = re.compile(r'\b(http[s]?://\S+)[,.]?\b')

def page_title(url, title_callback):
    html = lxml.html.parse(url)
    title = html.find(".//title").text
    if not title:
        title = "no title found"
    title_callback("{} => {}".format(url, title))

def print_page_url(bot, conn, event):
    arguments = event.arguments()
    if not arguments:
        return

    def send_title(message):
        conn.privmsg(event.target(), message)

    msg = arguments[0]
    for url in url_rx.findall(msg):
        t = threading.Thread(target=page_title, args=(url, send_title))
        t.start()

def on_pubmsg(bot, conn, event):
    print_page_url(bot, conn, event)

def on_privmsg(bot, conn, event):
    print_page_url(bot, conn, event)
