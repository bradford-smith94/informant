"""
informant/file.py

This module contains filesystem related functions.
"""

import pickle
import sys

from informant.config import InformantConfig
import informant.ui as ui

FILE_DEFAULT = '/var/cache/informant.dat'

def get_save_name():
    """ Return the name of the file to save read information to. """
    argv = InformantConfig().get_argv()
    if argv.get(FILE_OPT):
        return argv.get(FILE_OPT)
    return FILE_DEFAULT

def get_datfile(filename):
    """ Return a datfile, which should be a tuple with the first element
    containing the cache, and the second element the list of read items. """
    argv = InformantConfig().get_argv()
    if argv.get(DEBUG_OPT):
        ui.debug_print('Getting datfile from "{}"'.format(filename))

    try:
        with open(filename, 'rb') as pickle_file:
            try:
                (cache, readlist) = pickle.load(pickle_file)
                pickle_file.close()
            except (EOFError, ValueError):
                (cache, readlist) = ({"feed": None, "max-age": None, "last-request": None}, [])
    except (FileNotFoundError, PermissionError):
        (cache, readlist) = ({"feed": None, "components": {}}, [])
    return (cache, readlist)

def save_datfile():
    """ Save the datfile with cache and readlist """
    argv = InformantConfig().get_argv()
    if argv.get(DEBUG_OPT):
        return
    filename = get_save_name()
    datfile_obj = (CACHE, READLIST)
    try:
        # then open as write to save updated list
        with open(filename, 'wb') as pickle_file:
            pickle.dump(datfile_obj, pickle_file)
            pickle_file.close()
    except PermissionError:
        ui.err_print('Unable to save read information, please re-run with \
correct permissions to access "{}".'.format(filename))
        sys.exit(255)

