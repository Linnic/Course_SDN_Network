#!/usr/bin/env python

"""
*  This is an emulation about using 3 Hosts(host_1, host_2, 
*   host_3), and a Router(router_1).
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf

if '__main__' == __name__:
    net = Mininet(link=TCLink)
  
    host_1 = net.addHost('host_1')
    host_2 = net.addHost('host_2')
    host_3 = net.addHost('host_3')
    router_1 = net.addHost('router_1')

    # Set link bandwidth, Queue size and token bucket burst
    linkopts1 = {'bw':100, 'max_queue_size':50, 'use_htb':True}

    net.addLink(host_1, router_1, cls=TCLink, **linkopts1)
    net.addLink(host_2, router_1, cls=TCLink, **linkopts1)
    net.addLink(host_3, router_1, cls=TCLink, **linkopts1)

    net.build()

    router_1.cmd('ifconfig router_1-eth0 192.168.10.1 netmask 255.255.255.0')
    router_1.cmd('ifconfig router_1-eth1 192.168.20.1 netmask 255.255.255.0')
    router_1.cmd('ifconfig router_1-eth2 192.168.30.1 netmask 255.255.255.0')
    router_1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    host_1.cmd('ifconfig host_1-eth0 0')
    host_2.cmd('ifconfig host_2-eth0 0')
    host_3.cmd('ifconfig host_3-eth0 0')

    host_1.cmd("ip address add 192.168.10.2/24 dev host_1-eth0")
    host_1.cmd("ip route add default via 192.168.10.1 dev host_1-eth0")
    host_2.cmd("ip address add 192.168.20.2/24 dev host_2-eth0")
    host_2.cmd("ip route add default via 192.168.20.1 dev host_2-eth0")
    host_3.cmd("ip address add 192.168.30.2/24 dev host_3-eth0")
    host_3.cmd("ip route add default via 192.168.30.1 dev host_3-eth0")

    CLI(net)
    net.stop()
