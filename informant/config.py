"""
informant/config.py

This module contains helpers to manage arguments, options and configuration
settings provided to Informant.
"""

import json
import os

from xdg import xdg_config_dirs, xdg_config_home

DEBUG_OPT = '--debug'
FILE_OPT = '--file'
CFILE_OPT = '--config'
NOCACHE_OPT = '--no-cache'

FILE_DEFAULT = '/var/lib/informant.dat' # readlist save file
CACHE_DEFAULT = '/var/cache/informant' # http caching
CONFIG_BASE = 'informantrc.json' # user config

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
        self.config = None
        self.colors = {
                'RED': '\033[0;31m',
                'YELLOW': '\033[1;33m',
                'CLEAR': '\033[0m',
                'BOLD': '\033[1m'
        }
        self.readlist = None
        self.debug_print = None

    def set_argv(self, args):
        self.argv = args

    def get_argv(self):
        return self.argv

    def get_argv_debug(self):
        return self.argv.get(DEBUG_OPT)

    def get_argv_use_cache(self):
        """ Return True if we should use the cache, else False.
        Providing the NOCACHE_OPT means that we should not use the cache.
        """
        if self.argv.get(NOCACHE_OPT):
            return False
        return True

    def get_cachefile(self):
        return CACHE_DEFAULT

    def get_savefile(self):
        if self.argv.get(FILE_OPT):
            return self.argv.get(FILE_OPT)
        return FILE_DEFAULT

    def set_config(self, config):
        self.config = config

    def read_config(self):
        self.config = {}
        cfile_option = self.argv.get(CFILE_OPT)
        cfg_fname = None
        if cfile_option and os.path.exists(cfile_option):
            cfg_fname = cfile_option
        elif os.path.exists(os.path.expandvars('$HOME/.' + CONFIG_BASE)):
            cfg_fname = os.path.expandvars('$HOME/.' + CONFIG_BASE)
        elif os.path.exists(os.path.join(xdg_config_home(), CONFIG_BASE)):
            cfg_fname = os.path.join(xdg_config_home(), CONFIG_BASE)
        elif os.path.exists(os.path.join('/etc/', CONFIG_BASE)):
            cfg_fname = os.path.join('/etc/', CONFIG_BASE)
        else:
            for dirname in xdg_config_dirs():
                if os.path.exists(os.path.join(dirname, CONFIG_BASE)):
                    cfg_fname = os.path.join(dirname, CONFIG_BASE)
                    break
        if self.get_argv_debug():
            self.debug_print('cfg_fname: {}'.format(cfg_fname))
        if cfg_fname is not None:
            with open(cfg_fname, 'r') as cfg:
                self.config = json.loads(cfg.read())
        if self.get_argv_debug():
            self.debug_print('config: {}'.format(self.config))
        return self.config

    def get_config(self):
        if self.config is None:
            return self.read_config()
        return self.config
