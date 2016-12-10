#! /bin/env python3
'''fork1.py'''

import os
def child():
	print('Hello from fork1 child', os.getpid())
	os._exit(0)

def parent():
	while True:
		newpid = os.fork()
		if newpid == 0:
			child()
		else:
			print('Hello from fork1 parent', os.getpid(), newpid)

		if input() == 'q':
			break

if __name__ == '__main__':
	parent()