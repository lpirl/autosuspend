#!/bin/bash

(type smbstatus > /dev/null) || exit 0

exit $(smbstatus -p | tail -n +5 | grep -cv nobody)
