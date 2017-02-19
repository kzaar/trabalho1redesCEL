#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Controller
from mininet.log import setLogLevel
from mininet.cli import CLI

class Router(Node):
	
	def config(self,**params):
		super(Router,self).config(**params)
		#Enable forwarding
		self.cmd('sysctl net.ipv4.ip_forward=1')
		
	def terminate(self):
		self.cmd('sysctl net.ipv4.ip_forward=0')
		super(Router,self).terminate()

class NetTopo(Topo):
	#h3 -- router -- switch -- h1,h2
	def build(self, **_opts):
		r1 = self.addNode('r1', cls=Router, ip='192.168.1.1/24')
		
		h1 = self.addHost('h1', ip='192.168.1.100/24',
			defaultRoute='via 192.168.1.1')
		h2 = self.addHost('h2', ip='192.168.1.101/24',
			defaultRoute='via 192.168.1.1')
		h3 = self.addHost('h3', ip='10.0.0.100/8',
			defaultRoute='via 10.0.0.1')

		s1 = self.addSwitch('s1')	

		self.addLink(h1,s1)
		self.addLink(h2,s1)

		self.addLink(s1,r1, intfName2='r1-eth1',
			params2={'ip' : '192.168.1.1/24'})
		self.addLink(h3,r1, intfName2='r1-eth2',
			params2={'ip' : '10.0.0.1/8'})
		

def run():
	topo = NetTopo()
	net = Mininet(topo=topo)
	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	run()
