#!/bin/bash

# supported wakes:
#              p  Wake on phy activity
#              u  Wake on unicast messages
#              m  Wake on multicast messages
#              b  Wake on broadcast messages
#              g  Wake on MagicPacket(tm)

/sbin/ethtool -s eth0 wol ug
