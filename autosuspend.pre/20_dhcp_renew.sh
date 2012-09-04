#!/bin/bash

# We just grab a new DHCP lease here. Mainly to refresh the routers
# ARP cache and to reset the DHCP lease life time.

dhclient -r eth0
dhclient eth0
