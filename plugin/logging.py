import sqlite3

from . import helpers


class Storage:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

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
            self._connection.rollback()
        self.connection.close()
        self.connection = None

    def __enter__(self):
        return self.connection_new().cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection_free(exc_type is None)


class Message:
    def __init__(self, event):
        self.event = event



@helpers.events('pubmsg')
def log(bot, conn, event):
    pass
