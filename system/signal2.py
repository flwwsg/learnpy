'''signal2.py'''
import sys, signal, time

def now():
	return time.ctime(time.time())

def onSignal(signum, stackframe):
	print('Got signal', signum, 'at', now())

while True:
	print('Setting at', now())
	signal.signal(signal.SIGALRM, onSignal)
	signal.alarm(5)
	signal.pause()
