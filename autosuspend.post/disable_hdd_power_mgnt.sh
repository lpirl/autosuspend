#!/bin/bash -x

# Since we do (radical) power management by suspending the machine,
# we do not want the HDD's to spin down by itselfs.
# If they would spin down, they had to spin-up prior suspending
# (because 'sync' is invoked to clear caches) and thus cause more
# spin-up/-downs. HDD's don't like that.

FIND_DEVS='sd[a-z]'

for f in $(find /dev -name $FIND_DEVS)
do
	hdparm -S0 $f &
done
exit 0
