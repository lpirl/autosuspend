#!/bin/bash
grep "pci" /proc/acpi/wakeup | \
	grep \*disabled | \
	cut -d" " -f1 | \
	xargs -I{} echo {} > /proc/acpi/wakeup
