"""
informant/file.py

This module contains filesystem related functions.
"""

import pickle
import sys

from informant.config import InformantConfig
import informant.ui as ui

def read_datfile():
    """ Return the saved readlist from the datfile """
    debug = InformantConfig().get_argv_debug()
    filename = InformantConfig().get_savefile()
    if debug:
        ui.debug_print('Getting datfile from "{}"'.format(filename))

    try:
        with open(filename, 'rb') as pickle_file:
            try:
                readlist = pickle.load(pickle_file)
                pickle_file.close()
                if isinstance(readlist, tuple):
                    # backwards compatibility with informant < 0.4.0 save data
                    readlist = readlist[1]
            except (EOFError, ValueError):
                readlist = []
    except (FileNotFoundError, PermissionError):
        readlist = []
    return readlist

def save_datfile():
    """ Save the readlist to the datfile """
    debug = InformantConfig().get_argv_debug()
    readlist = InformantConfig().readlist
    if debug:
        return
    filename = InformantConfig().get_savefile()
    try:
        # then open as write to save updated list
        with open(filename, 'wb') as pickle_file:
            pickle.dump(readlist, pickle_file)
            pickle_file.close()
    except PermissionError:
        ui.err_print('Unable to save read information, please re-run with \
correct permissions to access "{}".'.format(filename))
        sys.exit(255)

