#!/usr/bin/env python3

from subprocess import call, check_output
from sys import exit

DO_NOT_DISTURB=["aptitude", "apt-get", "rsync"]

processes = check_output(["ps", "-e" ,"-c"])
processes = processes.splitlines()
processes = [l.split()[5] for l in processes]
for command in DO_NOT_DISTURB:
	if command.encode("utf-8") in processes:
		print("	Won't sleep because %s is running." % command)
		exit(1)
exit(0)
