#!/bin/bash

# Since we do (radical) power management by suspending the machine,
# we do not want the HDD's to spin down by itselfs.
# If they would spin down, they had to spin-up prior suspending
# (because 'sync' is invoked to clear caches) and thus cause more
# spin-up/-downs. HDD's don't like that.

lsblk -nrdo rota,path \
| grep '^1' \
| awk '{print $2}' \
| xargs -rP0 hdparm -S0

exit 0
