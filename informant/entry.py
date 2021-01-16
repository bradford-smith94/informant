"""
informant/entry.py

This module contains entry (feed item) related functions.
"""

from informant.config import InformantConfig
import informant.ui as ui

def has_been_read(entry):
    """ Check if the given entry has been read and return True or False. """
    debug = InformantConfig().get_argv_debug()
    readlist = InformantConfig().readlist
    if debug:
        ui.debug_print(readlist)
    title = entry['title']
    date = entry['timestamp']
    if str(date.timestamp()) + '|' + title in readlist:
        return True
    return False

def mark_as_read(entry):
    """ Save the given entry to mark it as read. """
    readlist = InformantConfig().readlist
    if has_been_read(entry):
        return
    title = entry['title']
    date = entry['timestamp']
    readlist.append(str(date.timestamp()) + '|' + title)

