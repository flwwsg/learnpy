#!/usr/bin/python3
import sys
import mailconfig
print('config:', mailconfig.__file__)

from mailFetcher import MailFetcherConsole
from mailParser import MailParser
from mailSender import MailSender, MailSenderAuthConsole

if not mailconfig.smtpusername:
	sender = MailSender(tracesize=5000)
else:
	sender = MailSenderAuthConsole(tracesize=5000)

sender.sendMessage(From 	 = mailconfig.myaddress,
				   To		 = [mailconfig.recevieaddr],
				   Subj		 = 'testing mailtools package',
				   extrahdrs = [('X-Mailer', 'mailtools')],
				   bodytext  = 'Here is my source code\n',
				   attaches  = ['selftest.py']
				)

fetcher = MailFetcherConsole()
def status(*args):
	print(args)

hdrs, sizes, loadedall = fetcher.downloadAllHeaders(status)
for num, hdr in enumerate(hdrs[:5]):
	print(hdr)
	if input('load mail?') in ['y', 'Y']:
		print(fetcher.downloadAllHeaders(num+1).rstrip(), '\n', '-'*70)

last5 = len(hdrs)-4
msgs, sizes, loadedall = fetcher.downloadAllHeaders(status, loadfrom=last5)
for msg in msgs:
	print(msg[:200], '\n', '-'*70)

parser = MailParser()
for i in [0]:
	fulltext = msgs[i]
	message = parser.parseMessage(fulltext)
	ctype, maintext = parser.findMainText(message)
	print('Parsed:', message['Subject'])
	print(maintext)


