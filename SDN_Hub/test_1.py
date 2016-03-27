#!/usr/bin/env python

"""
*  This is an emulation about using 3 Hosts(host_1, host_2, host_3),
*  and set host_2 as a Router
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link,TCLink,Intf

if '__main__' == __name__:
    net = Mininet(link=TCLink)
  
    #Set host
    host_1 = net.addHost('host_1')
    host_2 = net.addHost('host_2')
    host_3 = net.addHost('host_3')

    #Set link type and bandwidth
    linkopts1={'bw':100}
    linkopts2={'bw':100}
    net.addLink(host_1, host_2, cls=TCLink, **linkopts1)
    net.addLink(host_2, host_3, cls=TCLink, **linkopts2)
    """
    *   A simple link :
    *     Link(host_1, host_2)
    *
    *   Set interface of network card :
    *     Link(host_2, host_3, intfName1='host_2-eht1')
    """
    net.build();
  
    # Set IP forward
    host_2.cmd('ifconfig host_2-eth0 192.168.10.1 netmask 255.255.255.0')
    host_2.cmd('ifconfig host_2-eth1 192.168.20.1 netmask 255.255.255.0')
    host_2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # Clear host as default
    host_1.cmd("ifconfig host_1-eth0 0")
    host_3.cmd("ifconfig host_3-eth0 0")

    # Set host IP and default route
    host_1.cmd("ip address add 192.168.10.2/24 dev host_1-eth0")
    host_1.cmd("ip route add default via 192.168.10.1 dev host_1-eth0")
    host_3.cmd("ip address add 192.168.20.2/24 dev host_3-eth0")
    host_3.cmd("ip route add default via 192.168.20.1 dev host_3-eth0")

    CLI(net)
    net.stop()
