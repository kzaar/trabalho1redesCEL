#!/usr/bin/env python

def mkmsg(prot, opt):
	version = 2
	
	#IHL
	#numero de WORDs 32-bit
	#minimo = 5 (5x32 = 160bits) (sem options)
	#maximo = 15(15x32 = 480bits)
	IHL = 5

	typeofversion = 0
	totallenght = 20 #numero total de bytes (160bits = 20bytes)
	idmsg = 0
	flags = 000
	fragoffset = 0
	timetolive = 64

	#protocol
	#1	ps
	#2	df
	#3	finger
	#4	uptime
	pdict = {'ps':1, 'df':2, 'finger':3, 'uptime':4}
	protocol = pdict.get(prot)

	#headerchksum calculado por ultimo
	srcaddr = '127.0.0.1'
	dstaddr = '127.0.0.1'
	options = opt ##fazer um if para tratar opt!=0 que afeta o IHL

