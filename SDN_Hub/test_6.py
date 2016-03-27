#! /usr/bin/env python

"""
*  This is an emulation about 1 Router(router_1), 1 Bridge(bridge_1),
*   4 Hosts(host_1, host_2, host_3, host_4), 2 VLAN groups(mybr_10, mybr_20),
*   and host_1 & host_2 in mybr_10, host_3 & host_4 in mybr_20,
*   then use trunk to connect 2 VLAN.
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf

if '__main__' == __name__:
    net = Mininet(link=TCLink)

    host_1 = net.addHost('host_1')
    host_2 = net.addHost('host_2')
    host_3 = net.addHost('host_3')
    host_4 = net.addHost('host_4')
    router_1 = net.addHost('router_1')
    bridge_1 = net.addHost('bridge_1')

    net.addLink(host_1, bridge_1)
    net.addLink(host_2, bridge_1)
    net.addLink(host_3, bridge_1)
    net.addLink(host_4, bridge_1)
    net.addLink(bridge_1, router_1)

    net.build()

    host_1.cmd('ifconfig host_1-eth0 0')
    host_2.cmd('ifconfig host_2-eth0 0')
    host_3.cmd('ifconfig host_3-eth0 0')
    host_4.cmd('ifconfig host_4-eth0 0')
    router_1.cmd('ifconfig router_1-eth0 0')
    bridge_1.cmd('ifconfig bridge_1-eth0 0')
    bridge_1.cmd('ifconfig bridge_1-eth1 0')
    bridge_1.cmd('ifconfig bridge_1-eth2 0')
    bridge_1.cmd('ifconfig bridge_1-eth3 0')
    bridge_1.cmd('ifconfig bridge_1-eth4 0')

    # set trunk tunnel
    router_1.cmd("vconfig add router_1-eth0 10")
    router_1.cmd("vconfig add router_1-eth0 20")
    bridge_1.cmd("vconfig add bridge_1-eth4 10")
    bridge_1.cmd("vconfig add bridge_1-eth4 20")

    # set vlan groups
    bridge_1.cmd("brctl addbr mybr_10")
    bridge_1.cmd("brctl addbr mybr_20")
    bridge_1.cmd("brctl addif mybr_10 bridge_1-eth0")
    bridge_1.cmd("brctl addif mybr_10 bridge_1-eth1")
    bridge_1.cmd("brctl addif mybr_10 bridge_1-eth4.10")
    bridge_1.cmd("brctl addif mybr_20 bridge_1-eth2")
    bridge_1.cmd("brctl addif mybr_20 bridge_1-eth3")
    bridge_1.cmd("brctl addif mybr_20 bridge_1-eth4.20")

    router_1.cmd('ifconfig router_1-eth0.10 up')
    router_1.cmd('ifconfig router_1-eth0.20 up')
    bridge_1.cmd('ifconfig bridge_1-eth4.10 up')
    bridge_1.cmd('ifconfig bridge_1-eth4.20 up')
    bridge_1.cmd('ifconfig mybr_10 up')
    bridge_1.cmd('ifconfig mybr_20 up')

    router_1.cmd('ifconfig router_1-eth0.10 192.168.10.254 netmask 255.255.255.0')
    router_1.cmd('ifconfig router_1-eth0.20 192.168.20.254 netmask 255.255.255.0')
    router_1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    host_1.cmd("ip address add 192.168.10.1/24 dev host_1-eth0")
    host_1.cmd("ip route add default via 192.168.10.254")
    host_2.cmd("ip address add 192.168.10.2/24 dev host_2-eth0")
    host_2.cmd("ip route add default via 192.168.10.254")
    host_3.cmd("ip address add 192.168.20.1/24 dev host_3-eth0")
    host_3.cmd("ip route add default via 192.168.20.254")
    host_4.cmd("ip address add 192.168.20.2/24 dev host_4-eth0")
    host_4.cmd("ip route add default via 192.168.20.254")

    CLI(net)
    net.stop()
