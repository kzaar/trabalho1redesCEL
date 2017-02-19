# Relatório Projeto 2

### Router mininet
  
router.py:

```python
#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import Node

class Router(Node):

	ID = 0
	def __init__(self,name,**kwargs):
		kwargs['inNamespace'] = True
		Node.__init__(self,name,**kwargs)
		Router.ID += 1
		self.node_id = Router.ID

	
	def config(self,**params):
		super(Router,self).config(**params)
		#Enable IP forward
		self.cmd('sysctl net.ipv4.ip_forward=1')

	def terminate(self):
		self.cmd('sysctl net.ipv4.ip_forward=0')
		super(Router,self).terminate()
```

## Lab1 : Configuração Básica de Roteadores Cisco

lab1.py:

```python
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
```
output:

```
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3 r1 
*** Adding switches:
s1 
*** Adding links:
(h1, s1) (h2, s1) (h3, r1) (s1, r1) 
*** Configuring hosts
h1 h2 h3 r1 
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 r1 
h2 -> h1 h3 r1 
h3 -> h1 h2 r1 
r1 -> h1 h2 h3 
*** Results: 0% dropped (12/12 received)
*** Done
```

## Lab2: 

lab2.py

```python
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

class Lab2Topo(Topo):

	def __init__(self):
		super(Lab2Topo,self).__init__()
		r1 = self.addNode('r1', cls=Router, ip='192.168.0.249/30',
			defaultRoute='via 192.168.0.251')
		r2 = self.addNode('r2', cls=Router, ip='192.168.0.250/30',
			defaultRoute='via 192.168.0.251')
		
		h1_1 = self.addHost('h1-1', ip='192.168.1.1/24',
			defaultRoute='via 192.168.1.254')
		h1_2 = self.addHost('h1-2', ip='192.168.1.2/24',
			defaultRoute='via 192.168.1.254')
		h2_1 = self.addHost('h2-1', ip='192.168.2.1/24',
			defaultRoute='via 192.168.2.254')
		h2_2 = self.addHost('h2-2', ip='192.168.2.2/24',
			defaultRoute='via 192.168.2.254')
		h3_1 = self.addHost('h3-1', ip='192.168.3.1/24',
			defaultRoute='via 192.168.3.254')
		h3_2 = self.addHost('h3-2', ip='192.168.3.2/24',
			defaultRoute='via 192.168.3.254')
		h8_1 = self.addHost('h8-1', ip='192.168.8.1/24',
			defaultRoute='via 192.168.8.254')
		h8_2 = self.addHost('h8-2', ip='192.168.8.2/24',
			defaultRoute='via 192.168.8.254')
		h9_1 = self.addHost('h9-1', ip='192.168.9.1/24',
			defaultRoute='via 192.168.9.254')
		h9_2 = self.addHost('h9-2', ip='192.168.9.2/24',
			defaultRoute='via 192.168.9.254')

		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s8 = self.addSwitch('s8')
		s9 = self.addSwitch('s9')

		self.addLink(h1_1,s1)
		self.addLink(h1_2,s1)
		self.addLink(h2_1,s2)
		self.addLink(h2_2,s2)
		self.addLink(h3_1,s3)
		self.addLink(h3_2,s3)
		self.addLink(h8_1,s8)
		self.addLink(h8_2,s8)
		self.addLink(h9_1,s9)
		self.addLink(h9_2,s9)

		self.addLink(r1, r2)#, params2={'ip' : '10.0.0.1/8'})
		self.addLink(s1, r1)#, params2={'ip' : '192.168.1.1/24'})
		self.addLink(s2, r1)#, params2={'ip' : '192.168.2.1/24'})
		self.addLink(s3, r1)#, params2={'ip' : '192.168.3.1/24'})
		self.addLink(s8, r2)
		self.addLink(s9, r2)

def run():
	os.system("rm -f /tmp/zebra*.log /tmp/ripd*.log  /tmp/zebra*.pid /tmp/ripd*.pid logs/*")
	os.system("mn -c > /dev/null 2>&1")
	os.system("killall -9 zebra ripd ospfd > /dev/null 2>&1")
	topo=Lab2Topo()
	net = Mininet(topo=topo)
	net.start()

	r1= net.getNodeByName('r1')
	print "Starting zebra on r1"
	r1.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-lab2-r1.conf -d -i /tmp/zebra-r1.pid > logs/lab2-zebra-r1-stdout 2>&1")
	r1.waitOutput()

	print "Starting RIP on r1"
	r1.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-lab2-r1.conf -d -i /tmp/ripd-r1.pid > logs/lab2-ospf-r1-stdout 2>&1")
	r1.waitOutput()

	r2= net.getNodeByName('r2')
	print "Starting zebra on r2"
	r2.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-lab2-r2.conf -d -i /tmp/zebra-r2.pid > logs/lab2-zebra-r2-stdout 2>&1")
	r2.waitOutput()

	print "Starting RIP on r2"
	r2.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-lab2-r2.conf -d -i /tmp/rip-r2.pid > logs/lab2-ospf-r2-stdout 2>&1")
	r2.waitOutput()

	CLI(net)
	net.stop()
	
	print "killing zebras ... RIP :c"	
	os.system("killall -9 zebra ripd ospfd")


if __name__ == '__main__':
	setLogLevel('info')
	run()
```

