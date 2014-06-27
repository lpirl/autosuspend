=========================================================================
how to set up an automatically suspending and waking server (using Linux)
=========================================================================

.. contents::
	:depth: 2

.. raw:: pdf

	PageBreak oneColumn

motivation
----------

Servers experience a growing importance in today's overall
IT infrastructure. Nearly every application or service
requires at least one of them.

Besides the engagement of the operators to maximize the efficiency
of their servers and data centers,
there are more things that can be taken into account
in order to lower the power consumption of the machines for the cost of a little performance decrease.

A bunch of proven mechanisms to reduce power consumption can be found
in consumer machines, such as notebooks. These mechanisms include
CPU/GPU frequency scaling, power management of devices or
the power states of the machine itself (hibernate, sleep, …).

As a prove of concept, I decided to try to set up a server that suspends
automatically when it is idle and that is waking up again if there is
work to be done. This obviously only makes sense, if the services
on that server are not accessed too frequently:
the more idle times, the better.
Due to the concept that the uptime is controlled by the actual usage,
you can pick a relatively strong machine, if the service profits
from that.

In my case, the machine is a storage server to hold user data
and backups of other machines (each redundantly and encrypted).
When it's up and running, it needs about 150 Watts for several
harddisks and a relatively strong and old CPU.
It is a question of resources for me *not* to run this device 24/7
(*not* speaking about monetary resources in the first place).

target audience
...............

People that have basic knowledge of how to administrate a Linux machine.
I will neither explain everything step-by-step nor in a very detailed
way.
Most things are explained very well somewhere else.
You should feature basic skills as a terminal-ninja (edit files,
navigate through the file system, modify commands and adjust
configurations to cater your distribution/needs/environment,
search and install missing software).

requirements
------------

This document assumes Linux to be installed on the servers you plan to use.

For the server side, you pick any machine that fits your purpose.
There is only one thing, your machine (especially network interface card,
motherboard and BIOS) should support: **Wake on unicast**.
This is very similar to *WakeOnLan* but instead of using a so called
*MagicPaket* your network interface can wake the machine on an ordinary
request that is addressed to itself.

Check if your device support wake on unicast:

.. code-block:: bash

	# as root
	ethtool eth0 | grep 'Supports Wake' | cut -d: -f2 | \
		grep -c u && echo lucky || echo not lucky

Please change your interface name accordingly.
For the whole how-to, I'll stick to ``eth0``.

Once you found a machine printing "lucky" when running the command above,
you need to make sure you can **modify the aging time of the ARP cache**
of your network devices (routers and switches).
This can get a bit difficult, because most consumer network hardware
does not allow you to modify those values.

If you run managed switches or something with alternative firmware
(such as DD-WRT, OpenWRT, …), you are probably able to turn off
ARP cache aging. If not, please crawl through the corresponding
configuration interface to see if you are lucky again.

If you do not have a possibility to modify the ARP cache aging time,
one way out would be to use a proxy (see below)
and connect your suspending server directly to it
(no intermediates, only one single cable).

