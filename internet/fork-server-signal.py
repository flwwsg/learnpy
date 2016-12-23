'''fork-server-signal.py'''
import os, time, sys, signal
from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost,myPort))
sockobj.listen(5)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

def now():
	return time.ctime(time.time())

def handClient(connection):
	time.sleep(5)
	while True:
		data = connection.recv(1024)
		if not data: break
		reply = 'Echo=>%s at %s' % (data, now())
		connection.send(reply.encode())
	connection.close()
	os._exit(0)

def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print('Server connected by', address, end=' ')
		print('at', now())
		childPid = os.fork()
		if childPid == 0:
			handClient(connection)

dispatcher()