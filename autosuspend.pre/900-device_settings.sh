#!/bin/bash

# required to tell the kernel, that eth0 is allowed to wake the machine

echo enabled > /sys/class/net/eth0/device/power/wakeup
