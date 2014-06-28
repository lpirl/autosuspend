# Autosuspend

This script suspends a computer based on the network activity.

This is useful, if you have a server that is accessed
rarely and that is able to wake on unicast packets.

It was written for a proof of concept, that servers can be suspended
in order to save resources.

### Installation

(Pssssst: for best success, you want to read the detailed How-to. See bottom of page.)

You need Python 3.

Checkout this repository and simply run `./autosuspend.py eth0`.

If you are interested in what autosuspend is doing, invoke with
`./autosuspend.py -d eth0`.

In Debian, one would put something like this in `/etc/rc.local`:

	nice -n 10 /path/to/autosuspend.py eth0 &

### Configuration

See `./autosuspend.py -h`.

### Dispatchers

Executable scripts in `autosuspend.pre/` and `autosuspend.post/` will be run
(guess what:) right before and after suspending.
Scripts exiting with a status other than `0` in `autosuspend.pre/` will
prevent the machine from suspending.
Every script will receive the interface we are listening on as only argument.

## Detailed How-to

See [here](howto.rst "how to").
