'''multi5.py'''

import os
from multiprocessing import Process

def runprogram(arg):
	os.execlp('python3','python3','child.py', str(arg))

if __name__ == '__main__':
	for i in range(5):
		Process(target=runprogram, args=(i,)).start()
	print('parent exit')