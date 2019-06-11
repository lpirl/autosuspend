#!/usr/bin/env python3

# Exits with exit code 0 (i.e., allows sleep) if all load averages
# (1, 5, 15 minutes) are below ``MAX_IDLE_LOAD``.

from os import getloadavg

MAX_IDLE_LOAD = .09

def check_load(time_span, load):
  if load > MAX_IDLE_LOAD:
    print(
      "	Won't sleep because %i minute load average" % time_span,
      "of %.2f is above threshold of %.2f." % (load, MAX_IDLE_LOAD)
    )
    exit(1)

loads = getloadavg()
check_load(1, loads[0])
check_load(5, loads[1])
check_load(15, loads[2])
