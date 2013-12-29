#!/usr/bin/env python3

##### CONFIGURATION #####
# what interface to monitor?
INTERFACE="eth0"
# wait how many seconds before suspending since last network activity?
ACTIVITY_TIMEOUT=1800
# how long to sleep between measurements?
SLEEP_TIME=60
# how many packets must be transferred to consider the interface as active?
ACTIVITY_THRESHOLD=2500
# directory with dispatcher scripts
DISPATCHERS_DIR_PRE="./autosuspend.pre/"
DISPATCHERS_DIR_POST="./autosuspend.post/"
# command to perform suspend
SLEEP_CMD="s2ram"
#########################

from subprocess import call, check_output
from time import time, sleep, ctime
from string import whitespace
from os import walk, access, X_OK, chdir
from os.path import join, dirname
import sys

chdir(dirname(sys.argv[0]) or '.')

def debug(msg):
	if __debug__:
		print(msg)

def get_executables(directory):
	executables = []
	for root, dirs, files in walk(directory):
		for filename in files:
			script = join(root, filename)
			if access(script, X_OK):
				executables.append(script)
	executables.sort(reverse=True)
	return executables

def dispatch_pre():
	for executable in get_executables(DISPATCHERS_DIR_PRE):
		debug("		will run '%s' as a pre dispatcher" % executable)
		if call(executable, shell=True):
			debug("			returned not zero!")
			return False
	return True

def dispatch_post():
	for executable in get_executables(DISPATCHERS_DIR_POST):
		debug("		will run '%s' as a post dispatcher" % executable)
		call(executable, shell=True)

def try_to_sleep():
	if dispatch_pre():
		call([SLEEP_CMD])
		dispatch_post()
		return True
	return False

def get_packets():
	packet_fields=[2,10]
	file = open("/proc/net/dev", 'r')
	lines = file.readlines()
	file.close()
	lines.reverse()
	for line in lines:
		if INTERFACE in line:
			line = line.replace(":", " ")
			line = line.split()
			packet_counts = [ int(line[i]) for i in packet_fields ]
			return sum( packet_counts )

debug("Computer will sleep after a network activity less than %i packets in %i seconds on %s"
	% (ACTIVITY_THRESHOLD, ACTIVITY_TIMEOUT, INTERFACE) )

measurements = []
while True:
	time_now = time()
	packets_now = get_packets()
	measurements.append((time_now, packets_now))
	debug("%i packets at %s" % (packets_now, ctime(time_now)))

	for measurement in measurements[:]:
		measurement_time = measurement[0]
		measurement_packets = measurement[1]

		active = (packets_now - measurement_packets) > ACTIVITY_THRESHOLD
		expired = (time_now - measurement_time) > ACTIVITY_TIMEOUT

		if active:
			debug("	Activity - deleting record (%s => %i)"
					% (ctime(measurement_time), measurement_packets))
			measurements.remove(measurement)
			continue

		if not expired:
			break
		else:
			debug("	Not enough activity since %s! Try to sleep..."
					% ctime(measurement_time))
			measurements.remove(measurement)
			if try_to_sleep():
				debug("	Sleep was successfull! Resetting...")
				measurements = []
				break
	sleep(SLEEP_TIME)

