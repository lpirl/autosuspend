#!/bin/bash

# required because we do not want network interfaces to be powered off
# (would disable wake on lan)

file=/etc/default/halt

# if configuration unset, set it:
grep -q "NETDOWN" $file || (echo "NETDOWN=no" >> $file)

# check that expected configuration exists
grep -q 'NETDOWN=*no*' $file || exit 1
