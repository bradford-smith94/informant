# informant

An Arch Linux News reader designed to also be used as a pacman hook.

Originally I had wanted to make an interactive pacman hook, but pacman is not
designed to work that way. So informant will instead interrupt pacman
transactions to make sure you have read the news first.

## Installation

You can install from my [AUR package](https://aur.archlinux.org/packages/informant/).
In case anyone wants to use Github to create issues or contribute to the AUR
package I have also [mirrored the PKGBUILD](https://github.com/bradford-smith94/informant-PKGBUILD).

Requirements are in `requirements.txt`. If you want to install it manually.
**NOTE:** The provided pip requirements likely won't be as up to date as the Arch
packages that AUR-installed informant will depend on, so your mileage may vary
if you take this approach.

On the first run informant assumes that you have not read any of the most recent news items.
Use the `informant read` command specified below to mark items as read.

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

`informant read` - if given a news item, will print that item and mark it as read.
You can specify a news item as either an index or a string matching the title.
If you want to use an index it must only be that shown when running `informant list`
(without '--unread' or '--reverse'). If no item is given, will begin looping through
all unread items, printing each one and marking them as read with a prompt to continue.
Passing the '--all' flag will mark all items as read without printing them.

More options can be found by reading `informant --help` or `man informant`.

### About the pacman hook

informant provides a PreTransaction pacman hook, so that it can interrupt a
pacman transaction if there are unread Arch Linux News items. This hook runs on
Upgrades and Installs, but not Removes. If for some reason the hook (or
informant) breaks in such a way that you cannot run a successful pacman
transaction (even after trying to read the news) you should be able to `pacman
-Rsn informant`.

informant installs its hook to `/usr/share/libalpm/hooks/` so you should also be
able to override the pacman hook by placing a new hook in
`/etc/pacman.d/hooks/00-informant.hook` or disable it by placing a symlink to
`/dev/null` in that location (e.g. `ln -s /dev/null
/etc/pacman.d/hooks/00-informant.hook`).

More information on pacman hooks can be found in `man alpm-hooks`.

## Configuration

Informant can be configured to check multiple feeds instead of just the Arch
Linux News feed (whether having it do so is actually useful or not is left up to
the user). Informant will check for an [informantrc.json](informantrc.json.example)
file in a few places. It will check in this order:

- CLI provided option
- `$HOME/.informantrc.json`
- `$XDG_CONFIG_HOME/informantrc.json`
- `/etc/informantrc.json`
- for each directory (`$d`) in `$XDG_CONFIG_DIRS` it will look for `$d/informantrc.json`

**NOTE:** If you want the configuration file to be used in the pacman hook make
sure to use a save location that will be accessible to informant when running as
root/sudo.

### Configuration Syntax

The syntax of informantrc.json is a JSON object containing one key (feeds) that
is a list describing the feeds you want informant to check. Each feed is
represented as a JSON object with the following keys:

- `name` (optional) - used to show which feed each news item is from
- `url` (required) - the feed URL
- `title-key` (optional) - defaults to `title`, the key used to reference the news item title in the feed
- `body-key` (optional) - defaults to `summary`, the key used to reference the news item body in the feed
- `timestamp-key` (optional) - defaults to `published`, the key used to reference the news item date in the feed

An example is provided here as [informanrc.json.example](informantrc.json.example) which configures informant to check the Arch Linux News feed as well as the [Arch Linux 32](https://archlinux32.org/) News feed.
