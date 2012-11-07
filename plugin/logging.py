import datetime
import sqlite3

from . import helpers


class Storage:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.ensure_table_exist()

    def ensure_table_exist(self):
        with self as c:
            c.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY,
    created DATE,
    event_type TEXT,
    source TEXT,
    target TEXT,
    argument TEXT
)
            """)

    def connection_new(self):
        if self.connection:
            raise Exception("Connection already created")
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def connection_free(self, commit=True):
        if not self.connection:
            raise Exception("Connection does not exist")
        if commit:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
        self.connection = None

    def __enter__(self):
        return self.connection_new().cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection_free(exc_type is None)


class Message:
    def __init__(self, event):
        self.now = datetime.datetime.now()
        self.event = event

    def as_insert_sql(self):
        e = self.event
        if e.arguments():
            argument = e.arguments()[0]
        else:
            argument = ''
        return '''
INSERT INTO messages (created, event_type, source, target, argument)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.now, e.eventtype(), e.source(), e.target(), argument)


storage = Storage('/tmp/irclogs.sqlite3.db')

@helpers.events('pubmsg', 'privmsg')
def log(bot, conn, event):
    msg = Message(event)
    with storage as c:
        c.execute(*msg.as_insert_sql())
