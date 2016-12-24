'''test-stream-modes.py'''

import sys
def reader(F):
	tmp, sys.stdin = sys.stdin, F
	line = input()
	print(line)
	sys.stdin = tmp
	reader(open('test-stream-modes.py'))
	reader(open('test-stream-modes.py', 'rb'))

def writer(F):
	tmp, sys.stdout = sys.stdout, F
	print(99, 'spam')
	sys.stdout = tmp

writer(open('tmp', 'w'))
print(open('tmp').read())

# writer(open('tmp','wb'))
# writer(open('tmp','w',0))
