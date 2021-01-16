#!/usr/bin/python3
"""
informant - an Arch Linux News reader designed to also be used as a pacman hook

Usage:
    informant [options] check
    informant [options] list [--reverse --unread]
    informant [options] read [<item> | --all]

Commands:
    check - Check for unread news items, will exit with a positive return code
            with the number of unread items. If there is only one unread item it
            will also print in like 'read' would and mark it as read, else it
            will print the number of unread titles.

    list -  Print the most recent news items, regardless of read status. If
            '--reverse' is provided items are printed oldest to newest. If
            '--unread' is provided only the unread items are returned.

    read  - Read the specified news item, <item> can be either an index or a
            full title. This will also save the item as 'read' so that future
            calls to 'check' will no longer display it. If no <item> is given,
            will begin looping through all unread items, printing each one and
            marking them as read with a prompt to continue. Passing the --all
            flag will mark all items as read without printing.

Options:
    -d, --debug                 Print the command line arguments and don't make
                                changes to the save file
    -r, --raw                   When printing items do not replace any markup
    -f <file>, --file=<file>    Use <file> as the save location for read items
    -h, --help                  Show this help and exit
    -V,--version                Show version and exit
    --no-cache                  Do not use cache

"""

# builtins
import json
import os
import sys

# external
import docopt

# local
from informant.config import InformantConfig
from informant.feed import Feed
import informant.file as fs
import informant.ui as ui

__version__ = '0.3.0'

CONFIG_FILE = 'config.json' #TODO rename for release
ARCH_NEWS = 'https://archlinux.org/feeds/news'

# commands
CHECK_CMD = 'check'
LIST_CMD = 'list'
READ_CMD = 'read'

# global options
DEBUG_OPT = '--debug'
FILE_OPT = '--file'
RAW_OPT = '--raw'
NOCACHE_OPT = '--no-cache'

# 'list' options
REV_OPT = '--reverse'
UNREAD_OPT = '--unread'

# 'read' options and args
ITEM_ARG = '<item>'
READALL_OPT = '--all'

def has_been_read(entry):
    """ Check if the given entry has been read and return True or False. """
    argv = InformantConfig.get_argv()
    if argv.get(DEBUG_OPT):
        ui.debug_print(READLIST)
    title = entry['title']
    date = entry['timestamp']
    if str(date.timestamp()) + '|' + title in READLIST:
        return True
    return False

def mark_as_read(entry):
    """ Save the given entry to mark it as read. """
    if has_been_read(entry):
        return
    title = entry['title']
    date = entry['timestamp']
    READLIST.append(str(date.timestamp()) + '|' + title)
    fs.save_datfile()

def check_cmd(feed):
    """ Run the check command. Check if there are any news items that are
    unread. If there is only one unread item, print it out and mark it as read.
    Also, exit the program with return code matching the unread count. """
    running_from_pacman = ui.running_from_pacman()
    unread = 0
    unread_items = []
    for entry in feed:
        if not has_been_read(entry):
            unread += 1
            unread_items.append(entry)
    if unread == 1:
        if running_from_pacman:
            ui.pacman_msg('Stopping upgrade to print news')
        ui.pretty_print_item(unread_items[0])
        mark_as_read(unread_items[0])
        if running_from_pacman:
            ui.pacman_msg('You can re-run your pacman command to complete the upgrade')
    elif unread > 1:
        print('There are {:d} unread news items! Use informant to read \
them.'.format(unread))
        if running_from_pacman:
            ui.pacman_msg('Run `informant read` before re-running your pacman command')
    sys.exit(unread)

def list_cmd(feed):
    """ Run the list command. Print out a list of recent news item titles. """
    argv = InformantConfig.get_argv()
    if argv.get(REV_OPT):
        feed_list = reversed(feed)
    else:
        feed_list = feed
    index = 0
    for entry in feed_list:
        if not argv.get(UNREAD_OPT) \
        or (argv.get(UNREAD_OPT) and not has_been_read(entry)):
            print(ui.format_list_item(entry, index))
            index += 1

def read_cmd(feed):
    """ Run the read command. Print news items and mark them as read. """
    argv = InformantConfig.get_argv()
    if argv.get(READALL_OPT):
        for entry in feed:
            mark_as_read(entry)
    else:
        if argv[ITEM_ARG]:
            try:
                item = int(argv[ITEM_ARG])
                entry = feed[item]
            except ValueError:
                for entry in feed:
                    if entry.title == item:
                        break
                #NOTE: this will read the oldest unread item if no matches are found
            ui.pretty_print_item(entry)
            mark_as_read(entry)
        else:
            unread_entries = list()
            for entry in feed:
                if not has_been_read(entry):
                    unread_entries.insert(0, entry)
            for entry in unread_entries:
                ui.pretty_print_item(entry)
                mark_as_read(entry)
                if entry is not unread_entries[-1]:
                    read_next = ui.prompt_yes_no('Read next item?', 'yes')
                    if read_next in ('n', 'no'):
                        break
                else:
                    print('No more unread items')

def run():
    """ The main function.
    Check given arguments get feed and run given command. """
    argv = InformantConfig.get_argv()
    config = InformantConfig.get_config()
    if argv.get(DEBUG_OPT):
        ui.debug_print(argv)

    feed = []
    for config_feed in config['feeds']:
        feed = feed + Feed(config_feed).entries

    feed = sorted(feed, key=lambda k: k['timestamp'], reverse=True)

    if argv.get(CHECK_CMD):
        check_cmd(feed)
    elif argv.get(LIST_CMD):
        list_cmd(feed)
    elif argv.get(READ_CMD):
        read_cmd(feed)

def main():
    global CACHE, READLIST
    argv = docopt.docopt(__doc__, version='informant v{}'.format(__version__))
    InformantConfig().set_argv(argv)
    CACHE, READLIST = fs.get_datfile(fs.get_save_name())
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as cfg:
            config = json.loads(cfg.read())
            InformantConfig().set_config(config)
    run()
    sys.exit()

if __name__ == '__main__':
    main()
