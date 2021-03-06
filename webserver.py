#!/usr/bin/env python
import cgitb
import cgi
import socket
from msgredes import mkmsg
cgitb.enable()
form = cgi.FieldStorage()

print "Content-Type: text/html\n"

#	INDEX
# 	0	ps
#	1	ps -
#	2	df
#	3	df -
#	4	finger
#	5	finger -
#	6	uptime
#	7	uptime -

m1 = [form.getvalue('maq1_ps'),
	form.getvalue('maq1-ps'),
	form.getvalue('maq1_df'),
	form.getvalue('maq1-df'),
	form.getvalue('maq1_finger'),
	form.getvalue('maq1-finger'),
	form.getvalue('maq1_uptime'),
	form.getvalue('maq1-uptime')]

m2 = [form.getvalue('maq2_ps'),
	form.getvalue('maq2-ps'),
	form.getvalue('maq2_df'),
	form.getvalue('maq2-df'),
	form.getvalue('maq2_finger'),
	form.getvalue('maq2-finger'),
	form.getvalue('maq2_uptime'),
	form.getvalue('maq2-uptime')]

m3 = [form.getvalue('maq3_ps'),
	form.getvalue('maq3-ps'),
	form.getvalue('maq3_df'),
	form.getvalue('maq3-df'),
	form.getvalue('maq3_finger'),
	form.getvalue('maq3-finger'),
	form.getvalue('maq3_uptime'),
	form.getvalue('maq3-uptime')]

DAEMONIP = "127.0.0.1"
DAEMON1 = (DAEMONIP, 9001)
DAEMON2 = (DAEMONIP, 9002)
DAEMON3 = (DAEMONIP, 9003)

#conexao sequencial
#conectando com DAEMON1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect(DAEMON1)
connected = False
#mensagens para a maquina 1
for i in range(len(m1))[::2]:
	if m1[i] != None:
		if not connected:
			s.connect(DAEMON1)
			connected = True
			print "<h2>Machine 1</h2>"
		msg = mkmsg(m1[i],m1[i+1])
		s.send(msg)
		a = s.recv(1024)
		for line in a.splitlines():
			print "<pre>" + line + "</pre>"
if connected:
	s.close()
	connected = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

#mensagens para a maquina 2
for i in range(len(m2))[::2]:
	if m2[i] != None:
		if not connected:
			s.connect(DAEMON2)
			connected = True
			print "<h2>Machine 2</h2>"
		msg = mkmsg(m2[i],m2[i+1])
		s.send(msg)
		a = s.recv(1024)
		for line in a.splitlines():
			print "<pre>" + line + "</pre>"
if connected:
	s.close()
	connected = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

#mensagens para a maquina 3
for i in range(len(m3))[::2]:
	if m3[i] != None:
		if not connected:
			s.connect(DAEMON3)
			connected = True
			print "<h2>Machine 3</h2>"
		msg = mkmsg(m3[i],m3[i+1])
		s.send(msg)
		a = s.recv(1024)
		for line in a.splitlines():
			print "<pre>" + line + "</pre>"
if connected:
	s.close()