To make the whole thing much more comfortable, you preferably use a
very low power consuming, fanless machine
as a [proxy](#proxy) to your suspending server.

suspending
----------

The probably most important part is to suspend the machine when it's idle.
Since servers communicate through their network interface with the
rest of the world, network activity seems to be the measure to
determine if some client uses a services or not.

There is a small script that
monitors network activity and suspends a machine when the activity
drops below certain thresholds.

Please clone the `repository <https://github.com/lpirl/autosuspend/>`_
somewhere to your suspending server.

``autosuspend.py``: **What it does** (configuration options in brackets):
frequently (``INTERVAL``) count transmitted packets for a
network interface (``interface``) and suspend the machine if there
is an interval (``TIMEOUT``) with less than a few
(``THRESHOLD``) packets transmitted.

Please configure these values in ``autosuspend.py`` according to your
needs (possibly needs experimentation).

**Right before** the actual suspend, all executables in ``autosuspend.pre``
are executed. If an executable has an exit code other than ``0``,
the machine will *not* suspend.

The scripts in that directory provide some basics for system configuration,
check some settings that are hard/willingly not to set with a script
or some environment checks
(to avoid suspending an upgrading machine, for example).

Please *read* the comments of the files in ``autosuspend.pre`` to see what
is happening, customize them to your system if needed or
add/remove scripts as you like.

**Right after** the suspend, all executables in ``autosuspend.post``
are executed. Exit codes do not matter here.

Please read, customize, add/remove them too, as you did with the ones in
``autosuspend.pre``.

You should start ``autosuspend.py`` at boot time.
On Debian, you could add the following line to your ``/etc/rc.local``:

.. code-block:: bash

	nice -n 10 /path/to/autosuspend.py eth0 &

If your machine does not come back from the suspension, you may have to
check you BIOS for

	* [enable] WakeOnLan
	* [enable] PCI devices wake
	* [enable] PCI devices always on/stay on

and alike.

the ARP-thing
-------------

The server will wake on unicast packets.
Unicast packets are addressed using the MAC address of a network device.
The clients will try to find this MAC address using the
*address resolution protocol* (*ARP*).
The *ARP* relies on broadcast packets.
The sleeping server does not answer those broadcasts
(intentionally, because it would wake up too often).

An important step is to configure clients and network devices to be able
to send unicast packets without getting answers to broadcasts.

clients
.......

There are two possible alternatives to connect the clients to the
suspending server. The more obvious way is to connect them directly
requires you to `modify all ARP caches`_, thus setting up a `proxy`_
seems to be the more elegant solution.

proxy
~~~~~

The proxy is a separate machine and will be contacted by all the
clients and will 'hide' the suspending server.

Now, if you add a static entry for the suspending server to ARP cache
of your proxy, it is always capable of sending unicast packets to the
suspending server without doing ARP request.
If the suspended server receives such packet, it will wake up.
Clients will notice a short delay for the first request
(e.g. 4 seconds between a ping to a suspended machine and the first
reply).

This is how you add the static ARP cache entry:

.. code-block:: sh

	arp -i eth0 -s 192.168.1.10 00:19:66:46:33:b5

Do this at boot automatically.
On Debian, you could put it in ``/etc/rc.local``.

Because the proxy must be powered up 24/7, you should pick the least
power consuming machine you can get.
I recommend (and use myself) a **fanless** computer (such as a Nettop)
with an SSD.
There is no single moving part and that keeps maintenance, power consumption
and noise at a minimum.

Since being a proxy is an easy job most of the time, it is a good idea to
combine the use of that proxy with something else.
For example: put it close to your TV and use it as an `HTPC <http://en.wikipedia.org/wiki/HTPC>`_.

It works well to **run the services on the proxy**
(sfp server, web server, …) and **mount data from the suspending server**.
I have no experience if it works out well, if the suspending server
is just NATed behind the proxy using ``iptable``
(please tell me, if you try this!).

modify all ARP caches
~~~~~~~~~~~~~~~~~~~~~

The **less preferred** way to enable the clients waking the server is
to tell them the MAC address of the IP address of the
suspending server.

This is inflexible and annoying on some operating systems and
- even worse - impossible for some scenarios.

Nevertheless,
on **Windows** you can add an ARP cache entry with the following command:

.. code-block:: batch

	netsh interface ip add neighbors "Local Area Connection" "192.168.1.10" "00-19-66-46-33-b5"
	:: if you want to wake the suspended server:
	ping 192.168.1.10

It is required to run the above ``netsh`` command regularly
(with the Windows Task Scheduler),
since you cannot modify Windows' ARP cache timeout
(except you are a proud user of `Windows Server 2003 and older
<http://technet.microsoft.com/en-us/library/cc739819(v=ws.10).aspx>`_).

In Windows Vista and younger (including the server products),
the ARP cache timeout is chosen
`randomly <http://support.microsoft.com/kb/949589>`_ (sigh…).
So you could add the entry every 10 seconds to be sure.
This seems to be a little bit excessive, so you may experiment
with higher value here (no experiences).

On **UNIX-like** operating systems, it is possible to add a static ARP
cache entry with the follwing command:

.. code-block:: sh

	arp -i eth0 -s 192.168.1.10 00:19:66:46:33:b5
	# if you want to wake the suspended server:
	ping 192.168.1.10

The entry will stay there until shutdown.
You can put it in ``/etc/rc.local`` (Debian) to add an entry at boot.


network devices
...............

Please **disable the ARP cache aging** on all network devices that are
intermediates between the suspending server and potential clients.
By doing so, network devices know where to forward unicast packets for
the sleeping server to.

Technical background: for example, a switch receives an unicast packet on
port 1.
Now it is looking into that packet to see who should receive that packet.
The switch is looking up that receiver in its ARP cache.
(A) Cache hit: forward the packet to the port that is
assigned to the receiver's MAC address in the cache.
(B) cache miss: do an ARP request on all ports: the suspended server will
not answer (to keep the number of 'false wakes' as low as possible).

If you cannot add an ARP cache entry or modify the ARP cache timeout
at your switches or routers,
you won't be able to wake the server through those devices.
This is especially important for routers (gateways) to 'transparently'
wake your machine from the Internet.

On linux based routers and switches, you probably have shell access and
can run the following command to modify ARP cache aging:

.. code-block:: sh

	# two days in seconds = 60 * 60 * 24 * 2 = 172800
	# as root
	echo 172800 > /proc/sys/net/ipv4/neigh/eth0/gc_stale_time
	echo 172800 > /proc/sys/net/ipv6/neigh/eth0/gc_stale_time

or you add the following lines to ``/etc/sysctl.conf``:

.. code-block:: cfg

	net.ipv4.neigh.eth0.gc_stale_time = 172800
	net.ipv6.neigh.eth0.gc_stale_time = 172800

and reboot.

services
--------

Generally: avoid frequent access such as pings and keepalives.

Focus on as few services as possible.
It makes it easier to "debug" your suspending server
(read: to find out why it is powered up too often) and - as always -
lowers administrative work and helps you to focus on securing the few
services.

Use something like

.. code-block:: bash

	# as root
	netstat -anp|egrep 'LISTEN |Address'

to see which program is listening to the rest of the world.

HTTP
....

If - for instance - the proxy serves the data mounted from the suspending server,
**do not mount them to /** or at least use a port other than 80 or 8080.

Every few minutes, some crawler pops by and asks for
/ at your domain or IP-Address (yes, this also happens if you don't have
a domain).
Thus, make sure that hits on / of your site do not require access to the suspending server in order to avoid unnecessary wake-ups.

SSHFS / SFTP
............

Sad story, but even if you disable KeepAlive in your ssh_config,
ssh woke my machine very regularly so that I had no time in suspend in
the end. **Don't use it for permanent mounts**
(or tell me how to keep it from talking to the server all the time).

If you want to use SFTP anyways, you'd have to use *autofs*
(or the *automount* mount option for *systemd*, respectively).

SMB
...

This protocol worked very well for me. We know that SMB is normally not
the way to go, but it provides interoperability and does only talk to
the server when it is actually in use.
Works like a charm with permanent mounts.

NFS
...

I have no experience with NFS but I would expect it to behave like SMB
concerning network communication.

cron
....

Remember: your machine is not up all the time.
Use a task scheduler that does not assume your system to be up always
or regularly (you could use: *fcron*, *anachron*, *vixie cron*, …).

ntp
...

Synchronize your clock using *ntp*. Most BIOS clocks are bad.
