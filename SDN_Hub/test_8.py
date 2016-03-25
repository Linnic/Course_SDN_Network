#!/usr/bin/python

"""
*  This is an emulation about a Host(host_1) & a Router(router_1)
*   in the Mininet, and the host_1 can connect to other system 
*   on Virtualbox by the router_1.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info

def myNetwork():
    net = Mininet()
    
    host_1 = net.addHost('host_1', ip='192.168.0.10/24')
    router_1 = net.addHost('router_1')

    net.addLink(host_1, router_1)

    # Interface binding with the SDN_hub's eth1 
    Intf( 'eth1', node=router_1)

    # Print information
    info( '*** Starting network\n')

    net.start()

    router_1.cmd('ifconfig router-eth0 0')
    router_1.cmd('ifconfig router-eth1 0')
    router_1.cmd("ip addr add 192.168.0.1/24 brd + dev router_1-eth0")
    router_1.cmd("ip addr add 10.0.0.1 brd + dev router_1-eth1")
    router_1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    host_1.cmd("ip route add default via 192.168.0.1")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
