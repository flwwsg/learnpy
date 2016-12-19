'''spawnv.py'''

import os, sys

for i in range(10):
	if sys.platform[:3] == 'win':
		pypath = sys.executable
		os.spawnv(os.P_NOWAIT, pypath, ('py -3', 'child.py', str(i)))
	else:
		pid = os.fork()
		if pid != 0:
			print('Process %d spawned' % pid)
		else:
			os.execlp('python3', 'python3','child.py', str(i))
print('Main process exiting')