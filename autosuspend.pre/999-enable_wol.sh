#!/bin/bash

# obviously needed to enable wake on lan

# wake types
#	p	Wake on PHY activity
#	u	Wake on unicast messages
#	m	Wake on multicast messages
#	b	Wake on broadcast messages
#	a	Wake on ARP
#	g	Wake on MagicPacket™
#	s	Enable SecureOn™ password for MagicPacket™
#	d	Disable (wake on  nothing).   This  option
#		clears all previous options.
#
# check supported modes with `ethtool eth0|grep "Supports Wake"`

IF=eth0
WAKE_ON=ug

# fix for Intel e1000* cards:
for (( i=0; i<${#WAKE_ON}; i++ )); do
  TYPE=${WAKE_ON:$i:1}
  [ $(ethtool $IF | grep -P "\tWake-on" | grep -c "$TYPE") -eq 0 ] && continue
  MSG="You need to reboot your machine in order to make wake on LAN work.\n"
  MSG+="Please refer to section 'Enabling Wake on LAN' at \n"
  MSG+="http://www.cyberciti.biz/files/linux-kernel/Documentation/networking/e1000e.txt \n"
  MSG+="for further details."
  echo -e $MSG
  (echo -e $MSG | sendmail s "autosyspendat $(hostname): reboot required" $(whoami)) \
    > /dev/null 2>&1
  break
done

/sbin/ethtool -s $IF wol $WAKE_ON
