#!/bin/bash

exit $(( $(grep "NETDOWN" /etc/default/halt|grep -c no) - 1 ))
