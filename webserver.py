#!/usr/bin/env python
import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()

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

print "Content-Type: text/html\n"
print "M1: %s" % m1[0]
print m1, m2, m3

