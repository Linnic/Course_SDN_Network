#!/usr/bin/python

"""
*  This is an emulation about a Host(host_1) & a Router(router_1)
*   in the Mininet, and the host_1 can connect to Internet 
*   by the router_1 with NAT.
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
    Intf( 'eth0', node=router_1)

    # Print information
    info( '*** Starting network\n')

    net.start()

    router_1.cmd('ifconfig router-eth0 0')
    router_1.cmd('ifconfig router-eth1 0')
    
    # Get ip from NAT's DHCP
    router_1.cmd("dhclient eth0")
    
    router_1.cmd("ip addr add 192.168.0.1/24 brd + dev router_1-eth0")
    router_1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    
    # Change the Intranet IP to NAT IP
    router_1.cmd("iptables -t nat -A POSTROUTING -o eth0 -s 192.168.0.0/24 -j MASQUERADE")

    host_1.cmd("ip route add default via 192.168.0.1")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
