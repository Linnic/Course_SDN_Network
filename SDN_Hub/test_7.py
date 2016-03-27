#! /usr/bin/env python

"""
*  This is an emulation about 2 Switches(switch_1, switch_2), 
*   4 Hosts(host_1, host_2), 2 VLAN Groups(vlan_10, vlan_20),
*   and host_1 & host_4 in vlan_20, host_2 & host_3 in vlan_10
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf

if '__main__' == __name__:
    net = Mininet(link=TCLink)

    host_1 = net.addHost('host_1')
    host_2 = net.addHost('host_2')
    host_3 = net.addHost('host_3')
    host_4 = net.addHost('host_4')
    switch_1 = net.addHost('switch_1')
    switch_2 = net.addHost('switch_2')

    Link(host_1, switch_1)
    Link(host_2, switch_1)
    Link(host_3, switch_2)
    Link(host_4, switch_2)
    Link(switch_1, switch_2)

    net.build()

    # Clear switch setting
    switch_1.cmd('ifconfig switch_1-eth0 0')
    switch_1.cmd('ifconfig switch_1-eth1 0')
    switch_1.cmd('ifconfig switch_1-eth2 0')
    switch_2.cmd('ifconfig switch_2-eth0 0')
    switch_2.cmd('ifconfig switch_2-eth1 0')
    switch_2.cmd('ifconfig switch_2-eth2 0')

    # Create trunk tunnel
    switch_1.cmd("vconfig add switch_1-eth2 10")
    switch_1.cmd("vconfig add switch_1-eth2 20")
    switch_2.cmd("vconfig add switch_2-eth2 10")
    switch_2.cmd("vconfig add switch_2-eth2 20")

    switch_1.cmd('ifconfig switch_1-eth2.10 up')
    switch_1.cmd('ifconfig switch_1-eth2.20 up')
    switch_2.cmd('ifconfig switch_2-eth2.10 up')
    switch_2.cmd('ifconfig switch_2-eth2.20 up')

    # Set vlan groups
    switch_1.cmd("brctl addbr vlan_10")
    switch_1.cmd("brctl addbr vlan_20")
    switch_1.cmd("brctl addif vlan_20 switch_1-eth0")
    switch_1.cmd("brctl addif vlan_10 switch_1-eth1")
    switch_1.cmd("brctl addif vlan_10 switch_1-eth2.10")
    switch_1.cmd("brctl addif vlan_20 switch_1-eth2.20")

    switch_2.cmd("brctl addbr vlan_10")
    switch_2.cmd("brctl addbr vlan_20")
    switch_2.cmd("brctl addif vlan_10 switch_2-eth0")
    switch_2.cmd("brctl addif vlan_20 switch_2-eth1")
    switch_2.cmd("brctl addif vlan_10 switch_2-eth2.10")
    switch_2.cmd("brctl addif vlan_20 switch_2-eth2.20")

    switch_1.cmd('ifconfig vlan_10 up')
    switch_1.cmd('ifconfig vlan_20 up')
    switch_2.cmd('ifconfig vlan_10 up')
    switch_2.cmd('ifconfig vlan_20 up')

    host_1.cmd('ifconfig host_1-eth0 10.0.10.1 netmask 255.255.255.0')
    host_2.cmd('ifconfig host_2-eth0 10.0.10.2 netmask 255.255.255.0')
    host_3.cmd('ifconfig host_3-eth0 10.0.10.3 netmask 255.255.255.0')
    host_4.cmd('ifconfig host_4-eth0 10.0.10.4 netmask 255.255.255.0')

    CLI(net)
    net.stop()
