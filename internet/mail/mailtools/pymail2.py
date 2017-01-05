#!/usr/bin/python3
import sys
sys.path.append('../')

import mailconfig, mailtools
from pymail import inputmessage
mailcache = {}

def fetchmessage(i):
	try:
		fulltext = mailcache[i]
	except KeyError:
		fulltext = fetcher.downloadMessage(i)
		mailcache[i] = fulltext

	return fulltext

def sendmessage():
	From, To, Subj, text = inputmessage()
	sender.sendMessage(From, To, Subj, [], text, attaches=None)

def deletemessage(toDelete, verify=True):
	print('To be deleted:', toDelete)
	if verify and input('Delete? ')[:1] not in ['y','Y']:
		print('Delete cancelled.')
	else:
		print('Deleting messages from server...')
		fetcher.deleteMessages(toDelete)

def showindex(msgList, msgSizes, chunk=5):
	count = 0
	for (msg, size) in zip(msgList, msgSizes):
		count += 1
		print('%d:\t%d bytes' % (count, size))
		for hdr in ('From', 'To', 'Date', 'Subject'):
			print('\t%-8s=>%s' % (hdr, msg.get(hdr, '(unknown)')))
		if count % chunk == 0:
			input('[press any key]')

def showmesssage(i, msgList):
	if 1 <= i <= len(msgList):
		fulltext = fetchmessage(i)
		message = parser.parseMessage(fulltext)
		ctype, maintext = parser.findMainText(message)
		print('-'*80)
		print(maintext.rstrip()+'\n')
		print('-'*80)
	else:
		print('Bad message number')

def savemessage(i, mailfile, msgList):
	if 1 <= i <= len(msgList):
		fulltext = fetchmessage(i)
		savefile = open(mailfile, 'a', encoding=mailconfig.fetchEncoding)
		savefile.write('\n'+fulltext+'-'*80+'\n')
	else:
		print('Bad message number')

def msgnum(command):
	try:
		return int(command.split()[1])
	except:
		return -1

helptext = """
Available commands:
i    - index display
l n? - list all messages (or just message n)
d n? - mark all messages for deletion (or just message n)
s n? - save all messages to a file (or just message n)
m    - compose and send a new mail message
q    - quit pymail
?    - display this help text
"""	

def interact(msgList, msgSizes, mailfile):
	showindex(msgList, msgSizes)	
	toDelete = []
	while True:
		try:
			command = input('[Pymail] Action? (i, l, d, s, m, q, ?)')
		except EOFError:
			command = 'q'
		if not command: command ='*'

		if command == 'q':
			break
		elif command[0] == 'i':
			showindex(msgList, msgSizes)
		elif command[0] == 'l':
			if len(command) == 1:
				for i in range(1, len(msgList)+1):
					showmesssage(i, msgList)
			else:
				showmesssage(msgnum(command), msgList)
		elif command[0] == 's':
			if len(command) == 1:
				for i in range(1, len(msgList)+1):
					savemessage(i, mailfile, msgList)
			else:
				savemessage(msgnum(command), mailfile,msgList)
		elif command[0] == 'd':
			if len(command) == 1:
				toDelete = list(range(1,len(msgList)+1))
			else:
				delnum = msgnum(command)
				if (1 <= delnum <= len(msgList)) and (delnum not in toDelete):
					toDelete.append(delnum)
				else:
					print('Bad message number')

		elif command[0] == 'm':
			try:
				sendmessage()
			except:
				print('Error - mail not sent')

		elif command[0] == '?':
			print(helptext)
		else:
			print('What? -- type "?" for command help ')
	return toDelete

def main():
	global parser, sender, fetcher
	mailserver = mailconfig.popservername
	mailuser = mailconfig.popusername
	mailfile = mailconfig.savemailfile

	parser = mailtools.MailParser()
	sender = mailtools.MailSenderAuth()
	fetcher = mailtools.MailFetcherConsole(mailserver, mailuser)

	def progress(i, max):
		print(i, 'of', max)

	hdrsList, msgSizes, ignore = fetcher.downloadAllHeaders(progress)
	msgList = [parser.parseHeaders(hdrtext) for hdrtext in hdrsList]

	print('[Pymail email client]')
	toDelete = interact(msgList, msgSizes, mailfile)
	if toDelete: deletemessage(toDelete)

if __name__ == '__main__':
	main()