#!/bin/bash

# this will be (only?) required to spin down external drives

FIND_DEVS='sd[c-z]'

sync

find /dev -name $FIND_DEVS -print0 | xargs -0P0 hdparm -y

exit 0
