#!/usr/bin/env python

"""
*  This is an emulation about 3 Hosts(host_1, host_2, host_3) 
*   & 1 Bridge(bridge), and in a Group "mybr"
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf

if '__main__' == __name__:
    net = Mininet(link=TCLink)

    host_1 = net.addHost('host_1')
    host_2 = net.addHost('host_2')
    host_3 = net.addHost('host_3')
    bridge = net.addHost('bridge')

    net.addLink(host_1, bridge)
    net.addLink(host_2, bridge)
    net.addLink(host_3, bridge)

    net.build()

    host_1.cmd('ifconfig host_1-eth0 0')
    host_2.cmd('ifconfig host_2-eth0 0')
    host_3.cmd('ifconfig host_3-eth0 0')

    bridge.cmd('ifconfig bridge-eth0 0')
    bridge.cmd('ifconfig bridge-eth1 0')
    bridge.cmd('ifconfig bridge-eth2 0')

    # Add a group: mybr
    bridge.cmd("brctl addbr mybr")
    
    bridge.cmd("brctl addif mybr bridge-eth0")
    bridge.cmd("brctl addif mybr bridge-eth1")
    bridge.cmd("brctl addif mybr bridge-eth2")

    # Wake up group
    bridge.cmd('ifconfig mybr up')

    host_1.cmd("ip address add 192.168.10.1/24 dev host_1-eth0")
    host_2.cmd("ip address add 192.168.10.2/24 dev host_2-eth0")
    host_3.cmd("ip address add 192.168.10.3/24 dev host_3-eth0")

    CLI(net)
    net.stop()
