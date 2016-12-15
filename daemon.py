#!/usr/bin/env python

import socket, sys, getopt
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
	print PORT + " erro ao vincular a porta"
	sys.exit(2)

s.listen(10)
print PORT + 'socket listening'

def rundata(data):
	#TODO
	return

def clientthread(con):

	while True:
		data = con.recv(1024)
		if not data:
			break
		else:
			rundata(data)	
	
	con.close()

while 1:
	
	con, addr = s.accept()
	print PORT + 'conectado'
	start_new_thread(clientthread, (con,))

s.close()
