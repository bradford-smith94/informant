"""
informant/entry.py

This module contains entry (feed item) related functions.
"""

from informant.config import InformantConfig
import informant.ui as ui

class Entry:
    def __init__(self, title, timestamp, body, feed_name):
        self.title = title
        self.timestamp = timestamp
        self.pretty_date = timestamp.strftime('%a, %d %b %Y %H:%M:%S %z')
        self.body = body
        self.feed_name = feed_name

    def has_been_read(self):
        """ Check if this entry has been read and return True or False. """
        readlist = InformantConfig().readlist
        #ui.debug_print('readlist: {}'.format(readlist))
        title = self.title
        date = self.timestamp
        if str(date.timestamp()) + '|' + title in readlist:
            return True
        return False

    def mark_as_read(self):
        """ Save this entry to mark it as read. """
        readlist = InformantConfig().readlist
        if self.has_been_read():
            return
        title = self.title
        date = self.timestamp
        readlist.append(str(date.timestamp()) + '|' + title)

