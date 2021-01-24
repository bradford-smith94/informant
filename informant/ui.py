"""
informant/ui.py

This module contains User Interface related functions.
"""

import os
import shutil
import subprocess
import sys
import textwrap

import html2text

from informant.config import InformantConfig

RAW_OPT = '--raw'

def err_print(*args, **kwargs):
    """ Same as builtin print but output to stderr with red color and "ERROR"
    preamble.
    """
    red = InformantConfig().colors['RED']
    clear = InformantConfig().colors['CLEAR']
    msg = red + 'ERROR: ' + clear
    for arg in args:
        msg += arg
    print(*args, file=sys.stderr, **kwargs)

def debug_print(*args, **kwargs):
    """ Same as builtin print but output to stderr. """
    print(*args, file=sys.stderr, **kwargs)

def pacman_msg(*args, **kwargs):
    """ Same as print but include yellow color and "informant" preamble so the
    message is clear in pacman.
    """
    yellow = InformantConfig().colors['YELLOW']
    clear = InformantConfig().colors['CLEAR']
    msg = yellow + ':: informant: ' + clear
    for arg in args:
        msg += arg
    print(msg, **kwargs)

def prompt_yes_no(question, default):
    """ Print 'question' to user with (y/n) and 'default' being the
    response for blank input.
    """
    again = 'Unknown response.'
    if default.lower() in ('y', 'yes'):
        options = '(Y/n): '
    elif default.lower() in ('n', 'no'):
        options = '(y/N): '

    response = input(' '.join((question, options))).lower()
    while response not in ('y', 'yes', 'n', 'no', ''):
        response = input(' '.join((again, question, options))).lower()
    if response == '':
        return default
    return response

def running_from_pacman():
    """ Return True if the parent process is pacman """
    debug = InformantConfig().get_argv_debug()
    ppid = os.getppid()
    p_name = subprocess.check_output(['ps', '-p', str(ppid), '-o', 'comm='])
    p_name = p_name.decode().rstrip()
    if debug:
        ui.debug_print('informant: running from: {}'.format(p_name))
    return p_name == 'pacman'

def pretty_print_item(entry):
    """ Print out the given entry, replacing some markup to make it look nicer.
    If the '--raw' option has been provided then the markup will not be
    replaced. """
    argv = InformantConfig().get_argv()
    title = entry.title
    body = entry.body
    bold = InformantConfig().colors['BOLD']
    clear = InformantConfig().colors['CLEAR']
    timestamp = str(entry.timestamp)
    if not argv.get(RAW_OPT):
        #if not using raw also bold title
        title = bold + title + clear
        h2t = html2text.HTML2Text()
        h2t.inline_links = False
        h2t.body_width = 85
        body = h2t.handle(body)
    if entry.feed_name is not None:
        feed_name = '({})'.format(entry.feed_name)
        print('{}\n{}\n{}\n\n{}'.format(title, feed_name, timestamp, body))
    else:
        print('{}\n{}\n\n{}'.format(title, timestamp, body))

def format_list_item(entry, index):
    """ Returns a formatted string with the entry's index number, title, and
    right-aligned timestamp. Unread items are bolded"""
    bold = InformantConfig().colors['BOLD']
    clear = InformantConfig().colors['CLEAR']
    terminal_width = shutil.get_terminal_size().columns
    wrap_width = terminal_width - len(str(entry.timestamp)) - 1
    heading = str(index) + ': ' + entry.title
    wrapped_heading = textwrap.wrap(heading, wrap_width)
    padding = terminal_width - len(wrapped_heading[0] + str(entry.timestamp))
    if entry.has_been_read():
        return (
            wrapped_heading[0] +
            ' ' * (padding) +
            str(entry.timestamp) +
            '\n'.join(wrapped_heading[1:])
                )
    else:
        return (
            bold +
            wrapped_heading[0] +
            clear +
            ' ' * (padding) +
            str(entry.timestamp) +
            bold +
            '\n'.join(wrapped_heading[1:]) +
            clear
        )

