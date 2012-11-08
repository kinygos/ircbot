import urllib.request
import re


from . import helpers

definition_rx = re.compile(r'<div class="definition">(.*?)</div>')
uri = 'http://www.urbandictionary.com/define.php?term='

def urbandictionary(word):
    page = urllib.request.urlopen(uri + urllib.parse.quote(word))
    html = page.read().decode('utf8')
    try:
        res = next(definition_rx.finditer(html))
        return res.groups()[0]
    except StopIteration:
        return "I would tell you but I can't be arsed."

def urbandict(term):
    if not term:
        return "Missing term"
    definition = urbandictionary(term)
    if not definition:
        return 'You done made up {}'.format(term)
    return '{} - {}'.format(term, definition)

@helpers.throttling(5, 2)
@helpers.commands('urb', 'urbandict')
def urb(bot, conn, event):
    term = event.arguments()[0].split(' ', 1)[1]
    res = urbandict(term)
    if len(res) > 450:
        res = res[:450] + '...'
    conn.privmsg(event.target(), res)
