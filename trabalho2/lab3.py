
#!/usr/bin/python

from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.node import Node
from router import Router
from time import sleep

import sys
import os

class Lab3Topo(Topo):

	def __init__(self):
		super(Lab3Topo,self).__init__()
		r1 = self.addNode('r1', cls=Router, ip='176.16.100.1/24',
			defaultRoute='via 176.16.100.254')
		r2 = self.addNode('r2', cls=Router, ip='176.16.100.2/24',
			defaultRoute='via 176.16.100.254')
		r3 = self.addNode('r3', cls=Router, ip='176.16.200.1/24',
			defaultRoute='via 176.16.200.254')		

		h1_1 = self.addHost('h1-1', ip='176.16.10.1/24',
			defaultRoute='via 176.16.10.254')
		h1_2 = self.addHost('h1-2', ip='176.16.10.2/24',
			defaultRoute='via 176.16.10.254')
		h2_1 = self.addHost('h2-1', ip='176.16.20.1/24',
			defaultRoute='via 176.16.20.254')
		h2_2 = self.addHost('h2-2', ip='176.16.20.2/24',
			defaultRoute='via 176.16.20.254')
		h3_1 = self.addHost('h3-1', ip='176.16.30.1/24',
			defaultRoute='via 176.16.30.254')
		h3_2 = self.addHost('h3-2', ip='176.16.30.2/24',
			defaultRoute='via 176.16.30.254')
		h4_1 = self.addHost('h4-1', ip='176.16.40.1/24',
			defaultRoute='via 176.16.40.254')
		h4_2 = self.addHost('h4-2', ip='176.16.40.2/24',
			defaultRoute='via 176.16.40.254')
		h5_1 = self.addHost('h5-1', ip='176.16.50.1/24',
			defaultRoute='via 176.16.50.254')
		h5_2 = self.addHost('h5-2', ip='176.16.50.2/24',
			defaultRoute='via 176.16.50.254')
		h6_1 = self.addHost('h6-1', ip='176.16.60.1/24',
			defaultRoute='via 176.16.60.254')
		h6_2 = self.addHost('h6-2', ip='176.16.60.2/24',
			defaultRoute='via 176.16.60.254')


		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')
		s6 = self.addSwitch('s6')

		self.addLink(h1_1,s1)
		self.addLink(h1_2,s1)
		self.addLink(h2_1,s2)
		self.addLink(h2_2,s2)
		self.addLink(h3_1,s3)
		self.addLink(h3_2,s3)
		self.addLink(h4_1,s4)
		self.addLink(h4_2,s4)
		self.addLink(h5_1,s5)
		self.addLink(h5_2,s5)
		self.addLink(h6_1,s6)
		self.addLink(h6_2,s6)

		self.addLink(r1, r2)
		self.addLink(r2, r3)
		self.addLink(s1, r1)
		self.addLink(s2, r1)
		self.addLink(s3, r2)
		self.addLink(s4, r2)
		self.addLink(s5, r3)
		self.addLink(s6, r3)

def run():
	os.system("rm -f /tmp/zebra*.log /tmp/ospfd*.log  /tmp/zebra*.pid /tmp/ripd*.pid logs/*")
	os.system("mn -c > /dev/null 2>&1")
	os.system("killall -9 zebra ripd ospfd > /dev/null 2>&1")
	topo=Lab3Topo()
	net = Mininet(topo=topo)
	net.start()

	r1= net.getNodeByName('r1')
	print "Starting zebra on r1"
	r1.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-lab3-r1.conf -d -i /tmp/zebra-r1.pid > logs/lab2-zebra-r1-stdout 2>&1")
	r1.waitOutput()

	print "Starting OSPF on r1"
	r1.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-lab3-r1.conf -d -i /tmp/ripd-r1.pid > logs/lab2-ospf-r1-stdout 2>&1")
	r1.waitOutput()

	r2= net.getNodeByName('r2')
	print "Starting zebra on r2"
	r2.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-lab3-r2.conf -d -i /tmp/zebra-r2.pid > logs/lab2-zebra-r2-stdout 2>&1")
	r2.waitOutput()

	print "Starting OSPF on r2"
	r2.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-lab3-r2.conf -d -i /tmp/rip-r2.pid > logs/lab2-ospf-r2-stdout 2>&1")
	r2.waitOutput()

	r3= net.getNodeByName('r3')
	print "Starting zebra on r3"
	r3.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-lab3-r3.conf -d -i /tmp/zebra-r3.pid > logs/lab2-zebra-r3-stdout 2>&1")
	r3.waitOutput()

	print "Starting OSPF on r3"
	r3.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-lab3-r3.conf -d -i /tmp/ripd-r3.pid > logs/lab3-ospf-r1-stdout 2>&1")
	r3.waitOutput()


	CLI(net)
	net.stop()
	
	print "killing zebras and ospfd :c"	
	os.system("killall -9 zebra ospfd")


if __name__ == '__main__':
	setLogLevel('info')
	run()
