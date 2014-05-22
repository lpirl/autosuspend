#!/bin/bash

# WOL should be generally disabled so that the machine can be shut down
# normally w/o the need to disable WOL manually.
# Otherwise, you may wonder why the box is powering on again after
# power off.

# We do not disable this for e1000* cards since they apply their
# WOL options only upon shutdown and reboot:
#
# > WoL will be enabled on the system during the next shut down or reboot.
# > For this driver version, in order to enable WoL, the e1000e driver
# > must be loaded when shutting down or rebooting the system.
#
[ $(lsmod|grep -c "^e1000") -gt 0 ] && exit

/sbin/ethtool -s eth0 wol g
