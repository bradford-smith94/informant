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
    -c <cfile>, --config=<cfile>    Use <cfile> as the config file
    -d, --debug                     Print the command line arguments and don't
                                    make changes to the save file
    -r, --raw                       When printing items do not replace any
                                    markup
    -f <file>, --file=<file>        Use <file> as the save location for read
                                    items
    -h, --help                      Show this help and exit
    -V,--version                    Show version and exit
    --no-cache                      Do not use cache

"""

# builtins
import sys

# external
import docopt

# local
from informant.config import InformantConfig
from informant.feed import Feed
import informant.file as fs
import informant.ui as ui

__version__ = '0.4.2'

# commands
CHECK_CMD = 'check'
LIST_CMD = 'list'
READ_CMD = 'read'

# global options
DEBUG_OPT = '--debug'
FILE_OPT = '--file'
RAW_OPT = '--raw'

# 'list' options
REV_OPT = '--reverse'
UNREAD_OPT = '--unread'

# 'read' options and args
ITEM_ARG = '<item>'
READALL_OPT = '--all'

def check_cmd(feed):
    """ Run the check command. Check if there are any news items that are
    unread. If there is only one unread item, print it out and mark it as read.
    Also, exit the program with return code matching the unread count. """
    running_from_pacman = ui.running_from_pacman()
    unread = 0
    unread_items = []
    for entry in feed:
        if not entry.has_been_read():
            unread += 1
            unread_items.append(entry)
    if unread == 1:
        if running_from_pacman:
            ui.pacman_msg('Stopping upgrade to print news')
        ui.pretty_print_item(unread_items[0])
        unread_items[0].mark_as_read()
        fs.save_datfile()
        if running_from_pacman:
            ui.pacman_msg('You can re-run your pacman command to complete the upgrade')
    elif unread > 1:
        print('There are {:d} unread news items! Use informant to read \
them.'.format(unread))
        if running_from_pacman:
            ui.pacman_msg('Run `informant read` before re-running your pacman command')
    else:
        print('There are no unread news items')
    sys.exit(unread)

def list_cmd(feed):
    """ Run the list command. Print out a list of recent news item titles. """
    argv = InformantConfig().get_argv()
    if argv.get(REV_OPT):
        feed_list = reversed(feed)
    else:
        feed_list = feed
    index = 0
    for entry in feed_list:
        if not argv.get(UNREAD_OPT) \
        or (argv.get(UNREAD_OPT) and not entry.has_been_read()):
            print(ui.format_list_item(entry, index))
            index += 1

def read_cmd(feed):
    """ Run the read command. Print news items and mark them as read. """
    argv = InformantConfig().get_argv()
    if argv.get(READALL_OPT):
        for entry in feed:
            entry.mark_as_read()
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
            entry.mark_as_read()
        else:
            unread_entries = list()
            for entry in feed:
                if not entry.has_been_read():
                    unread_entries.insert(0, entry)
            for entry in unread_entries:
                ui.pretty_print_item(entry)
                entry.mark_as_read()
                if entry is not unread_entries[-1]:
                    read_next = ui.prompt_yes_no('Read next item?', 'yes')
                    if read_next in ('n', 'no'):
                        break
                else:
                    print('No more unread items')
    fs.save_datfile()

def run():
    """ The main function.
    Check given arguments get feed and run given command. """
    argv = InformantConfig().get_argv()
    config = InformantConfig().get_config()
    if argv.get(DEBUG_OPT):
        ui.debug_print('cli args: {}'.format(argv))

    if 'feeds' in config:
        feed = []
        for config_feed in config['feeds']:
            feed += Feed(config_feed).entries
    else:
        feed = Feed().entries

    feed = sorted(feed, key=lambda k: k.timestamp, reverse=True)

    if argv.get(CHECK_CMD):
        check_cmd(feed)
    elif argv.get(LIST_CMD):
        list_cmd(feed)
    elif argv.get(READ_CMD):
        read_cmd(feed)

def main():
    argv = docopt.docopt(__doc__, version='informant v{}'.format(__version__))
    InformantConfig().set_argv(argv)
    InformantConfig().debug_print = ui.debug_print
    InformantConfig().readlist = fs.read_datfile()
    run()
    sys.exit()

if __name__ == '__main__':
    main()
