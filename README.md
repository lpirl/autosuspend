# Autosuspend

This script suspends a computer based on the network activity.

This is useful, if you have a server that is accessed
rarely and that is able to wake on unicast packets.

It was written for a proof of concept, that servers can be suspended
in order to save resources.

### Installation

You need Python 3.

Checkout this repository and simply run `./autosuspend.py`.

If you are not interested in what autosuspend is doing, invoke with
`pyhton3 -O ./autosuspend.py` (recommended).

In Debian, one would put something like this in `/etc/rc.local`:

	nice -n 10 /usr/bin/python3 -O /path/to/autosuspend.py &



### Configuration

The first few lines in `autosuspend.py`.

### Dispatchers

Executable scripts in `autosuspend.pre/` and `autosuspend.post/` will be run
(guess what:) right before and after suspending.
Scripts exiting with a status other than `0` in `autosuspend.pre/` can
prevent the machine from suspending.

## How to set up a automatically suspending server

TODO: Write detailed manual.
