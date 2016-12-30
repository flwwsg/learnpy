#!/usr/bin/python3
import poplib, getpass, sys, mailconfig

mailserver = mailconfig.popservername
mailuser = mailconfig.popusername
mailpasswd = open(mailconfig.poppasswdfile).readlines()[0]

print('Connecting...')
server = poplib.POP3_SSL(mailserver)
server.user(mailuser)
server.pass_(mailpasswd)

try:
	print(server.getwelcome())
	# msgCount = len(server.list())[1]
	msgCount, msgBytes = server.stat()
	print('There are', msgCount, 'mail messages in', msgBytes, 'bytes')
	print(server.list())
	print('-'*80)
	input('[press Enter key]')
	for i in range(msgCount):
		hdr, message, octets = server.retr(i+1)        # octets = bytes
		for line in message:
			print(line.decode())
		print('-'*80)
		if i < msgCount -1:
			input('[press Enter key]')
finally:
	server.quit()
print('Bye.')