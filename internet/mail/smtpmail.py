#!/usr/bin/python3

import smtplib, sys, email.utils, mailconfig

mailserver = mailconfig.smtpservername
From = mailconfig.myaddress
To = input('To? ').strip()
Tos = To.split(';')
Subj = input('Subj? ').strip()
Date = email.utils.formatdate()
Passwd = open(mailconfig.smtppasswdfile).readlines()[0]

text = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n' % (
		From ,To, Date, Subj
	))
print('Type message text, end with line=[Ctrl+d (unix), Ctrl+z (windwos)]')
while True:
	line = sys.stdin.readline()
	if not line:
		break
	# if line[:4] == 'From':
		# line = '>' + line
	text += line

print('Connecting...')
server = smtplib.SMTP_SSL(mailserver, 465)
server.login(From, Passwd)
failed = server.sendmail(From, Tos, text)
if failed:
	print('Failed recipients:', failed)
else:
	print('No error')
print('Bye')
		# smail.sendmail(server['usr'], receiver, msg.as_string())
