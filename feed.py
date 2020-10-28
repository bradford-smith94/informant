import requests
import feedparser
from dateutil import parser as date_parser
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


class Feed:
    def __init__(self, config):
        if 'url' in config:
            self.url = config['url']
        else:
            self.url = 'https://archlinux.org/feeds/news'

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
        for entry in self.feed.entries:
            timestamp = date_parser.parse(entry[self.timestamp_key])
            entries.append({
                'title': entry[self.title_key],
                'body': entry[self.body_key],
                'timestamp': timestamp
            })
        return entries

    def fetch(self):
        # Here you would check if user has passed --no-cache or not
        # Lots of ways we could do this from inside the Feed class
        # For now we'll pretend cache is enabled
        #
        # if nocache:
        #   return feedparser.parse(self.url)
        # else:
        session = CacheControl(requests.Session(), cache=FileCache('.cache'))

        return feedparser.parse(session.get(self.url).content)
