#!/bin/bash

# required because we do not want network interfaces to be powered off
# (would disable wake on lan)

exit $(( $(grep "NETDOWN" /etc/default/halt|grep -c no) - 1 ))
