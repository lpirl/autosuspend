#!/usr/bin/env python3

if __name__ != '__main__':
	raise NotImplementedError(
		"This is module should only be called directly from command line."
	)

import argparse
from subprocess import call, check_output
from time import time, sleep, ctime
from string import whitespace
from os import walk, access, X_OK, chdir
from os.path import join, dirname
import sys


####################
# functions
#

def debug(msg):
	if __debug__:
		print(msg)

def call_dispatcher(executable):
	return call((executable, args.interface,))

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
		if call_dispatcher(executable):
			debug("			returned not zero!")
			return False
	return True

def dispatch_post():
	for executable in get_executables(DISPATCHERS_DIR_POST):
		debug("		will run '%s' as a post dispatcher" % executable)
		call_dispatcher(executable)

def try_to_sleep():
	if dispatch_pre():
		call([args.sleep_cmd], shell=True)
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
		if args.interface in line:
			line = line.replace(":", " ")
			line = line.split()
			packet_counts = [ int(line[i]) for i in packet_fields ]
			return sum( packet_counts )


####################
# CLI args.interface
#
parser = argparse.ArgumentParser(
	description="This script suspends your computer on few network activity.",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-t', '--timeout', type=int, default=1800,
                    help='How many seconds must the network be idle?')
parser.add_argument('-i', '--interval', type=int, default=60,
                    help='How many seconds to sleep between measurements?')
parser.add_argument('-s', '--threshold', type=int, default=2500,
                    help='Amount of packages to consider the interface as active.')
parser.add_argument('-c', '--sleep_cmd', type=str, default="s2ram",
                    help='The executable to call to suspend the machine.')
parser.add_argument('interface', type=str,
                    help='Use which interface to determine network activity?')
args = parser.parse_args()


####################
# main program
#
DISPATCHERS_DIR_PRE = "./autosuspend.pre/"
DISPATCHERS_DIR_POST = "./autosuspend.post/"

debug("Computer will sleep after a network activity less than %i packets in %i seconds on %s"
	% (args.threshold, args.timeout, args.interface) )

chdir(dirname(sys.argv[0]) or '.')

measurements = []
while True:
	time_now = time()
	packets_now = get_packets()

	if packets_now is None:
		print("Could not determine packet count for '%s'" % args.interface)
		print("Is this properlys configured?")
		exit(1)

	measurements.append((time_now, packets_now))
	debug("%i packets at %s" % (packets_now, ctime(time_now)))

	for measurement in measurements[:]:
		measurement_time = measurement[0]
		measurement_packets = measurement[1]

		active = (packets_now - measurement_packets) > args.threshold
		expired = (time_now - measurement_time) > args.timeout

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
	sleep(args.interval)
