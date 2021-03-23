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

from informant.config import InformantConfig
from informant.entry import Entry
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
        if InformantConfig().get_argv_use_cache():
            cachefile = InformantConfig().get_cachefile()
            os.umask(0o0002) # unrestrict umask so we can cache with proper permissions
            try:
                session = CacheControl(requests.Session(), cache=FileCache(cachefile, filemode=0o0664, dirmode=0o0775))
                feed = feedparser.parse(session.get(self.url).content)
            except Exception as e:
                ui.err_print('Unable to read cache information: {}'.format(e))
                feed = feedparser.parse(self.url)
        else:
            feed = feedparser.parse(self.url)

        if feed.bozo:
            ui.err_print('Encountered feed error: {}'.format(feed.bozo_exception))
            sys.exit(255)
        else:
            return feed
