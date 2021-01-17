"""
informant/config.py

This module contains helpers to manage arguments, options and configuration
settings provided to Informant.
"""

DEBUG_OPT = '--debug'
FILE_OPT = '--file'

FILE_DEFAULT = '/var/cache/informant.dat'

class Singleton(type):
    """ A Singleton class to be used as a base """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class InformantConfig(metaclass=Singleton):
    """ Class to store global Informant arguments/options and configuration """

    def __init__(self):
        self.argv = {}
        self.config = {}
        self.colors = {
                'RED': '\033[0;31m',
                'YELLOW': '\033[1;33m',
                'CLEAR': '\033[0m',
                'BOLD': '\033[1m'
        }
        self.cache = None
        self.readlist = None

    def set_argv(self, args):
        self.argv = args

    def get_argv(self):
        return self.argv

    def get_argv_debug(self):
        return self.argv.get(DEBUG_OPT)

    def get_savefile(self):
        if self.argv.get(FILE_OPT):
            return self.argv.get(FILE_OPT)
        return FILE_DEFAULT

    def set_config(self, config):
        self.config = config

    def get_config(self):
        return self.config
