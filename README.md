# informant

An Arch Linux News reader designed to also be used as a pacman hook.

Originally I had wanted to make an interactive pacman hook, but pacman is not
designed to work that way.

## Installation

You can install from my [AUR package](https://aur.archlinux.org/packages/informant/).

Requirements are in `requirements.txt`. If you want to install it manually.

## How does it work?

informant provides 3 subcommands, 'check', 'list' and 'read'.

`informant check` - will check for any unread news items, if there is only one
unread item it will print it and mark it as read. Informant check will exit with
return code equal to the number of unread news items (even if there is only
one). This is the command used by the pacman hook, so that if there are unread
news items it will interrupt your pacman transaction.

`informant list` - will list the titles of the most recent news items
(regardless of whether or not they have been read, unless the '--unread' option
is given). There is also a '--reverse' option if you prefer to see them newest
to oldest.

`informant read` - will print a given news item and mark it as read. You must
either specify a news item as either an index or a string matching the title, or
include the '--all' option. If you want to use an index it must only be that
shown when running `informant list` (without '--unread' or '--reverse').

More options can be found by reading `informant --help`.

### About the pacman hook

informant provides a PreTransaction pacman hook, so that it can interrupt a
pacman transaction if there are unread Arch Linux News items. This hook runs on
Upgrades and Installs, but not Removes. If for some reason the hook (or
informant) breaks in such a way that you cannot run a successful pacman
transaction (even after trying to read the news) you should be able to `pacman
-Rsn informant`.

informant installs its hook to `/usr/share/libalpm/hooks/` so you should also be
able to override the pacman hook by placing a new hook in
`/etc/pacman.d/hooks/informant.hook` or disable it by placing a symlink to
`/dev/null` in that location (e.g. `ln -s /dev/null
/etc/pacman.d/hooks/informant.hook`).

More information on pacman hooks can be found in `man alpm-hooks`.

### First time use

**Note**: On the first run informant assumes that you have not read any of the
most recent news items. The RSS feed provides the most recent 10 items, so after
first install you must use `informant read` to mark all the most recent news
items as read. You can use `informant read --all` to mark all 10 items at once,
but this assumes you have actually read the most recent 10 items.

