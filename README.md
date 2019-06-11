# Autosuspend

This script suspends a computer based on the network activity.

This is useful, if you have a server that is accessed
rarely and that is able to wake on unicast packets.

It was written for a proof of concept, that servers can be suspended
in order to save resources.

### Dispatchers

Executable scripts in the directories `autosuspend.pre/` and `autosuspend.post/` will be run
(guess what) right before and after suspending.
Enable (`$ chmod +x …`) and disable (`$ chmod -x …`) them as you wish.
Scripts exiting with an exit status other than `0` in `autosuspend.pre/` will
prevent the machine from suspending.
Every script will receive the interface we are listening on as the first argument.

### Installation

* for best success, read the [how-to](howto.rst)
* install Python 3.
* clone this repository

  `$ git clone https://github.com/lpirl/autosuspend.git`

* optional: run `$ /path/to/autosuspend.py --help` and choose your desired options

#### automatic

* go to the checked-out directory
* install autosuspend to `/opt`: `$ make install`
* if you want a systemd service to be installed, run `$ make install_systemd_service` as well
* edit the created file `autosuspend.service` to your liking

  (if you do, run `$ systemctl daemon-reload` afterwards)

#### manual

Put something like this in your crontab:

  @reboot nice -n 10 /path/to/autosuspend.py [your options] [your device] &

### Debugging

You can run `$ ./autosuspend.py -d [other options] [your device]` to see why your machine is [not] suspending.

## Detailed How-to

See [here](howto.rst "how to").
