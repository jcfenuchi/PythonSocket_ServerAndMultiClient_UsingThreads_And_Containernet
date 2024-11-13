#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""

import hashlib
from containernet.cli import CLI
from containernet.link import TCLink
from containernet.net import Containernet
from containernet.term import makeTerm
from mininet.node import Controller
from mininet.log import info, setLogLevel
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from os import system


setLogLevel('info')
net = Containernet(controller=Controller,link=wmediumd, wmediumd_mode=interference)

info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
master = net.addDocker('master', ip='10.0.0.1', dimage="core:1.0")
master.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
makeTerm(master, cmd="python3 main.py")

info('*** Adding switches\n')

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

info('*** Creating links\n')
net.addLink(master, s1)
net.addLink(s1, s2)


clients = {}
for node in ['192.168.9.1', '192.168.9.2', '192.168.9.3']:
    minion_node = net.addDocker(name=hashlib.md5(node.encode('utf-8')).hexdigest()[0:10], dimage="minion:1.0")
    clients[node] = minion_node.name
    minion_node.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
    net.addLink(s2, minion_node)



print(clients)
info('*** Starting network\n')
net.build()
net.start()


for nome_ip,node_name  in clients.items():
    minion_node = net.getNodeByName(node_name)
    makeTerm(minion_node, cmd=f"python3 main.py {master.IP()} 6618")
    

info('*** Testing connectivity\n')
net.pingAll()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()