output:
```
*** Creating network
*** Adding controller
*** Adding hosts:
h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
*** Adding switches:
s1 s2 s3 s8 s9 
*** Adding links:
(h1-1, s1) (h1-2, s1) (h2-1, s2) (h2-2, s2) (h3-1, s3) (h3-2, s3) (h8-1, s8) (h8-2, s8) (h9-1, s9) (h9-2, s9) (r1, r2) (s1, r1) (s2, r1) (s3, r1) (s8, r2) (s9, r2) 
*** Configuring hosts
h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
*** Starting controller
c0 
*** Starting 5 switches
s1 s2 s3 s8 s9 ...
Starting zebra on r1
Starting RIP on r1
Starting zebra on r2
Starting RIP on r2
*** Starting CLI:
mininet> pingall
*** Ping: testing ping reachability
h1-1 -> h1-2 h2-1 h2-2 h3-1 h3-2 X X X X r1 X 
h1-2 -> h1-1 h2-1 h2-2 h3-1 h3-2 X X X X r1 X 
h2-1 -> h1-1 h1-2 h2-2 h3-1 h3-2 X X X h9-2 r1 r2 
h2-2 -> h1-1 h1-2 h2-1 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h3-1 -> h1-1 h1-2 h2-1 h2-2 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h3-2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h8-1 h8-2 h9-1 h9-2 r1 r2 
h8-1 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-2 h9-1 h9-2 r1 r2 
h8-2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h9-1 h9-2 r1 r2 
h9-1 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-2 r1 r2 
h9-2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 r1 r2 
r1 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r2 
r2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 
*** Results: 9% dropped (119/132 received)
mininet> pingall
*** Ping: testing ping reachability
h1-1 -> h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h1-2 -> h1-1 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h2-1 -> h1-1 h1-2 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h2-2 -> h1-1 h1-2 h2-1 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h3-1 -> h1-1 h1-2 h2-1 h2-2 h3-2 h8-1 h8-2 h9-1 h9-2 r1 r2 
h3-2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h8-1 h8-2 h9-1 h9-2 r1 r2 
h8-1 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-2 h9-1 h9-2 r1 r2 
h8-2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h9-1 h9-2 r1 r2 
h9-1 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-2 r1 r2 
h9-2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 r1 r2 
r1 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r2 
r2 -> h1-1 h1-2 h2-1 h2-2 h3-1 h3-2 h8-1 h8-2 h9-1 h9-2 r1 
*** Results: 0% dropped (132/132 received) 
```

  No primeiro comando `<pingall>` o router r1 ainda não havia recebido o routing table de r2.
  
  Router1>sh ip route
  
  ```
  Router1> sh ip route
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, A - Babel,
       > - selected route, * - FIB route

C>* 127.0.0.0/8 is directly connected, lo
O   192.168.0.248/30 [110/10] is directly connected, r1-eth0, 00:00:52
C>* 192.168.0.248/30 is directly connected, r1-eth0
O   192.168.1.0/24 [110/10] is directly connected, r1-eth1, 00:00:52
C>* 192.168.1.0/24 is directly connected, r1-eth1
O   192.168.2.0/24 [110/10] is directly connected, r1-eth2, 00:00:52
C>* 192.168.2.0/24 is directly connected, r1-eth2
O   192.168.3.0/24 [110/10] is directly connected, r1-eth3, 00:00:52
C>* 192.168.3.0/24 is directly connected, r1-eth3
O>* 192.168.8.0/24 [110/20] via 192.168.0.250, r1-eth0, 00:00:02
O>* 192.168.9.0/24 [110/20] via 192.168.0.250, r1-eth0, 00:00:02
```
  
 
 ## Lab3:
 
 lab3.py:
 
 ```python
 
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
```
  
  output:
  
```
```
