#!/usr/bin/env python3

# needed because suspending (what could fail) during
# synchronization or upgrade processes could lead to data loss or
# a corrupted system

from subprocess import check_output
from sys import exit

DO_NOT_DISTURB = (
	"apt-get",
	"aptitude",
	"aria2c",
	"btrfs",
	"btrfsck",
	"clamscan",
	"cp",
	"curl",
	"duperemove",
	"mv",
	"pacman",
	"rsync",
	"tmux",
	"wget",
)

ps_output = check_output(["ps", "-e" ,"-c"])
processes = set(line.split()[5] for line in ps_output.splitlines())
for command in DO_NOT_DISTURB:
	if command.encode("utf-8") in processes:
		print("	Won't sleep because %s is running." % command)
		exit(1)
exit(0)
