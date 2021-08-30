"""
informant/feed.py

This module defines the structure of a newsfeed for Informant.
"""

import os
import sys

import requests
import feedparser
from dateutil import parser as date_parser
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from urllib.error import URLError

from informant.config import InformantConfig
from informant.entry import Entry
import informant.file as fs
import informant.ui as ui

ARCH_NEWS = 'https://archlinux.org/feeds/news'

class Feed:
    def __init__(self, config={}):
        if 'name' in config:
            self.name = config['name']
        else:
            self.name = None

        if 'url' in config:
            self.url = config['url']
        else:
            self.url = ARCH_NEWS

        if 'title-key' in config:
            self.title_key = config['title-key']
        else:
            self.title_key = 'title'

        if 'body-key' in config:
            self.body_key = config['body-key']
        else:
            self.body_key = 'summary'

        if 'timestamp-key' in config:
            self.timestamp_key = config['timestamp-key']
        else:
            self.timestamp_key = 'published'

        ui.debug_print('building feed for: {}'.format(self.name if self.name is not None else self.url))

        self.feed = self.fetch()  # the complete feed as returned by feedparser
        self.entries = self.build_feed()  # the list of entries informant will use

    def build_feed(self):
        """
        Abstract away any differences in feeds by using the parsed keys and
        return an informant-friendly list of entries
        """
        entries = []
        for item in self.feed.entries:
            timestamp = date_parser.parse(item[self.timestamp_key])
            entries.append(Entry(item[self.title_key],
                                 timestamp,
                                 item[self.body_key],
                                 self.name))
        return entries

    def fetch(self):
        feed = None
        if InformantConfig().get_argv_clear_cache():
            ui.debug_print('Clearing cache')
            fs.clear_cachefile()
        if InformantConfig().get_argv_use_cache():
            ui.debug_print('Checking cache in {}'.format(InformantConfig().get_cachefile()))
            cachefile = InformantConfig().get_cachefile()
            os.umask(0o0002) # unrestrict umask so we can cache with proper permissions
            try:
                session = CacheControl(requests.Session(), cache=FileCache(cachefile, filemode=0o0664, dirmode=0o0775))
                feed = feedparser.parse(session.get(self.url).content)
            except Exception as e:
                ui.err_print('Unable to read cache information: {}'.format(e))
                ui.debug_print('Falling back to fetching feed')
                feed = feedparser.parse(self.url)
        else:
            feed = feedparser.parse(self.url)

        if feed.bozo:
            e = feed.bozo_exception
            if isinstance(e, URLError):
                # most likely this is an internet issue (no connection)
                ui.warn_print('News could not be fetched for {}'.format(self.name if self.name is not None else self.url))
                ui.debug_print('URLError: {}'.format(e.reason))
            else:
                # I think this is most likely to be a malformed feed
                ui.err_print('Encountered feed error: {}'.format(feed.bozo_exception))
                ui.debug_print('bozo message: {}'.format(feed.bozo_exception.getMessage()))
            # In either of these error cases we probably shouldn't return error
            # so the pacman hook won't hold up an operation.
            # Here return an empty set of entries in case only one of multiple
            # feeds failed to fetch
            try:
                feed = feedparser.util.FeedParserDict()
                feed.update({'entries': []})
            except Exception as e:
                ui.err_print('Unexpected error: {}'.format(e))
                sys.exit()

        return feed
