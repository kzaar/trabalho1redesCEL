#!/usr/bin/env python

def chksum():
	
	return

def tonbits (a , nbits) :
	aux = "{0:b}".format(a)
	return aux.zfill(nbits)
		

def mkmsg(prot, opt=None):
	version = 2 #4bits
	msg = tonbits(version, 4)

	global mopt
	mopt = ""
	#IHL
	#numero de WORDs 32-bit
	#minimo = 5 (5x32 = 160bits) (sem options)
	#maximo = 15(15x32 = 480bits)
	if opt == None:
		IHL = 5 #4bits
	else:
		IHL = 5 + int(16*len(opt)/32) + int(16*len(opt) % 32 > 0)
		if IHL > 15:
			IHL = 15
		for c in opt:
			mopt = mopt + tonbits(ord(c), 16)			
	msg = msg + tonbits(IHL, 4)

	typeofversion = 0 #8bits
	msg = msg + tonbits(typeofversion, 8)
 
	totallenght = IHL*4 #numero total de bytes (160bits = 20bytes)
	#16bits
	msg = msg + tonbits(totallenght, 16)
	
	idmsg = 0 #16bits
	msg = msg + tonbits(idmsg, 16)
	
	flags = '000'
	msg = msg + flags

	fragoffset = 0 #13bits
	msg = msg + tonbits(fragoffset, 13)

	timetolive = 64 #8bits
	msg = msg + tonbits(timetolive, 8)

	#protocol
	#1	ps
	#2	df
	#3	finpger
	#4	uptime
	pdict = {'ps':1, 'df':2, 'finger':3, 'uptime':4}
	protocol = pdict.get(prot) #8bits
	msg = msg + tonbits(protocol, 8)

	#srcaddr 127.0.0.1 32bits
	msg = msg + tonbits(127, 8)
	msg = msg + tonbits(0 , 8)
	msg = msg + tonbits(0 , 8)
	msg = msg + tonbits(1 , 8)

	#dstaddr 127.0.0.1 32bits
	msg = msg + tonbits(127, 8)
	msg = msg + tonbits(0 , 8)
	msg = msg + tonbits(0 , 8)
	msg = msg + tonbits(1 , 8)

	if mopt:
		msg = msg + mopt

	#padding
	pad = int((len(msg)+16) % 32)
	if pad:
		a = ''
		msg = msg + a.zfill(pad)
	
	#crc #16bits
	crcindex = 79

	#bin to bytes
	n = int(msg, 2)
	data = bytes([n])	

	return data
