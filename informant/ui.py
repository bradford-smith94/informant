import os
import sys

from informant.config import InformantConfig

# colors
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
CLEAR = '\033[0m'
BOLD = '\033[1m'

def err_print(*args, **kwargs):
    """ Same as builtin print but output to stderr with red color and "ERROR"
    preamble.
    """
    msg = RED + 'ERROR: ' + CLEAR
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
    msg = YELLOW + ':: informant: ' + CLEAR
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
    argv = InformantConfig.get_argv()
    ppid = os.getppid()
    p_name = subprocess.check_output(['ps', '-p', str(ppid), '-o', 'comm='])
    p_name = p_name.decode().rstrip()
    if argv.get(DEBUG_OPT):
        ui.debug_print('informant: running from: {}'.format(p_name))
    return p_name == 'pacman'

