#!/bin/bash

# required to tell the kernel, that the interface is allowed to wake the
# machine

echo enabled > /sys/class/net/$1/device/power/wakeup
