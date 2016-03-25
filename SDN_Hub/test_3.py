#!/usr/bin/env python

"""
*  This is an emulation about 2 Hosts(host_1, host_2) & 
*  3 routers(router_1, router_2, router_3).
*  A string topology about static routing.
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf

if '__main__' == __name__:
    net = Mininet(link=TCLink)

    host_1 = net.addHost('host_1')
    host_2 = net.addHost('host_2')
    router_1 = net.addHost('router_1')
    router_2 = net.addHost('router_2')
    router_3 = net.addHost('router_3')

    net.addLink(host_1, router_1)
    net.addLink(router_1, router_2)
    net.addLink(router_2, router_3)
    net.addLink(router_3, host_2)

    net.build()

    router_1.cmd('ifconfig router_1-eth0 192.168.10.1 netmask 255.255.255.0')
    router_1.cmd('ifconfig router_1-eth1 192.168.20.1 netmask 255.255.255.0')
    router_1.cmd("ip route add 192.168.30.0/24 via 192.168.20.2")
    router_1.cmd("ip route add 192.168.40.0/24 via 192.168.20.2")
    router_1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    router_2.cmd('ifconfig router_2-eth0 192.168.20.2 netmask 255.255.255.0')
    router_2.cmd('ifconfig router_2-eth1 192.168.30.1 netmask 255.255.255.0')
    router_2.cmd("ip route add 192.168.10.0/24 via 192.168.20.1")
    router_2.cmd("ip route add 192.168.40.0/24 via 192.168.30.2")
    router_2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    router_3.cmd('ifconfig router_3-eth0 192.168.30.2 netmask 255.255.255.0')
    router_3.cmd('ifconfig router_3-eth1 192.168.40.1 netmask 255.255.255.0')
    router_3.cmd("ip route add 192.168.10.0/24 via 192.168.30.1")
    router_3.cmd("ip route add 192.168.20.0/24 via 192.168.30.1")
    router_3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    host_1.cmd('ifconfig host_1-eth0 0')
    host_2.cmd('ifconfig host_2-eth0 0')

    host_1.cmd("ip address add 192.168.10.2/24 dev host_1-eth0")
    host_1.cmd("ip route add default via 192.168.10.1")
    host_2.cmd("ip address add 192.168.40.2/24 dev host_2-eth0")
    host_2.cmd("ip route add default via 192.168.40.1")

    CLI(net)
    net.stop()
