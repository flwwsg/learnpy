#!/usr/bin/python3
import sys
import mailconfig
sys.path.append('..')
print('config:', mailconfig.__file__)

# from mailFetcher import MailFetcherConsole
# from mailParser import MailParser
# from mailSender import MailSender, MailSenderAuthConsole
from mailtools import (MailFetcherConsole, 
                       MailSender, MailSenderAuthConsole, 
                       MailParser)

if not mailconfig.smtpusername:
	sender = MailSender()
else:
	sender = MailSenderAuthConsole()

sender.sendMessage(From 	 = mailconfig.myaddress,
				   To		 = [mailconfig.recevieaddr],
				   Subj		 = 'testing mailtools package',
				   extrahdrs = [('X-Mailer', 'mailtools')],
				   bodytext  = 'Here is my source code\n',
				   attaches  = ['selftest.py']
				)

fetcher = MailFetcherConsole()
def status(*args): print(args)

hdrs, sizes, loadedall = fetcher.downloadAllHeaders(status)
for num, hdr in enumerate(hdrs):
	# print('header is:',hdr)
	if input('load mail?') in ['y', 'Y']:
		print(fetcher.downloadMessage(num+1).rstrip(), '\n', '-'*70)

totalmail = len(hdrs)
if totalmail < 5:
	last5 = 1
else:
	last5 = totalmail-4

msgs, sizes, loadedall = fetcher.downloadAllMessages(status, loadfrom=last5)
# for msg in msgs:
# 	print(msg[:200], '\n', '-'*70)

parser = MailParser()
# print('\nparser messages, tottal messages is %d\n' % len(msgs))
for msg in msgs:
	fulltext = msg
	print('='*80,'msg is:',fulltext,'='*80,sep='\n')
	message = parser.parseMessage(fulltext)
	ctype, maintext = parser.findMainText(message)
	print('Parsed:', message['Subject'])
	print(maintext)