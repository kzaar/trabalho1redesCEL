#!/usr/bin/env python

import socket, sys, getopt
import msgredes
import subprocess
from thread import *
argv = sys.argv[1:]
if len(argv) != 2:
	print "daemon.py --port <portnumber>"
	sys.exit(2)
if argv[0] != "--port":
	print "daemon.py --port <portnumber>"
	sys.exit(2)
if not argv[1].isdigit():
	print "daemon.py --port <portnumber>"
	sys.exit(2)

PORT = int(argv[1])
HOST = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((HOST, PORT))
except socket.error:
	print str(PORT) + " erro ao vincular a porta"
	sys.exit(2)

s.listen(10)
print str(PORT) + 'socket listening'

def rundata(data, con):
	msg = msgredes.openmsg(data)
	if msg == 0:
		con.send("Erro no protocolo de camada interna")
		return
	elif msg == -1:
		con.send("Erro ao validar CRC16, tente novamente.")
		return
	protocol = msg[msgredes.MSG_PROTOCOL]
	protocol = msgredes.PROTOCOL_COMMAND[protocol]
	options = msg[msgredes.MSG_OPTIONS]
	command = protocol + " " + options
	shellc = [protocol]
	options = options.replace("\x00", "").replace("|","").replace(";","").replace(">","").replace("<","")
	shellc.extend(options.split())
	try:
		output = subprocess.check_output(shellc)
		output = output + "\n" + "return code = 0"
	except subprocess.CalledProcessError as e:
		output = "return code = " + str(e.returncode)	
	
	header = "shell command: :" + command + "\n"
	output = header + output
	con.send(output)
	return

def clientthread(con):

	while True:
		data = con.recv(1024)
		if not data:
			break
		else:
			rundata(data, con)
				
	
	con.close()

while 1:
	
	con, addr = s.accept()
	print str(PORT) + 'conectado'
	start_new_thread(clientthread, (con,))

s.close()
