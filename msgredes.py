#!/usr/bin/env python

import sys

VERSION_INDEX = 0
IHL_INDEX = 4
TOS_INDEX = 8
TOTALLENGHT_INDEX = 16
ID_INDEX = 32
FLAGS_INDEX = 48 
FRAGMENTOFFSET_INDEX = 51
TIMETOLIVE_INDEX = 64
PROTOCOL_INDEX = 72
HEADERCHECKSUM_INDEX = 80
SOURCEADDR_INDEX = 96
DESTADDR_INDEX = 128
OPTIONS_INDEX = 160

MSG_LENGHT = 'MSG_LENGHT'
MSG_ID = 'MSG_ID'
MSG_PROTOCOL = 'MSG_PROTOCOL'
MSG_SOURCE = 'MSG_SOURCE'
MSG_OPTIONS = 'MSG_OPTION'


#protocol
#1	ps
#2	df
#3	finpger
#4	uptime
PROTOCOL_DICT = {'ps':1, 'df':2, 'finger':3, 'uptime':4}
PROTOCOL_COMMAND = [0 ,"ps","df","finger","uptime"]

def chksum(a, validate=0): #TODO
	
	if validate:
		msg_velha = a[0:HEADERCHECKSUM_INDEX] + a[HEADERCHECKSUM_INDEX+16:]
		chksum_velho = a[HEADERCHECKSUM_INDEX:HEADERCHECKSUM_INDEX+16]
		return chksum_velho == chksum(msg_velha)
	else:
	
		crc = 0xFFFF

		for i in range(0, len(a)):
			tmp = (crc >> 8) ^ ord(a[i])
			tmp ^= tmp >> 4
			crc = (crc << 8) ^ (tmp << 12) ^ (tmp << 5) ^ tmp
			crc &= 0xFFFF

		return bin(crc)

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
	protocol = PROTOCOL_DICT.get(prot) #8bits
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
	
	#crc #16bits TODO
	crc = chksum(msg)
	msg = msg[:80] +  crc + msg[80:]

	#bin to bytes 
	n = int(msg, 2)
 
	data = bytes(n) 
	
	return data

def openmsg(data):
	
	n = int(data)
	msg = "{0:b}".format(n)
	msg = "00" + msg # 2 zeros a esquerda sao perdidos nas conversoes
	if len(msg) % 32:
		print "a"
		return 0
	elif int(msg[VERSION_INDEX:IHL_INDEX],2) != 2:
		print "b"
		return 0
	elif int(msg[TIMETOLIVE_INDEX:PROTOCOL_INDEX],2) < 1:
		print "c"
		return 0
	elif int(msg[TOS_INDEX:TOTALLENGHT_INDEX],2) != 0:
		print "d"
		return 0
	elif not chksum(msg, 1):
		return -1

	lenght = int(msg[IHL_INDEX:TOS_INDEX],2)*32
	idmsg = int(msg[ID_INDEX:FLAGS_INDEX],2)
	protocol = int(msg[PROTOCOL_INDEX:HEADERCHECKSUM_INDEX],2)
	sourceaddr = str(int(msg[SOURCEADDR_INDEX:DESTADDR_INDEX-24],2))
	sourceaddr = sourceaddr + '.' + str(int(msg[SOURCEADDR_INDEX+8:DESTADDR_INDEX-16],2))
	sourceaddr = sourceaddr + '.' + str(int(msg[SOURCEADDR_INDEX+16:DESTADDR_INDEX-8],2))
	sourceaddr = sourceaddr + '.' + str(int(msg[SOURCEADDR_INDEX+24:DESTADDR_INDEX],2))
	options = ""
	if lenght > 160:
		for i in range(OPTIONS_INDEX, lenght, 16):
			options = options + chr(int(msg[i:i+16],2))	
	else:
		options = ""
	datarr = { MSG_LENGHT:lenght, MSG_ID:idmsg,
		MSG_PROTOCOL:protocol, MSG_SOURCE:sourceaddr,
		MSG_OPTIONS:options}
	return datarr

