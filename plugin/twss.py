import re

from . import helpers


PREFIXES = ['is', 'was', 'so']
DESC = ['really', 'bloody', 'totally', 'proper']
ADVERBS = ['huge', 'massive', 'tiny', 'awesome', 'hard']

prefixes = '|'.join(PREFIXES)
desc = '|'.join(DESC)
adverbs = '|'.join(ADVERBS)

what_she_said = re.compile(r'''
	({prefixes})

	\s+

	(({desc})\s+)?

	({adverbs})
    '''.format(prefixes=prefixes, desc=desc, adverbs=adverbs), re.VERBOSE|re.MULTILINE|re.UNICODE)

@helpers.events('pubmsg', 'privmsg')
@helpers.throttling(5, 2)
def twss(bot, conn, event):
    message = event.arguments()[0]
    if what_she_said.search(message.lower()):
        conn.privmsg(event.target(), "That's what she said!!!")


if __name__ == '__main__':
    import sys
