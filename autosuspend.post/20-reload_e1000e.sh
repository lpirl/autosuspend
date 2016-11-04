#!/bin/bash

lsmod | grep -q e1000e || exit 0
rmmod e1000e
modprobe e1000e
