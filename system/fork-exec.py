'''fork-exec.py'''

import os
parm = 0
while True:
	parm += 1
	pid = os.fork()
	if pid == 0:
		os.execlp('python', 'python', 'child.py', str(parm))
		assert False, 'error starting program'
	else:
		print('fork-exec Child is ', pid)
		if input() == 'q': break