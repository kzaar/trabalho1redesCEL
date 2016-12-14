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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(DAEMON1)

#mensagens para a maquina 1
for i in range(len(m1))[::2]:
	if m1[i] != None:
		msg = mkmsg(m1[i],m1[i+1])
		print(msg)
		#envia a msg, aguarda a resposta e imprime
	
#fazer para as outra maquinas, ou colocar todas em uma matriz 
#e fazer todas em um for

